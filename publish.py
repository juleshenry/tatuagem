import os
import subprocess
import sys
import re
from datetime import datetime


def run_command(command):
    print(f"Running: {command}")
    # Using Popen to stream output in real-time for interactive commands like twine if needed
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    if process.stdout:
        for line in process.stdout:
            print(line, end="")
    process.wait()
    if process.returncode != 0:
        print(f"\nCommand failed with exit code {process.returncode}")
        sys.exit(1)


def update_file(file_path, old_pattern, new_text):
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found.")
        return
    with open(file_path, "r") as f:
        content = f.read()

    new_content = re.sub(old_pattern, new_text, content)

    with open(file_path, "w") as f:
        f.write(new_content)


def update_changelog(new_version):
    file_path = "CHANGELOG.md"
    if not os.path.exists(file_path):
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"\n## v{new_version} ({date_str})\n\n* Automated release update\n"

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Insert after the header
    for i, line in enumerate(lines):
        if line.startswith("# Changelog"):
            lines.insert(i + 1, new_entry)
            break

    with open(file_path, "w") as f:
        f.writelines(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 publish.py <new_version>")
        sys.exit(1)

    new_version = sys.argv[1]

    print(f"--- Preparing Distribution for v{new_version} ---")

    # 1. Update pyproject.toml
    print("Updating pyproject.toml...")
    update_file("pyproject.toml", r'version = ".*"', f'version = "{new_version}"')

    # 2. Update CHANGELOG.md
    print("Updating CHANGELOG.md...")
    update_changelog(new_version)

    # 3. Clean and Build
    print("Cleaning old builds...")
    if os.path.exists("dist"):
        run_command("rm -rf dist/*")
    if os.path.exists("tatuagem.egg-info"):
        run_command("rm -rf tatuagem.egg-info")

    print("Installing/Updating build tools...")
    run_command("python3 -m pip install --upgrade --break-system-packages build twine")

    print("Building package...")
    run_command("python3 -m build")

    # 4. Twine Upload
    # print("Uploading to PyPI...")
    # # Note: Twine will prompt for credentials unless configured in ~/.pypirc or env vars
    # run_command("python3 -m twine upload dist/*")

    print(f"\nDone! v{new_version} has been built and upload triggered.")


if __name__ == "__main__":
    main()
