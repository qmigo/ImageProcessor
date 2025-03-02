import mysql.connector
from mysql.connector import pooling
from exceptions.exceptions import DatabaseException
from constants.app_constants import AppConstants
from constants.queries import Queries  
from services.webhook_service import trigger_webhook
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
# Using connection pooling to optimize database connections

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),  # Convert port to integer
}

try:
    # Create a connection pool to reuse database connections
    connection_pool = pooling.MySQLConnectionPool(
        pool_name=AppConstants.DATABASE_POOL_NAME,
        pool_size=AppConstants.DATABASE_POOL_SIZE,  
        **db_config
    )
except mysql.connector.Error as e:
    raise DatabaseException(AppConstants.DATABASE_POOL_INITIALIZATION_FAILURE + str(e))


def get_db_connection():
    """Fetch a connection from the database connection pool."""
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_CONNECTION_FAILURE + str(e))


def add_request(request_id, product_name, input_image_url):
    """Insert a new request into the database."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = Queries.INSERT_REQUEST
        cursor.execute(query, (request_id, product_name, input_image_url, 'N'))
        conn.commit()
        
        return request_id
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        raise DatabaseException(AppConstants.DATABASE_INSERTION_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_request(request_id, product_name, input_image_url, output_image_url):
    """Update request with the processed image output URL and trigger webhook if all images are processed."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = Queries.UPDATE_REQUEST
        cursor.execute(query, (output_image_url, request_id, product_name, input_image_url))
        conn.commit()
        
        # Check if all images are processed
        cursor.execute(Queries.CHECK_REQUEST_COMPLETION, (request_id,))
        remaining_images = cursor.fetchone()[0]
        
        if remaining_images == 0:
            trigger_webhook(request_id)  # Trigger webhook if all images are processed
        
        return True
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        raise DatabaseException(AppConstants.DATABASE_UPDATE_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_request(request_id):
    """Retrieve request details from the database."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries
        
        query = Queries.GET_REQUEST
        cursor.execute(query, (request_id,))
        
        return cursor.fetchall()
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_image_processor_request_table():
    """Create the table for storing image processing requests."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = Queries.CREATE_IMAGE_PROCESSOR_REQUEST_TABLE
        cursor.execute(query)
        
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_webhook_subscription_table():
    """Create the table for storing webhook subscriptions."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = Queries.CREATE_WEBHOOK_SUBSCRIPTION_TABLE
        cursor.execute(query)
        
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def register_webhook(webhook_url, request_id):
    """Register a webhook URL for a specific request."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = Queries.INSERT_WEBHOOK_SUBSCRIPTION
        cursor.execute(query, (webhook_url, request_id))
        conn.commit()
        
        return True
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        raise DatabaseException(AppConstants.DATABASE_INSERTION_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_webhook(request_id):
    """Retrieve the webhook URL for a given request ID."""
    conn, cursor = None, None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = Queries.GET_WEBHOOK_FROM_REQUEST_ID
        cursor.execute(query, (request_id,))
        
        return cursor.fetchone()
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
