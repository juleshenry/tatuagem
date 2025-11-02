import json
import os

# Load override and default syntax data
try:
    with open('lang_comment_block_syntax.json', 'r') as f:
        lang_data = json.load(f)
except FileNotFoundError:
    lang_data = {'Languages': {}, 'Extensions': {}}

try:
    with open('default_extension_syntax.json', 'r') as f:
        default_data = json.load(f)
except FileNotFoundError:
    default_data = {'Extensions': {}}

# Extension to language mapping
ext_lang = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C',
    '.cs': 'C#',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.sh': 'Bash',
    '.pl': 'Perl',
    '.lua': 'Lua',
    '.sql': 'SQL',
    '.html': 'HTML',
    '.xml': 'XML',
    '.css': 'CSS',
    '.go': 'Go',
    '.rs': 'Rust',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.scala': 'Scala',
    '.vb': 'Visual Basic',
    '.hs': 'Haskell',
    '.ml': 'OCaml',
    '.fs': 'F#',
    '.tcl': 'Tcl',
    '.r': 'R',
    '.asm': 'Assembly',
    '.scm': 'Scheme',
    '.lisp': 'Lisp',
    '.adb': 'Ada',
    '.scpt': 'AppleScript',
    '.beta': 'BETA',
    '.dockerfile': 'Docker',
    '.gml': 'GameMaker Language',
    '.slx': 'SL',
    '.tf': 'Terraform',
    '.vim': 'Vim script',
    '.g': 'Geode',
    '.svg': 'SVG',
    '.jsp': 'JSP',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.md': 'Markdown',
    '.txt': 'Text',
    '.nes': 'Nintendo Entertainment System',
    '.chr': 'Character ROM',
    '.jpg': 'JPEG',
    '.ipynb': 'Jupyter Notebook',
}

def get_comment_syntax(filepath):
    """
    Get the comment syntax for a filepath.
    Priority: default Extensions > lang_data Languages if ext maps to lang > None
    """
    ext = os.path.splitext(os.path.basename(filepath))[1].lower()
    
    # Check default Extensions first
    if ext in default_data.get('Extensions', {}):
        return default_data['Extensions'][ext]
    
    # Check if extension maps to a language with override
    lang = ext_lang.get(ext)
    if lang and lang in lang_data.get('Languages', {}):
        return lang_data['Languages'][lang]
    
    return None

if __name__ == "__main__":
    # Example usage
    # import sys
    # if len(sys.argv) > 1:
    #     filepath = sys.argv[1]
    #     syntax = get_comment_syntax(filepath)
    #     if syntax:
    #         print(json.dumps(syntax))
    #     else:
    #         print("null")
    # else:
    #     print("Usage: python override.py <filepath>")
    # Process comment block syntax to remove 'k: ' prefix
    for lang, syntax in lang_data.get('Languages', {}).items():
        if 'start_block' in syntax and syntax['start_block'].startswith('k: '):
            syntax['start_block'] = syntax['start_block'][3:]

    # for ext, syntax in lang_data.get('Extensions', {}).items():
    #     if 'start_block' in syntax and syntax['start_block'].startswith('k: '):
    #         syntax['start_block'] = syntax['start_block'][3:]

    # Save the modified data back to the file
    with open('lang_comment_block_syntax.json', 'w') as f:
        json.dump(lang_data, f, indent=2)