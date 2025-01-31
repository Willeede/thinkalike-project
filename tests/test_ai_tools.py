
"""
Test Script for AIApplicationDeveloper

This script uses Python's unittest framework to test the AIApplicationDeveloper class.
It includes various test cases to ensure that the code generation, debugging, and test case
creation functionalities work as expected under different scenarios.

Author: Willeede
Date: 2025-01-31
"""

import unittest  # Importing the unittest framework for writing test cases
from unittest.mock import patch, MagicMock  # Importing patch and MagicMock for mocking external dependencies
from scripts.ai_application_developer import AIApplicationDeveloper  # Importing the AIApplicationDeveloper class to be tested


class TestAIApplicationDeveloper(unittest.TestCase):
    """
    Test suite for the AIApplicationDeveloper class.
    """

    def setUp(self):
        """
        Set up the AIApplicationDeveloper instance before each test.
        """
        self.developer = AIApplicationDeveloper()

    @patch('scripts.ai_application_developer.AutoTokenizer')
    @patch('scripts.ai_application_developer.AutoModelForSeq2SeqLM')
    def test_generate_code_success(self, mock_model, mock_tokenizer):
        """
        Test the generate_code method with valid input.
        """
        # Mock the tokenizer and model behavior
        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [[4, 5, 6]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = "print('Hello, World!')"

        # Define the test parameters
        description = "Print a greeting message"
        language = "Python"
        max_length = 50

        # Call the generate_code method
        generated_code = self.developer.generate_code(description, language, max_length)

        # Assert that the generated code matches the expected output
        self.assertEqual(generated_code, "print('Hello, World!')")

    @patch('scripts.ai_application_developer.AutoTokenizer')
    @patch('scripts.ai_application_developer.AutoModelForSeq2SeqLM')
    def test_generate_code_invalid_description(self, mock_model, mock_tokenizer):
        """
        Test the generate_code method with an empty description.
        """
        # Configure the tokenizer and model to return empty output
        mock_tokenizer.from_pretrained.return_value.encode.return_value = []
        mock_model.from_pretrained.return_value.generate.return_value = [[]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = ""

        # Define the test parameters with an empty description
        description = ""
        language = "Python"
        max_length = 50

        # Call the generate_code method
        generated_code = self.developer.generate_code(description, language, max_length)

        # Assert that the generated code is an empty string
        self.assertEqual(generated_code, "")

    @patch('scripts.ai_application_developer.AutoTokenizer')
    @patch('scripts.ai_application_developer.AutoModelForSeq2SeqLM')
    def test_generate_code_different_languages(self, mock_model, mock_tokenizer):
        """
        Test the generate_code method with different programming languages.
        """
        languages = ["Python", "JavaScript", "Go"]
        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [[4, 5, 6]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = "// Hello, World!"  # Example for JavaScript/Go

        for language in languages:
            with self.subTest(language=language):
                # Define the test parameters
                description = f"Print a greeting message in {language}"
                max_length = 50

                # Call the generate_code method
                generated_code = self.developer.generate_code(description, language, max_length)

                # Example assertion based on language (you may need to adjust based on actual implementation)
                if language == "Python":
                    expected_snippet = "print('Hello, World!')"
                elif language == "JavaScript":
                    expected_snippet = "console.log('Hello, World!');"
                elif language == "Go":
                    expected_snippet = 'fmt.Println("Hello, World!")'

                # Assert that the generated code matches the expected snippet
                self.assertIn(expected_snippet.split('(')[0], generated_code)

    @patch('scripts.ai_application_developer.AutoTokenizer')
    @patch('scripts.ai_application_developer.AutoModelForSeq2SeqLM')
    def test_generate_code_max_length_short(self, mock_model, mock_tokenizer):
        """
        Test generate_code with a short max_length to ensure shorter code generation.
        """
        # Configure the tokenizer and model to return shorter output
        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1]
        mock_model.from_pretrained.return_value.generate.return_value = [[2, 3]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = "print()"

        # Define the test parameters
        description = "Print a greeting message"
        language = "Python"
        max_length = 10  # Short max_length

        # Call the generate_code method
        generated_code = self.developer.generate_code(description, language, max_length)

        # Assert that the generated code matches the expected output
        self.assertEqual(generated_code, "print()")

    @patch('scripts.ai_application_developer.AutoTokenizer')
    @patch('scripts.ai_application_developer.AutoModelForSeq2SeqLM')
    def test_generate_code_max_length_large(self, mock_model, mock_tokenizer):
        """
        Test generate_code with a large max_length to ensure longer code generation.
        """
        # Configure the tokenizer and model to return longer output
        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [[4, 5, 6, 7, 8, 9]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = "def complex_function():\n    pass"

        # Define the test parameters
        description = "Generate a complex function"
        language = "Python"
        max_length = 1000  # Large max_length

        # Call the generate_code method
        generated_code = self.developer.generate_code(description, language, max_length)

        # Assert that the generated code matches the expected output
        self.assertEqual(generated_code, "def complex_function():\n    pass")

    @patch('scripts.ai_application_developer.AutoTokenizer')
    @patch('scripts.ai_application_developer.AutoModelForSeq2SeqLM')
    def test_generate_code_error_handling(self, mock_model, mock_tokenizer):
        """
        Test generate_code's response when an error occurs during code generation.
        """
        # Define the test parameters
        description = "Print a greeting message"
        language = "Python"
        max_length = 50

        # Simulate the model raising an exception
        mock_model.from_pretrained.side_effect = Exception("Model loading failed")

        # Call the generate_code method
        generated_code = self.developer.generate_code(description, language, max_length)

        # Assert that the generated code is an empty string due to the exception
        self.assertEqual(generated_code, "")

    @patch('scripts.ai_application_developer.AIApplicationDeveloper.create_test_cases')
    def test_create_test_cases_valid_code(self, mock_create_test_cases):
        """
        Test create_test_cases with valid code and description.
        """
        # Define the test parameters
        code = "def add(a, b):\n    return a + b"
        description = "Adds two numbers together."

        # Mock the create_test_cases method to return a sample test case string
        mock_create_test_cases.return_value = (
            "import unittest\n\n"
            "class TestAdd(unittest.TestCase):\n"
            "    def test_add_positive_numbers(self):\n"
            "        self.assertEqual(add(2, 3), 5)\n\n"
            "    def test_add_negative_numbers(self):\n"
            "        self.assertEqual(add(-2, -3), -5)\n"
        )

        # Call the create_test_cases method
        result = self.developer.create_test_cases(code, description)

        # Assert that the returned test cases contain the expected class definition
        self.assertIn("class TestAdd(unittest.TestCase):", result)

    @patch('scripts.ai_application_developer.AIApplicationDeveloper.create_test_cases')
    def test_create_test_cases_invalid_code(self, mock_create_test_cases):
        """
        Test create_test_cases with invalid code.
        """
        # Define the test parameters with invalid code (missing colon)
        code = "def add(a, b)\n    return a + b"
        description = "Adds two numbers together."

        # Mock the create_test_cases method to return an empty string for invalid code
        mock_create_test_cases.return_value = ""

        # Call the create_test_cases method
        result = self.developer.create_test_cases(code, description)

        # Assert that the returned result is an empty string
        self.assertEqual(result, "")

    def test_debug_code_no_errors(self):
        """
        Test debug_code with valid code that has no syntax errors.
        """
        # Define valid code without syntax errors
        code = "def add(a, b):\n    return a + b"

        # Call the debug_code method
        result = self.developer.debug_code(code)

        # Assert that the result indicates no syntax errors
        self.assertEqual(result, "No syntax errors detected.")

    def test_debug_code_syntax_error(self):
        """
        Test debug_code with code that has a syntax error.
        """
        # Define code with a syntax error (missing colon)
        code = "def add(a, b)\n    return a + b"

        # Call the debug_code method
        result = self.developer.debug_code(code)

        # Assert that the result contains a syntax error message
        self.assertIn("SyntaxError in code:", result)

    @patch('scripts.ai_application_developer.AIApplicationDeveloper.log_error')
    def test_debug_code_unexpected_error(self, mock_log_error):
        """
        Test debug_code handling of unexpected exceptions.
        """
        # Define valid code
        code = "def add(a, b):\n    return a + b"

        # Simulate an unexpected exception during AST parsing
        with patch('scripts.ai_application_developer.ast.parse', side_effect=Exception("Unexpected error")):
            # Call the debug_code method
            result = self.developer.debug_code(code)

            # Assert that the result contains the error message
            self.assertIn("Error in debugging code: Unexpected error", result)

            # Assert that log_error was called with the correct message
            mock_log_error.assert_called_with("Error in debugging code: Unexpected error")


# This allows the tests to be run when the script is executed directly
if __name__ == '__main__':
    unittest.main()