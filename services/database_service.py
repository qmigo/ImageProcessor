import mysql.connector
from mysql.connector import pooling
from exceptions.exceptions import DatabaseException
from constants.app_constants import AppConstants
from constants.queries import Queries  
from services.webhook_service import trigger_webhook
import os
from dotenv import load_dotenv

load_dotenv()

# Create a connection pool (adjust pool size as needed)
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),  # Convert port to integer
}
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name=AppConstants.DATABASE_POOL_NAME,
        pool_size=AppConstants.DATABASE_POOL_SIZE,  
        **db_config
    )
except mysql.connector.Error as e:
    raise DatabaseException(AppConstants.DATABASE_POOL_INITIALIZATION_FAILURE + str(e))


def get_db_connection():
    """Fetch a connection from the pool."""
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_CONNECTION_FAILURE + str(e))


def add_request(request_id, product_name, input_image_url):
    conn = None
    cursor = None
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
            conn.close()  # Returns connection to the pool


def update_request(request_id, product_name, input_image_url, output_image_url):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = Queries.UPDATE_REQUEST
        cursor.execute(query, (output_image_url, request_id, product_name, input_image_url))
        conn.commit()
        
        cursor.execute(Queries.CHECK_REQUEST_COMPLETION, (request_id,))
        remaining_images = cursor.fetchone()[0]  # Fetch count of pending images
        
        if remaining_images == 0:
            trigger_webhook(request_id)

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
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

        query = Queries.GET_REQUEST
        cursor.execute(query, (request_id,))  # Parameterized query

        return cursor.fetchall()
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_image_processor_request_table():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

        query = Queries.CREATE_IMAGE_PROCESSOR_REQUEST_TABLE
        cursor.execute(query)  # Parameterized query

    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_webhook_subscription_table():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

        query = Queries.CREATE_WEBHOOK_SUBSCRIPTION_TABLE
        cursor.execute(query)  # Parameterized query

    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    

def register_webhook(webhook_url, request_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

        query = Queries.INSERT_WEBHOOK_SUBSCRIPTION
        cursor.execute(query, (webhook_url, request_id))  # Parameterized query
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
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Fetch rows as dictionaries

        query = Queries.GET_WEBHOOK_FROM_REQUEST_ID
        cursor.execute(query, (request_id,))  # Parameterized query

        return cursor.fetchone()
    except mysql.connector.Error as e:
        raise DatabaseException(AppConstants.DATABASE_RETRIEVAL_ERROR + str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
