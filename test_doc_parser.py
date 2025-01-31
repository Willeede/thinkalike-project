import unittest
from doc_parser import create_doc_list, extract_code_comments, transform_markdown

class TestDocParser(unittest.TestCase):
    """
    Unit tests for the doc_parser.py module.
    """

    def setUp(self):
        """
        Initializes data before each test.
        """
        # Sample content for create_doc_list
        self.sample_content = "Line1\nLine2\nLine3"
        
        # Sample code for extract_code_comments
        self.sample_code = """
# This is a comment
def greet(name):
    print(f"Hello, {name}!")  # Greets the user
"""
        
        # Sample markdown for transform_markdown
        self.sample_markdown = "# Title\n\nThis is a **bold** statement."

    def test_create_doc_list_basic(self):
        """
        Test create_doc_list with standard input.
        """
        expected = ['Line1', 'Line2', 'Line3']
        result = create_doc_list(self.sample_content)
        self.assertEqual(result, expected)

    def test_create_doc_list_empty(self):
        """
        Test create_doc_list with empty string.
        """
        expected = ['']
        result = create_doc_list('')
        self.assertEqual(result, expected)

    def test_create_doc_list_no_newlines(self):
        """
        Test create_doc_list with content that has no newline characters.
        """
        content = "SingleLine"
        expected = ['SingleLine']
        result = create_doc_list(content)
        self.assertEqual(result, expected)

    def test_extract_code_comments_basic(self):
        """
        Test extract_code_comments with standard code input.
        """
        expected = ['This is a comment', 'Greets the user']
        result = extract_code_comments(self.sample_code)
        self.assertEqual(result, expected)

    def test_extract_code_comments_no_comments(self):
        """
        Test extract_code_comments when there are no comments.
        """
        code = """
def add(a, b):
    return a + b
"""
        expected = []
        result = extract_code_comments(code)
        self.assertEqual(result, expected)

    def test_extract_code_comments_multiple_comments(self):
        """
        Test extract_code_comments with multiple comments.
        """
        code = """
# First comment
# Second comment
def multiply(a, b):
    return a * b  # Inline comment
"""
        expected = ['First comment', 'Second comment', 'Inline comment']
        result = extract_code_comments(code)
        self.assertEqual(result, expected)

    def test_transform_markdown_basic(self):
        """
        Test transform_markdown with standard markdown input.
        """
        expected = '<h1>Title</h1>\n<p>This is a <strong>bold</strong> statement.</p>'
        result = transform_markdown(self.sample_markdown)
        self.assertEqual(result, expected)

    def test_transform_markdown_empty(self):
        """
        Test transform_markdown with empty string.
        """
        expected = ''
        result = transform_markdown('')
        self.assertEqual(result, expected)

    def test_transform_markdown_complex(self):
        """
        Test transform_markdown with more complex markdown.
        """
        markdown_text = "# Heading\n\n- Item 1\n- Item 2\n\n[Link](https://example.com)"
        expected = '<h1>Heading</h1>\n<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n</ul>\n<p><a href="https://example.com">Link</a></p>'
        result = transform_markdown(markdown_text)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
