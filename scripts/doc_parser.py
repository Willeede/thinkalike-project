import logging
import os
import subprocess
import tokenize
from io import BytesIO
from typing import List

# Configure logging to display errors in the console
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DocParser:
    """A class to parse and manage documentation files for the ThinkAlike
    project."""

    def create_doc_list(self, directory: str) -> List[str]:
        """Scans the given directory and returns a list of all Markdown (.md)
        file paths.

        Parameters:
            directory (str): The path to the directory to scan.

        Returns:
            List[str]: A list of paths to Markdown files.
        """
        markdown_files = []
        try:
            # Walk through the directory and its subdirectories
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        markdown_files.append(file_path)
            return markdown_files
        except Exception as e:
            logging.error(f"Error scanning directory '{directory}': {e}")
            return []

    def extract_code_comments(self, python_file: str) -> List[str]:
        """Extracts all comments from a Python file, including single-line
        comments and multi-line docstrings.

        Parameters:
            python_file (str): The path to the Python file.

        Returns:
            List[str]: A list containing all extracted comments from the Python file.
        """
        comments = []
        try:
            with open(python_file, "rb") as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.COMMENT:
                        # Single-line comment
                        comments.append(token.string)
                    elif token.type == tokenize.STRING:
                        # Docstring (multi-line comment)
                        if token.start[1] == 0:
                            comments.append(token.string)
            return comments
        except FileNotFoundError:
            logging.error(f"Python file '{python_file}' not found.")
            return []
        except Exception as e:
            logging.error(f"Error extracting comments from '{python_file}': {e}")
            return []

    def transform_markdown(self, rst_file: str, output_md: str) -> bool:
        """Transforms a reStructuredText (.rst) file into a Markdown (.md) file
        using Pandoc.

        Parameters:
            rst_file (str): The path to the .rst file.
            output_md (str): The desired path for the output .md file.

        Returns:
            bool: True if transformation is successful, False otherwise.
        """
        try:
            # Run Pandoc to convert RST to Markdown
            subprocess.run(
                ["pandoc", rst_file, "-f", "rst", "-t", "markdown", "-o", output_md],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Pandoc error while converting '{rst_file}' to '{output_md}': {e.stderr.decode().strip()}"
            )
            return False
        except FileNotFoundError:
            logging.error("Pandoc is not installed or not found in the system PATH.")
            return False
        except Exception as e:
            logging.error(f"Unexpected error during transformation: {e}")
            return False
