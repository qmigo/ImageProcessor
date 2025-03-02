import pandas as pd
from werkzeug.datastructures import FileStorage
from exceptions.exceptions import InvalidCSVException
from constants.app_constants import AppConstants

def process_file(file_payload: FileStorage) -> list:
    """
    Processes a CSV file and converts it into a list of dictionaries.

    Args:
        file_payload (FileStorage): The uploaded CSV file.

    Returns:
        list: A list of dictionaries representing product data.

    Raises:
        InvalidCSVException: If the CSV file is empty, invalid, or cannot be parsed.
    """
    try:
        df = pd.read_csv(file_payload)  # Read CSV file into DataFrame

        # Validate CSV structure before processing
        if not validate_csv(df):
            raise InvalidCSVException(AppConstants.INVALID_CSV_EXCEPTION)

        return df.to_dict(orient='records')  # Convert DataFrame to list of dictionaries

    except pd.errors.EmptyDataError:
        raise InvalidCSVException(AppConstants.EMPTY_CSV_FILE_EXCEPTION)  # Handle empty CSV files
    
    except pd.errors.ParserError:
        raise InvalidCSVException(AppConstants.PARSING_CSV_EXCEPTION)  # Handle CSV parsing errors

    except Exception as e:
        raise InvalidCSVException(f"An error occurred while processing the CSV: {str(e)}")


def validate_csv(df) -> bool:
    """
    Validates whether the required columns exist in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        bool: True if the required columns are present, otherwise False.
    """
    required_columns = {AppConstants.PRODUCT_NAME_PARAMETER, AppConstants.INPUT_IMAGE_URLS_PARAMETER}
    return required_columns.issubset(set(df.columns))  # Check if required columns exist
