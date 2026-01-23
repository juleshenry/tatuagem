import os
import json
import subprocess

cache = {}


def get_block_comment(filepath):
    lang = filepath.replace("tests/hello_worlds/", "").split("/")[0]
    if not lang:
        return None
    if lang in cache:
        return cache[lang]
    print("Checking block comment for:", lang)
    prompt = f"What are the block comment delimiters for {lang}? \
    Answer with only 'START_BLOCK: <start_delimiter> END_BLOCK: <end_delimiter>' \
    or 'none' if block comments are not supported."
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )
        response = result.stdout.strip().lower()
        print("Response:", response)
        if "None" in response or "no block" in response:
            cache[lang] = None
        else:
            if "start_block:" in response and "end_block:" in response:
                start_idx = response.find("start_block:") + len("end_block:")
                end_idx = response.find("end_block:", start_idx)
                start = response[start_idx:end_idx].strip()

                end_start_idx = response.find("end_block:") + len("end_block:")
                end = response[end_start_idx:].strip()
                cache[lang] = {"start": start, "end": end}
            else:
                cache[lang] = None
    except subprocess.TimeoutExpired:
        cache[lang] = None
    except Exception:
        cache[lang] = None
    return cache[lang]


ext_lang = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".sh": "Bash",
    ".pl": "Perl",
    ".lua": "Lua",
    ".sql": "SQL",
    ".html": "HTML",
    ".xml": "XML",
    ".css": "CSS",
    ".go": "Go",
    ".rs": "Rust",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".vb": "Visual Basic",
    ".hs": "Haskell",
    ".ml": "OCaml",
    ".fs": "F#",
    ".tcl": "Tcl",
    ".r": "R",
    ".asm": "Assembly",
    ".scm": "Scheme",
    ".lisp": "Lisp",
    ".adb": "Ada",
    ".scpt": "AppleScript",
    ".beta": "BETA",
    ".dockerfile": "Docker",
    ".gml": "GameMaker Language",
    ".slx": "SL",
    ".tf": "Terraform",
    ".vim": "Vim script",
    ".g": "Geode",
    ".svg": "SVG",
    ".jsp": "JSP",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".txt": "Text",
    ".nes": "Nintendo Entertainment System",
    ".chr": "Character ROM",
    ".jpg": "JPEG",
    ".ipynb": "Jupyter Notebook",
}

import time

data = {}
for root, dirs, files in os.walk("tests/hello_worlds"):
    for file in files:
        if file == "ovo.yaml":
            continue
        filepath = os.path.join(root, file)

        comment = get_block_comment(filepath)
        lang = filepath.replace("tests/hello_worlds/", "").split("/")[0]
        data[lang] = comment

with open("comment_block_syntax.json", "w") as f:
    json.dump(data, f, indent=4)
