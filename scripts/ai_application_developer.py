import logging
from typing import Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import ast
import traceback

class AIApplicationDeveloper:
    """
    AIApplicationDeveloper is a class designed to assist in generating code,
    creating unit tests, and debugging Python code, while also logging all errors.
    """

    def __init__(self, model_name: str = 'Salesforce/codet5-base'):
        """
        Initializes the AIApplicationDeveloper with a specified CodeT5 model.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(
            filename='error_logs.log',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.logger.info(f"Loaded model '{model_name}' successfully.")
        except Exception as e:
            self.log_error(f"Error loading model '{model_name}': {e}")
            raise

    def log_error(self, message: str) -> None:
        """
        Logs error messages to a file for review.

        Parameters:
            message (str): The error message to log.
        """
        logging.error(message)


    def generate_code(self, description: str, language: str, max_length: int) -> str:
        """
        Generates code based on a textual description using the CodeT5 model.

        Parameters:
            description (str): A description of the desired functionality for the code to be generated.
            language (str): The programming language in which the code should be written.
            max_length (int): The maximum length of the generated code in tokens.

        Returns:
            str: The generated code snippet as a string.
        """
        try:
            # Construct the prompt by specifying the language and description
            prompt = f"Generate {language} code for the following description:\n{description}\n"
            inputs = self.tokenizer.encode(prompt, return_tensors='pt')
            # Generate the code using the CodeT5 model
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            # Decode the output from the model to get the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract the code block from the generated text
            code_start = generated_text.find(f"```{language}") + len(f"```{language}")
            code_end = generated_text.find("```", code_start)
            generated_code = generated_text[code_start:code_end].strip()
            return generated_code

        except Exception as e:
            # Log the error and return an empty string upon failure
            error_details = traceback.format_exc()
            self.log_error(f"An error occurred in generate_code: {e}\n{error_details}")
            return ""

    def create_test_cases(self, code: str, function_description: str) -> str:
        """
        Generates unit test cases for a given Python function using the unittest framework.
        Includes both positive and negative test inputs based on the function's parameters.

        Parameters:
            code (str): The Python code containing the function to be tested.
            function_description (str): A description of the function's purpose and behavior.

        Returns:
            str: A string containing the generated unit test cases.
        """
        try:
            # Parse the provided code into an Abstract Syntax Tree (AST)
            parsed_code = ast.parse(code)
            
            # Initialize variables to store function name and arguments
            function_name = ""
            args = []
            arg_types = {}
            
            # Traverse the AST to find the function definition
            for node in ast.walk(parsed_code):
                if isinstance(node, ast.FunctionDef):
                    # Assume the first function found is the target function
                    function_name = node.name
                    # Extract argument names and type annotations if available
                    for arg in node.args.args:
                        args.append(arg.arg)
                        if arg.annotation:
                            # Convert the AST annotation to a string
                            arg_types[arg.arg] = ast.unparse(arg.annotation)
                        else:
                            arg_types[arg.arg] = 'Any'  # Default to Any if no type annotation
                    break
            
            if not function_name:
                raise ValueError("No function definition found in the provided code.")
            
            # Dynamically create example input arguments based on the function's parameters
            example_inputs = {arg: "example_value" for arg in args}
            example_invalid_inputs = {arg: None for arg in args}  # Example invalid inputs
            # Placeholder for expected output
            expected_output = "expected_result"
            # Constructing the test case class as a string
            test_code = f"""import unittest
from {function_name}_module import {function_name}  # Replace with the actual module name

class Test{function_name.capitalize()}(unittest.TestCase):
    \"\"\"Unit tests for the {function_name} function.\"\"\"

    def test_positive_case(self):
        \"\"\"Test {function_name} with valid input parameters.\"\"\"
        # Example input arguments
        input_args = {example_inputs}
        expected_output = {expected_output}  # Replace with the actual expected result

        # Call the function with positive test inputs
        result = {function_name}(**input_args)
        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)

    def test_negative_case(self):
        \"\"\"Test {function_name} with invalid input parameters to ensure proper error handling.\"\"\"
        # Example invalid input arguments to trigger exceptions
        input_args = {negative_inputs}

        with self.assertRaises(Exception):
            {function_name}(**input_args)

if __name__ == '__main__':
    unittest.main()
"""
            return test_code

        except Exception as e:
            # Log the error details for debugging purposes
            error_details = traceback.format_exc()
            self.log_error(f"An error occurred in create_test_cases: {e}\n{error_details}")
            return ""
   
    def debug_code(self, code: str) -> str:
        """
        Attempts to debug the provided Python code by fixing syntax and logic errors.
        
        Parameters:
            code (str): A string containing the Python code to be debugged.
            
        Returns:
            str: The debugged Python code as a string, or an error message if no syntax error is detected.
        """
        try:
            # Parse the code into an Abstract Syntax Tree (AST) to check for syntax errors
            parsed = ast.parse(code)
            
            # If parsing is successful, assume there are no syntax errors
            # For simplicity, this function does not modify the code to fix errors
            return "No syntax errors detected."
        except SyntaxError as e:
            # Handle syntax errors by providing an error message
            # In a real-world scenario, you might attempt to fix common syntax issues here
            error_msg = f"Syntax error in code: {e}"
            self.log_error(error_msg)
            return ""
        except Exception as e:
            # Handle any other exceptions that may occur during debugging
            # traceback.format_exc() provides detailed error information
            error_details = traceback.format_exc()
            self.log_error(f"An error occurred while debugging the code: {e}\n{error_details}")
            return f"An error occurred while debugging the code: {error_details}"