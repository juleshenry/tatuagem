"""
DEPRECATED: This file is maintained for backward compatibility only.
Please use font_manager.py instead.
"""

import warnings
warnings.warn(
    "initi.py is deprecated. Please use font_manager.py instead.",
    DeprecationWarning,
    stacklevel=2
)

from font_manager import init_and_create_templates, get_font_png_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        init_and_create_templates(sys.argv[1])
    else:
        init_and_create_templates("unicode-arial.ttf")
