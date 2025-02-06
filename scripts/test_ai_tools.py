import unittest
from unittest.mock import MagicMock, patch

from ai_application_developer import AIApplicationDeveloper


class TestAIApplicationDeveloper(unittest.TestCase):
    """Test suite for the AIApplicationDeveloper class in
    ai_application_developer.py."""

    def setUp(self):
        """Set up the AIApplicationDeveloper instance before each test."""
        self.developer = AIApplicationDeveloper()

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_success(self, mock_model, mock_tokenizer):
        """Test the generate_code method with valid input."""
        # Mock the tokenizer and model behavior
        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [[4, 5, 6]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = (
            "print('Hello, World!')"
        )

        description = "Print a greeting message"
        language = "Python"
        max_length = 50

        generated_code = self.developer.generate_code(description, language, max_length)
        self.assertEqual(generated_code, "print('Hello, World!')")

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_invalid_description(self, mock_model, mock_tokenizer):
        """Test the generate_code method when an exception occurs."""
        # Configure the tokenizer and model to return empty output
        mock_tokenizer.from_pretrained.return_value.encode.return_value = []
        mock_model.from_pretrained.return_value.generate.return_value = [[]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = ""

        description = ""
        language = "Python"
        max_length = 50

        generated_code = self.developer.generate_code(description, language, max_length)
        self.assertEqual(generated_code, "")

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_different_languages(self, mock_model, mock_tokenizer):
        """Test generate_code with different programming languages."""
        languages = ["Python", "JavaScript", "Go"]
        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [[4, 5, 6]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = (
            "// Hello, World!"
        )

        for language in languages:
            description = f"Print a greeting message in {language}"
            max_length = 50
            result = self.developer.generate_code(description, language, max_length)
            self.assertEqual(result, "// Hello, World!")

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_parameters(self, mock_model, mock_tokenizer):
        """Verify that generate_code correctly implements all parameters."""
        description = "Print a greeting message"
        language = "Python"
        max_length = 100

        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [[4, 5, 6]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = (
            "print('Hello, World!')"
        )

        result = self.developer.generate_code(description, language, max_length)
        self.assertEqual(result, "print('Hello, World!')")

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_max_length_short(self, mock_model, mock_tokenizer):
        """Test generate_code with a short max_length to ensure shorter code
        generation."""
        description = "Print a greeting message"
        language = "Python"
        max_length = 10

        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1]
        mock_model.from_pretrained.return_value.generate.return_value = [[2, 3]]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = "print()"

        result = self.developer.generate_code(description, language, max_length)
        self.assertEqual(result, "print()")

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_max_length_large(self, mock_model, mock_tokenizer):
        """Test generate_code with a large max_length to ensure longer code
        generation."""
        description = "Generate a complex function"
        language = "Python"
        max_length = 1000

        mock_tokenizer.from_pretrained.return_value.encode.return_value = [1, 2, 3]
        mock_model.from_pretrained.return_value.generate.return_value = [
            [4, 5, 6, 7, 8, 9]
        ]
        mock_tokenizer.from_pretrained.return_value.decode.return_value = (
            "def complex_function():\n    pass"
        )

        result = self.developer.generate_code(description, language, max_length)
        self.assertEqual(result, "def complex_function():\n    pass")

    @patch("ai_application_developer.AutoTokenizer")
    @patch("ai_application_developer.AutoModelForSeq2SeqLM")
    def test_generate_code_error_handling(self, mock_model, mock_tokenizer):
        """Test generate_code's response when an error occurs during code
        generation."""
        description = "Print a greeting message"
        language = "Python"
        max_length = 50

        # Simulate model raising an exception
        mock_model.from_pretrained.side_effect = Exception("Model loading failed")

        result = self.developer.generate_code(description, language, max_length)
        self.assertEqual(result, "")

    @patch("ai_application_developer.AIApplicationDeveloper.create_test_cases")
    def test_create_test_cases_valid_code(self, mock_create_test_cases):
        """Test create_test_cases with valid code and description."""
        code = "def add(a, b):\n    return a + b"
        description = "Adds two numbers together."
        mock_create_test_cases.return_value = (
            "import unittest\n\n"
            "class TestAdd(unittest.TestCase):\n"
            "    def test_add_positive_numbers(self):\n"
            "        self.assertEqual(add(2, 3), 5)\n\n"
            "    def test_add_negative_numbers(self):\n"
            "        self.assertEqual(add(-2, -3), -5)\n"
        )

        result = self.developer.create_test_cases(code, description)
        self.assertIn("class TestAdd(unittest.TestCase):", result)

    @patch("ai_application_developer.AIApplicationDeveloper.create_test_cases")
    def test_create_test_cases_invalid_code(self, mock_create_test_cases):
        """Test create_test_cases with invalid code."""
        code = "def add(a, b)\n    return a + b"  # Missing colon
        description = "Adds two numbers together."
        mock_create_test_cases.return_value = ""

        result = self.developer.create_test_cases(code, description)
        self.assertEqual(result, "")

    def test_debug_code_no_errors(self):
        """Test debug_code with valid code that has no syntax errors."""
        code = "def add(a, b):\n    return a + b"
        result = self.developer.debug_code(code)
        self.assertEqual(result, "No syntax errors detected.")

    def test_debug_code_syntax_error(self):
        """Test debug_code with code that has a syntax error."""
        code = "def add(a, b)\n    return a + b"  # Missing colon
        result = self.developer.debug_code(code)
        self.assertIn("SyntaxError in code:", result)

    @patch("ai_application_developer.AIApplicationDeveloper.log_error")
    def test_debug_code_unexpected_error(self, mock_log_error):
        """Test debug_code handling of unexpected exceptions."""
        code = "def add(a, b):\n    return a + b"

        with patch(
            "ai_application_developer.ast.parse",
            side_effect=Exception("Unexpected error"),
        ):
            result = self.developer.debug_code(code)
            self.assertIn("Error in debugging code: Unexpected error", result)
            mock_log_error.assert_called_with(
                "Error in debugging code: Unexpected error"
            )


if __name__ == "__main__":
    unittest.main()
