"""Deploy 管家.html to the dongyun GitHub repository."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SOURCE_FILE = Path(__file__).with_name("管家.html")
REPOSITORY = "https://github.com/damei0526/dongyun.git"
BRANCH = "main"


def git(*args: str, cwd: Path | None = None, non_interactive: bool = False) -> None:
    env = os.environ.copy()
    if non_interactive:
        env.update({"GCM_INTERACTIVE": "never", "GIT_TERMINAL_PROMPT": "0"})
    subprocess.run(["git", *args], cwd=cwd, env=env, check=True)


def main() -> None:
    if not SOURCE_FILE.is_file():
        raise FileNotFoundError(f"找不到待部署文件：{SOURCE_FILE}")

    with tempfile.TemporaryDirectory(prefix="dongyun-deploy-") as temporary_directory:
        repo_dir = Path(temporary_directory) / "dongyun"
        git("clone", "--branch", BRANCH, "--single-branch", REPOSITORY, str(repo_dir))
        git("config", "user.name", "damei0526", cwd=repo_dir)
        git("config", "user.email", "damei0526@users.noreply.github.com", cwd=repo_dir)
        shutil.copy2(SOURCE_FILE, repo_dir / SOURCE_FILE.name)
        git("add", SOURCE_FILE.name, cwd=repo_dir)

        changes = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo_dir)
        if changes.returncode == 0:
            print("上线成功！")
            return
        if changes.returncode != 1:
            raise subprocess.CalledProcessError(changes.returncode, changes.args)

        git("commit", "-m", "Add member recharge placeholder", cwd=repo_dir)
        git("push", "origin", BRANCH, cwd=repo_dir, non_interactive=True)

    print("上线成功！")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"上线失败：{error}", file=sys.stderr)
        sys.exit(1)
