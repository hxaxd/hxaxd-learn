from __future__ import annotations

import contextlib
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from script import consolidate


def git(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


class ConsolidateIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        git(self.repo, "init", "--initial-branch=main")
        git(self.repo, "config", "user.name", "Test User")
        git(self.repo, "config", "user.email", "test@example.com")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def commit(self, message: str, date: str, content: str | None = None) -> str:
        if content is not None:
            (self.repo / "note.md").write_text(content, encoding="utf-8")
            git(self.repo, "add", "note.md")
        env = {
            **os.environ,
            "GIT_AUTHOR_DATE": date,
            "GIT_COMMITTER_DATE": date,
        }
        arguments = ["commit", "-m", message]
        if content is None:
            arguments.insert(1, "--allow-empty")
        git(self.repo, *arguments, env=env)
        return git(self.repo, "rev-parse", "HEAD")

    def run_consolidate(self, *arguments: str) -> int:
        previous = Path.cwd()
        output = io.StringIO()
        try:
            os.chdir(self.repo)
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = consolidate.main(list(arguments))
            self.last_output = output.getvalue()
            return result
        finally:
            os.chdir(previous)

    def test_builds_identical_monthly_trees_without_touching_worktree(self) -> None:
        january_first = self.commit("jan one", "2024-01-01T10:00:00+00:00", "one\n")
        january_last = self.commit("jan two", "2024-01-20T10:00:00+00:00", "two\n")
        february_last = self.commit("feb empty", "2024-02-01T10:00:00+00:00")
        source_head = git(self.repo, "rev-parse", "HEAD")
        (self.repo / "untracked.txt").write_text("keep me\n", encoding="utf-8")

        result = self.run_consolidate(
            "--yes", "--target-branch", "monthly-snapshots"
        )

        self.assertEqual(result, 0, self.last_output)
        self.assertEqual(git(self.repo, "branch", "--show-current"), "main")
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), source_head)
        self.assertEqual((self.repo / "untracked.txt").read_text(encoding="utf-8"), "keep me\n")
        self.assertEqual(git(self.repo, "rev-list", "--count", "monthly-snapshots"), "2")

        snapshots = git(
            self.repo, "rev-list", "--reverse", "monthly-snapshots"
        ).splitlines()
        self.assertEqual(
            git(self.repo, "rev-parse", f"{snapshots[0]}^{{tree}}"),
            git(self.repo, "rev-parse", f"{january_last}^{{tree}}"),
        )
        self.assertEqual(
            git(self.repo, "rev-parse", f"{snapshots[1]}^{{tree}}"),
            git(self.repo, "rev-parse", f"{february_last}^{{tree}}"),
        )
        self.assertNotEqual(january_first, january_last)

    def test_rebuilds_existing_target_atomically(self) -> None:
        self.commit("jan", "2024-01-01T10:00:00+00:00", "one\n")
        result = self.run_consolidate("--yes", "--target-branch", "monthly-snapshots")
        self.assertEqual(result, 0, self.last_output)
        old_tip = git(self.repo, "rev-parse", "monthly-snapshots")
        self.commit("feb", "2024-02-01T10:00:00+00:00", "two\n")
        result = self.run_consolidate("--yes", "--target-branch", "monthly-snapshots")
        self.assertEqual(result, 0, self.last_output)
        new_tip = git(self.repo, "rev-parse", "monthly-snapshots")
        self.assertNotEqual(old_tip, new_tip)
        self.assertEqual(git(self.repo, "rev-list", "--count", new_tip), "2")

    def test_dry_run_does_not_create_target_branch(self) -> None:
        self.commit("jan", "2024-01-01T10:00:00+00:00", "one\n")
        self.assertEqual(
            self.run_consolidate("--dry-run", "--target-branch", "monthly-snapshots"),
            0,
        )
        result = subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", "refs/heads/monthly-snapshots"],
            cwd=self.repo,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
