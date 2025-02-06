import logging
import re
from typing import List

import pandas as pd
from great_expectations.dataset import PandasDataset

# Configure logging to save errors to 'error_logs.log'
logging.basicConfig(
    filename="error_logs.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class EthicalDataset(PandasDataset):
    """A dataset class for performing ethical validations on the data.

    Inherits from Great Expectations' PandasDataset.
    """

    def validate_biased_language(self) -> List[str]:
        """Identifies potential use of biased language in the dataset using
        regular expressions.

        Returns:
            List[str]: A list of problematic words or phrases found in the text.
        """
        biased_phrases = [
            r"\bhe\b",
            r"\bshe\b",
            r"\bhis\b",
            r"\bher\b",  # Gender bias
            r"\bmankind\b",
            r"\bhe/she\b",
            r"\boy\b",
            r"\bgirl\b",  # Other biases
        ]
        problematic_phrases = []
        try:
            for column in self.columns:
                for phrase in biased_phrases:
                    matches = (
                        self[column]
                        .astype(str)
                        .str.findall(phrase, flags=re.IGNORECASE)
                    )
                    for match_list in matches:
                        if match_list:
                            problematic_phrases.extend(match_list)
            return problematic_phrases
        except Exception as e:
            logging.error(f"Error in validate_biased_language: {e}")
            return []

    def validate_sensitive_data(self) -> List[str]:
        """Detects the presence of sensitive data such as email addresses and
        phone numbers.

        Returns:
            List[str]: A list of columns containing sensitive data.
        """
        sensitive_patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "phone_number": r"(\+\d{1,2}\s?)?1?\-?\s?(\d{3}[\-.\s]?){2}\d{4}",
        }
        sensitive_columns = []
        try:
            for column in self.columns:
                for data_type, pattern in sensitive_patterns.items():
                    if (
                        self[column]
                        .astype(str)
                        .str.contains(pattern, regex=True, na=False)
                        .any()
                    ):
                        sensitive_columns.append(column)
                        break  # Avoid duplicate entries for the same column
            return sensitive_columns
        except Exception as e:
            logging.error(f"Error in validate_sensitive_data: {e}")
            return []


def log_error(message: str) -> None:
    """Logs error messages to the 'error_logs.log' file.

    Parameters:
        message (str): The error message to log.
    """
    logging.error(message)


def validate_ethical_requirements(file_path: str) -> bool:
    """Validates the ethical requirements of the given data file.

    Parameters:
        file_path (str): The path to the data file to validate.

    Returns:
        bool: True if all ethical requirements are met, False otherwise.
    """
    try:
        # Step 1: Load the data into a Pandas DataFrame
        df = pd.read_csv(file_path)
        dataset = EthicalDataset(df)

        # Step 2: Validate biased language
        biased_language = dataset.validate_biased_language()
        if biased_language:
            logging.warning(f"Biased language detected: {biased_language}")

        # Step 3: Validate sensitive data
        sensitive_data = dataset.validate_sensitive_data()
        if sensitive_data:
            logging.warning(f"Sensitive data found in columns: {sensitive_data}")

        # Step 4: Determine if all ethical requirements are met
        all_compliant = not biased_language and not sensitive_data

        # Step 5: Generate report
        with open("ethical_validation_report.txt", "w") as report:
            report.write("Ethical Validation Report\n")
            report.write("=========================\n\n")
            report.write(
                f"Biased Language Found: {biased_language if biased_language else 'None'}\n"
            )
            report.write(
                f"Sensitive Data Found in Columns: {sensitive_data if sensitive_data else 'None'}\n"
            )
            report.write(
                f"Overall Compliance: {'Passed' if all_compliant else 'Failed'}\n"
            )

        return all_compliant

    except FileNotFoundError:
        log_error(f"File not found: {file_path}")
        return False
    except pd.errors.EmptyDataError:
        log_error(f"No data: {file_path} is empty.")
        return False
    except Exception as e:
        log_error(f"Unexpected error during validation: {e}")
        return False
