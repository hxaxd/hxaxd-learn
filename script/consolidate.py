#!/usr/bin/env python3
"""
Git提交历史聚合脚本 (快照版)
功能：将历史按月聚合，每个月生成一个快照提交。
优势：避免Cherry-pick产生的冲突，保证代码状态与当时完全一致。
提交信息格式：第一行为 YYYY-MM-DD (该月最后一次提交的日期)
"""

import subprocess
import sys
from collections import defaultdict
import datetime

def run_command(cmd, check=True):
    """运行Shell命令"""
    try:
        # shell=False 更安全，但需要传入列表
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {' '.join(cmd)}")
        print(f"错误信息: {e.stderr}")
        sys.exit(1)

def get_commits():
    """获取所有提交，按时间正序排列 (旧 -> 新)"""
    # %H: Hash, %ai: ISO Date, %s: Subject
    cmd = ["git", "log", "--reverse", "--format=%H|%ai|%s"]
    result = run_command(cmd)
    
    commits = []
    for line in result.stdout.strip().split("\n"):
        if "|" in line:
            parts = line.split("|", 2)
            if len(parts) == 3:
                commits.append({
                    "hash": parts[0],
                    "date_str": parts[1], # e.g., 2023-01-01 12:00:00 +0800
                    "message": parts[2]
                })
    return commits

def parse_date(date_str):
    """解析Git日期字符串，返回 YYYY-MM-DD"""
    # 提取空格前的日期部分
    return date_str.split(" ")[0]

def group_by_month(commits):
    """按月份分组提交"""
    groups = defaultdict(list)
    for commit in commits:
        date = parse_date(commit["date_str"])
        month_key = date[:7] # YYYY-MM
        groups[month_key].append(commit)
    return groups

def main():
    print("="*60)
    print("Git 历史聚合工具 (快照模式)")
    print("目标：生成 YYYY-MM-DD 格式的月度快照")
    print("="*60)

    # 1. 检查当前状态
    status = run_command(["git", "status", "--porcelain"], check=False)
    if status.stdout.strip():
        print("错误：工作区不干净，请先提交或暂存更改。")
        sys.exit(1)

    print("正在读取提交历史...")
    commits = get_commits()
    if not commits:
        print("没有找到提交记录。")
        return

    monthly_groups = group_by_month(commits)
    sorted_months = sorted(monthly_groups.keys())
    
    print(f"检测到 {len(commits)} 个提交，跨越 {len(sorted_months)} 个月份。")

    # 2. 创建一个新的孤儿分支（不继承旧历史，从零开始）
    new_branch = "consolidated-history-clean"
    print(f"\n正在创建新分支: {new_branch} ...")
    
    # 检查分支是否存在，存在则删除
    run_command(["git", "branch", "-D", new_branch], check=False)
    # 创建孤儿分支 (没有任何历史记录的空分支)
    run_command(["git", "checkout", "--orphan", new_branch])
    # 清空暂存区和工作区（确保从零开始）
    run_command(["git", "rm", "-rf", "."])

    print("开始构建月度快照...")
    
    for month in sorted_months:
        month_commits = monthly_groups[month]
        # 取该月最后一个提交作为“快照点”
        last_commit = month_commits[-1]
        last_date = parse_date(last_commit["date_str"])
        
        print(f"处理 {month} -> 使用快照点: {last_date} ({last_commit['hash'][:7]})")

        # 核心逻辑：使用 read-tree 强制将工作区和暂存区变为目标提交的状态
        # -u: 更新工作区文件
        # --reset: 强制重置
        run_command(["git", "read-tree", "-u", "--reset", last_commit["hash"]])

        # 构建提交信息
        # 第一行：YYYY-MM-DD
        msg_lines = [last_date, ""]
        msg_lines.append(f"包含 {len(month_commits)} 个原始提交的变更:")
        for c in month_commits:
            msg_lines.append(f"- {c['hash'][:7]}: {c['message']}")
        
        full_message = "\n".join(msg_lines)

        # 提交 (使用该月最后一次提交的原始时间，保持时间线大致正确)
        # 这里的 date 只是元数据，提交顺序是线性的
        env = {"GIT_AUTHOR_DATE": last_commit["date_str"], "GIT_COMMITTER_DATE": last_commit["date_str"]}
        
        # 调用 git commit
        # 注意：因为 read-tree 已经把暂存区准备好了，直接 commit 即可
        subprocess.run(
            ["git", "commit", "-m", full_message],
            env=env, # 注入时间环境变量
            check=True,
            stdout=subprocess.DEVNULL # 减少噪音
        )

    print("\n" + "="*60)
    print("聚合完成！")
    print("="*60)
    print(f"当前所在分支: {new_branch}")
    print("\n请检查历史记录:")
    print("git log --oneline --graph --stat | head -n 20")
    print("\n如果满意，可以使用以下命令强制推送到远程（请谨慎）：")
    print(f"git push -f origin {new_branch}:main")

if __name__ == "__main__":
    main()