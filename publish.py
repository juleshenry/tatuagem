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

    new_content = re.sub(old_pattern, new_text, content, flags=re.MULTILINE)

    with open(file_path, "w") as f:
        f.write(new_content)


def update_changelog(new_version):
    file_path = "CHANGELOG.md"
    if not os.path.exists(file_path):
        return

    # Ensure version starts with 'v' for the changelog
    display_version = new_version if new_version.startswith("v") else f"v{new_version}"

    date_str = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"\n## {display_version} ({date_str})\n\n* Automated release update\n"

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Insert after the header
    for i, line in enumerate(lines):
        if "# Changelog" in line:
            lines.insert(i + 1, new_entry)
            break

    with open(file_path, "w") as f:
        f.writelines(lines)


def get_current_version():
    if not os.path.exists("pyproject.toml"):
        return "0.0.0"
    with open("pyproject.toml", "r") as f:
        content = f.read()
    match = re.search(r'version\s*=\s*["\']v?(.*?)["\']', content)
    return match.group(1) if match else "0.0.0"


def suggest_next_version(version):
    parts = version.split(".")
    if not parts or not parts[-1].isdigit():
        return version + ".1"

    # Increment the last numeric part
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def main():
    current_version = get_current_version()
    suggested_version = suggest_next_version(current_version)

    if len(sys.argv) < 2:
        print(f"Current version (normalized): {current_version}")
        new_version = input(f"Enter new version (suggested: {suggested_version}): ")
        if not new_version:
            print("Aborted.")
            sys.exit(0)
    else:
        new_version = sys.argv[1]

    # Normalize new_version (remove 'v' prefix if present)
    clean_version = new_version[1:] if new_version.startswith("v") else new_version
    tag_version = f"v{clean_version}"

    print(f"--- Preparing Distribution for {tag_version} ---")

    # 1. Update version files
    print(f"Updating pyproject.toml to {clean_version}...")
    update_file(
        "pyproject.toml",
        r'^version\s*=\s*["\'].*?["\']',
        f'version = "{clean_version}"',
    )

    print(f"Updating tatuagem/__init__.py to {clean_version}...")
    update_file(
        "tatuagem/__init__.py",
        r'^__version__\s*=\s*["\'].*?["\']',
        f'__version__ = "{clean_version}"',
    )

    # 2. Update CHANGELOG.md
    print("Updating CHANGELOG.md...")
    update_changelog(clean_version)

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

    # # 4. Twine Upload
    # print("Uploading to PyPI...")
    # # Note: Twine will prompt for credentials unless configured in ~/.pypirc or env vars
    # run_command("python3 -m twine upload dist/*")

    # 5. Git Tag and Push
    print("Tagging and pushing to git...")
    run_command(f"git add pyproject.toml tatuagem/__init__.py CHANGELOG.md")
    run_command(f'git commit -m "Release {tag_version}"')
    run_command(f"git tag {tag_version}")
    run_command(f"git push origin main")
    run_command(f"git push origin --tags")

    print(f"\nDone! {tag_version} has been built, and tagged.")


if __name__ == "__main__":
    main()
