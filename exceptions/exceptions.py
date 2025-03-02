class InvalidCSVException(Exception):
    """Custom exception for invalid CSV files."""
    
    def __init__(self, message: str):
        super().__init__(message)  

class FileNotFoundException(Exception):
    """Custom exception for files not found."""
    
    def __init__(self, message: str):
        super().__init__(message)  


class DatabaseException(Exception):
    """Custom exception for database errors."""
    def __init__(self, message):
        super().__init__(message)


class ImageProcessingException(Exception):
    """Custom exception for database errors."""
    def __init__(self, message):
        super().__init__(message)

class InvalidRequestException(Exception):
    """Custom exception for database errors."""
    def __init__(self, message):
        super().__init__(message)

class WebHookNotFoundException(Exception):
    """Webhook exception"""
    def __init__(self, message):
        super().__init__(message)