#!/usr/bin/env python3
"""将 Git 历史按月聚合为不触碰工作区的快照提交。"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Mapping, Sequence


DEFAULT_TARGET_BRANCH = "consolidated-history-clean"


class CommandError(RuntimeError):
    """Git 命令执行失败。"""


def configure_standard_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


@dataclass(frozen=True)
class Commit:
    hash: str
    date_str: str
    message: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将 Git 历史按月聚合为快照提交。")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示计划，不创建提交对象、不更新分支。",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="跳过确认提示，适合非交互运行。",
    )
    parser.add_argument(
        "--source",
        default="HEAD",
        help="要聚合的源修订，默认为 HEAD。",
    )
    parser.add_argument(
        "--target-branch",
        default=DEFAULT_TARGET_BRANCH,
        help=f"目标分支，默认为 {DEFAULT_TARGET_BRANCH}。",
    )
    return parser.parse_args(argv)


def run_command(
    cmd: Sequence[str],
    *,
    check: bool = True,
    input_text: str | None = None,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            list(cmd),
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=check,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        command = " ".join(cmd)
        details = (exc.stderr or exc.stdout or "").strip()
        raise CommandError(f"命令执行失败: {command}\n{details}") from exc


def ensure_git_repository() -> None:
    result = run_command(["git", "rev-parse", "--git-dir"], check=False)
    if result.returncode != 0:
        raise CommandError("当前目录不是 Git 仓库。")


def validate_branch_name(branch: str) -> None:
    result = run_command(["git", "check-ref-format", "--branch", branch], check=False)
    if result.returncode != 0:
        raise CommandError(f"目标分支名无效: {branch}")


def get_commits(revision: str = "HEAD") -> list[Commit]:
    result = run_command(
        ["git", "log", "--reverse", "--format=%H%x00%aI%x00%s", revision]
    )
    commits: list[Commit] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        parts = line.split("\0", 2)
        if len(parts) != 3:
            raise CommandError("无法解析 git log 输出。")
        commits.append(Commit(hash=parts[0], date_str=parts[1], message=parts[2]))
    return commits


def parse_date(date_str: str) -> str:
    """从 ISO 8601 Git 日期中提取 YYYY-MM-DD。"""
    return date_str[:10]


def group_by_month(commits: Sequence[Commit]) -> dict[str, list[Commit]]:
    groups: dict[str, list[Commit]] = defaultdict(list)
    for commit in commits:
        groups[parse_date(commit.date_str)[:7]].append(commit)
    return groups


def get_current_branch() -> str:
    result = run_command(["git", "branch", "--show-current"], check=False)
    return result.stdout.strip() or "HEAD"


def get_branch_tip(branch: str) -> str | None:
    result = run_command(
        ["git", "rev-parse", "--verify", f"refs/heads/{branch}"],
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def branch_is_checked_out(branch: str) -> bool:
    result = run_command(["git", "worktree", "list", "--porcelain"])
    expected = f"branch refs/heads/{branch}"
    return expected in result.stdout.splitlines()


def resolve_git_identity(revision: str) -> tuple[str, str]:
    name = run_command(["git", "config", "--get", "user.name"], check=False).stdout.strip()
    email = run_command(["git", "config", "--get", "user.email"], check=False).stdout.strip()

    if not name or not email:
        latest = run_command(
            ["git", "log", "-1", "--format=%an%x00%ae", revision],
            check=False,
        ).stdout.strip()
        if "\0" in latest:
            fallback_name, fallback_email = latest.split("\0", 1)
            name = name or fallback_name.strip()
            email = email or fallback_email.strip()

    if not name or not email:
        raise CommandError(
            "无法确定 Git 提交身份。请设置 user.name 和 user.email。"
        )
    return name, email


def print_plan(
    commits: Sequence[Commit],
    monthly_groups: Mapping[str, Sequence[Commit]],
    current_branch: str,
    source: str,
    target_branch: str,
) -> None:
    print(f"当前分支: {current_branch}")
    print(f"源修订: {source}")
    print(f"目标分支: {target_branch}")
    print(f"原始提交数: {len(commits)}")
    print(f"将生成的月度快照数: {len(monthly_groups)}")
    print("目标分支处理: " + ("原子更新" if get_branch_tip(target_branch) else "新建"))
    print("工作区处理: 不切换分支、不修改索引和文件")
    print("\n月度快照:")
    for month in sorted(monthly_groups):
        month_commits = monthly_groups[month]
        last_commit = month_commits[-1]
        print(
            f"- {month}: {len(month_commits)} 个提交, "
            f"快照点 {last_commit.hash[:7]}"
        )


def confirm_execution(target_branch: str) -> None:
    expected = f"REBUILD {target_branch}"
    print("\n警告: 即将重建目标分支引用；源分支和工作区不会被修改。")
    print(f"请输入以下内容确认执行:\n{expected}")
    try:
        response = input("> ").strip()
    except EOFError:
        response = ""
    if response != expected:
        raise CommandError("确认内容不匹配，已取消。")


def snapshot_message(month: str, commits: Sequence[Commit]) -> str:
    lines = [month, "", f"包含 {len(commits)} 个原始提交的变更:"]
    lines.extend(f"- {commit.hash[:7]}: {commit.message}" for commit in commits)
    return "\n".join(lines) + "\n"


def create_snapshot_commit(
    month: str,
    commits: Sequence[Commit],
    parent: str | None,
    author_name: str,
    author_email: str,
) -> str:
    last_commit = commits[-1]
    tree = run_command(
        ["git", "rev-parse", f"{last_commit.hash}^{{tree}}"]
    ).stdout.strip()
    command = ["git", "commit-tree", tree]
    if parent:
        command.extend(["-p", parent])
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": author_name,
        "GIT_AUTHOR_EMAIL": author_email,
        "GIT_COMMITTER_NAME": author_name,
        "GIT_COMMITTER_EMAIL": author_email,
        "GIT_AUTHOR_DATE": last_commit.date_str,
        "GIT_COMMITTER_DATE": last_commit.date_str,
    }
    return run_command(
        command,
        input_text=snapshot_message(month, commits),
        env=env,
    ).stdout.strip()


def build_snapshot_history(
    monthly_groups: Mapping[str, Sequence[Commit]],
    author_name: str,
    author_email: str,
) -> str:
    parent = None
    for month in sorted(monthly_groups):
        commits = monthly_groups[month]
        last_commit = commits[-1]
        print(
            f"构建 {month}: {parse_date(last_commit.date_str)} "
            f"({last_commit.hash[:7]})"
        )
        parent = create_snapshot_commit(
            month, commits, parent, author_name, author_email
        )
    if parent is None:
        raise CommandError("没有可生成的月度快照。")
    return parent


def update_target_branch(branch: str, new_tip: str, old_tip: str | None) -> None:
    ref = f"refs/heads/{branch}"
    command = [
        "git",
        "update-ref",
        "-m",
        "rebuild monthly snapshot history",
        ref,
        new_tip,
        old_tip or "",
    ]
    run_command(command)


def main(argv: Sequence[str] | None = None) -> int:
    configure_standard_streams()
    args = parse_args(argv)
    try:
        ensure_git_repository()
        validate_branch_name(args.target_branch)
        commits = get_commits(args.source)
        if not commits:
            raise CommandError("没有找到提交记录。")
        monthly_groups = group_by_month(commits)
        current_branch = get_current_branch()
        print_plan(
            commits,
            monthly_groups,
            current_branch,
            args.source,
            args.target_branch,
        )
        if args.dry_run:
            print("\nDry run 完成，未执行任何 Git 修改。")
            return 0

        if branch_is_checked_out(args.target_branch):
            raise CommandError(
                f"目标分支 {args.target_branch} 正在某个工作树中使用，拒绝更新。"
            )
        if not args.yes:
            confirm_execution(args.target_branch)

        author_name, author_email = resolve_git_identity(args.source)
        old_tip = get_branch_tip(args.target_branch)
        new_tip = build_snapshot_history(monthly_groups, author_name, author_email)
        update_target_branch(args.target_branch, new_tip, old_tip)
    except CommandError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    print("\n聚合完成。")
    print(f"当前分支仍为: {get_current_branch()}")
    print(f"检查结果: git log --oneline --graph --stat {args.target_branch}")
    print(
        "如需发布，请谨慎执行: "
        f"git push --force-with-lease origin {args.target_branch}:main"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
