"""
This module provides functions to parse and process documentation content.
It includes capabilities to split documents into lists, extract comments from code,
and transform markdown text into HTML.
"""

import markdown  # External library for markdown processing

def create_doc_list(content):
    """
    Splits the given content into a list of lines.

    Parameters:
    content (str): The content of the document.

    Returns:
    list: A list of lines from the content.
    """
    # Split the content by newline characters to create a list of lines
    return content.split('\n')


def extract_code_comments(code):
    """
    Extracts comment lines from the provided code, including inline comments.

    Parameters:
    code (str): A string containing code snippets, possibly with comments.

    Returns:
    list: A list of comment strings found in the code.
    """
    comments = []
    for line in code.split('\n'):
        stripped_line = line.strip()
        
        # Check for full-line comments
        if stripped_line.startswith('#'):
            # Remove the comment symbol and any leading/trailing whitespace
            comment = stripped_line.lstrip('#').strip()
            comments.append(comment)
        else:
            # Check for inline comments
            if '#' in stripped_line:
                # Split the line at the first '#' and take the comment part
                comment = stripped_line.split('#', 1)[1].strip()
                comments.append(comment)
    return comments


def transform_markdown(markdown_text):
    """
    Converts markdown-formatted text into HTML.

    Parameters:
    markdown_text (str): A string containing markdown-formatted text.

    Returns:
    str: A string containing the HTML representation of the markdown.
    """
    # Use the markdown library to convert markdown text to HTML
    html = markdown.markdown(markdown_text)
    return html


# Example usage (if you run this script directly)
if __name__ == '__main__':
    sample_content = """# Sample Document

This is a sample document.

## Section 1
Content of section 1.

## Section 2
Content of section 2."""

    sample_code = """
# This is a sample function
def greet(name):
    print(f"Hello, {name}!")  # Greets the user
"""

    sample_markdown = "# Heading\n\nThis is a **bold** statement."

    # Test create_doc_list
    doc_list = create_doc_list(sample_content)
    print("Document List:")
    for line in doc_list:
        print(line)

    # Test extract_code_comments
    comments = extract_code_comments(sample_code)
    print("\nExtracted Comments:")
    for comment in comments:
        print(comment)

    # Test transform_markdown
    html_output = transform_markdown(sample_markdown)
    print("\nHTML Output:")
    print(html_output)