import pandas as pd
from werkzeug.datastructures import FileStorage
from exceptions.exceptions import InvalidCSVException
from constants.app_constants import AppConstants


def process_file(file_payload: FileStorage) -> list:
    try:
        df = pd.read_csv(file_payload)
        
        if not validate_csv(df):
            raise InvalidCSVException(AppConstants.INVALID_CSV_EXCEPTION)

        products = df.head().to_dict(orient='records')
        return products

    except pd.errors.EmptyDataError:
        raise InvalidCSVException(AppConstants.EMPTY_CSV_FILE_EXCEPTION)
    
    except pd.errors.ParserError:
        raise InvalidCSVException(AppConstants.PARSING_CSV_EXCEPTION)

    except Exception as e:
        raise InvalidCSVException(f"An error occurred while processing the CSV: {str(e)}")


def validate_csv(df)-> bool:
    required_columns = {AppConstants.PRODUCT_NAME_PARAMETER, AppConstants.INPUT_IMAGE_URLS_PARAMETER}
    return required_columns.issubset(set(df.columns))
        
