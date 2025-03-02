from flask import jsonify
from werkzeug.exceptions import NotFound
from exceptions.exceptions import (
    InvalidCSVException,
    FileNotFoundException,
    DatabaseException,
    ImageProcessingException,
    InvalidRequestException
)

def register_error_handlers(app):
    """Registers global error handlers in Flask."""
    
    @app.errorhandler(InvalidCSVException)
    def handle_invalid_csv_exception(error):
        response = {
            "error": "Invalid CSV File",
            "message": str(error)
        }
        return jsonify(response), 400

    @app.errorhandler(FileNotFoundException)
    def handle_file_not_found_exception(error):
        response = {
            "error": "File Not Found",
            "message": str(error)
        }
        return jsonify(response), 404

    @app.errorhandler(DatabaseException)
    def handle_database_exception(error):
        response = {
            "error": "Database Error",
            "message": str(error)
        }
        return jsonify(response), 500

    @app.errorhandler(ImageProcessingException)
    def handle_image_processing_exception(error):
        response = {
            "error": "Image Processing Error",
            "message": str(error)
        }
        return jsonify(response), 500

    @app.errorhandler(InvalidRequestException)
    def handle_invalid_request_exception(error):
        response = {
            "error": "Request validation error",
            "message": "The request id could not be found or is not valid."
        }
        return jsonify(response), 404
    
    @app.errorhandler(InvalidRequestException)
    def handle_missing_webhook_exception(error):
        response = {
            "error": "WebHook error",
            "message": "The web hook url could not be found or is not valid."
        }
        return jsonify(response), 404
    
    @app.errorhandler(NotFound)
    def handle_404_exception(error):
        """Handles 404 errors when a route is not found."""
        response = {
            "error": "Not Found",
            "message": "The requested resource could not be found."
        }
        return jsonify(response), 404
    

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handles any unexpected internal server errors (500)."""
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
        return jsonify(response), 500
