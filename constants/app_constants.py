class AppConstants:
    FILE_NOT_FOUND_EXCEPTION_MSG = 'File is missing from request'
    PRODUCT_NAME_PARAMETER = 'Product Name'
    INPUT_IMAGE_URLS_PARAMETER = 'Input Image Urls'
    INVALID_CSV_EXCEPTION = 'Uploaded CSV file is not following the validations'
    EMPTY_CSV_FILE_EXCEPTION = 'Uploaded CSV file is empty'
    PARSING_CSV_EXCEPTION = 'Uploaded CSV file is not properly formatted'
    DATABASE_CONNECTION_FAILURE = 'Failed to get a database connection'
    DATABASE_POOL_INITIALIZATION_FAILURE = 'Failed to initialize connection pool'
    DATABASE_INSERTION_ERROR = 'Error inserting request'
    DATABASE_UPDATE_ERROR = 'Error updating request'
    DATABASE_RETRIEVAL_ERROR = 'Error retrieving request'
    IMAGE_COMPRESSION_FORMAT = 'jpeg'
    IMAGE_COMPRESS_RATIO = 50
    DATABASE_POOL_NAME = 'mypool'
    DATABASE_POOL_SIZE = 10