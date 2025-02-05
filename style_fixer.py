"""
Style Fixer Script

This script demonstrates how to automatically fix code style and formatting issues using Python tools.
It addresses:
- Inconsistent indentation (mix of tabs/spaces)
- Lines that exceed the recommended length
- Overall code formatting for improved readability

Usage:
    python style_fixer.py <path_to_python_file>
"""

import sys
import os

try:
    import autopep8
except ImportError:
    print("The 'autopep8' module is required but not installed. Install it using 'pip install autopep8'.")
    sys.exit(1)


def fix_code_style(file_path: str, max_line_length: int = 120) -> str:
    """
    Fixes the code style of the provided Python file using autopep8.

    This function reads the source code from the specified file, applies autopep8 fixes
    such as re-indentation, enforcing the maximum line length, and adjusting spacing,
    then returns the formatted code.

    :param file_path: Path to the Python file to be fixed.
    :param max_line_length: Maximum allowed line length (default is 120).
    :return: The formatted code as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            original_code = source_file.read()

        # Configure autopep8 options:
        # - max_line_length ensures lines do not exceed the specified length.
        # - aggressive mode helps fix more nuanced formatting issues, including inconsistent indentation.
        options = {
            "max_line_length": max_line_length,
            "aggressive": 1,
        }

        fixed_code = autopep8.fix_code(original_code, options=options)
        return fixed_code
    except Exception as e:
        print(f"Error fixing code style for file {file_path}: {str(e)}")
        sys.exit(1)


def write_fixed_code(file_path: str, fixed_code: str) -> None:
    """
    Writes the formatted code to a new file to avoid overwriting the original file.

    :param file_path: The original file path.
    :param fixed_code: The code after formatting.
    """
    # Create a new file path by appending '_fixed' before the .py extension.
    fixed_file_path = file_path.rsplit(".py", 1)[0] + "_fixed.py"
    try:
        with open(fixed_file_path, "w", encoding="utf-8") as fixed_file:
            fixed_file.write(fixed_code)
        print(f"Formatted code has been written to: {fixed_file_path}")
    except Exception as e:
        print(f"Error writing fixed code to file: {str(e)}")
        sys.exit(1)


def main() -> None:
    """
    Main function that processes the input file and applies code style fixes.

    This function expects one command-line argument (the path to the Python file that needs formatting).
    It then fixes the code style and writes the formatted code to a new file.
    """
    if len(sys.argv) != 2:
        print("Usage: python style_fixer.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    formatted_code = fix_code_style(file_path)
    write_fixed_code(file_path, formatted_code)


if __name__ == "__main__":
    main()