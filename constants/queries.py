class Queries:
    INSERT_REQUEST = """
        INSERT INTO image_processor_request 
        (request_id, product_name, input_image_url, is_completed)
        VALUES (%s, %s, %s, %s)
    """

    UPDATE_REQUEST = """
        UPDATE image_processor_request
        SET output_image_url = %s, is_completed = 'Y'
        WHERE request_id = %s
        AND product_name = %s
        AND input_image_url = %s
    """

    GET_REQUEST = """
        SELECT * FROM image_processor_request WHERE request_id = %s
    """

    CREATE_IMAGE_PROCESSOR_REQUEST_TABLE = """
        CREATE TABLE IF NOT EXISTS image_processor_request (
        id INT AUTO_INCREMENT PRIMARY KEY,
        request_id VARCHAR(40) NOT NULL,
        product_name VARCHAR(255) NOT NULL,
        input_image_url VARCHAR(2083) NOT NULL,
        output_image_url VARCHAR(2083),
        is_completed VARCHAR(1) DEFAULT '1'
    )
    """

    CREATE_WEBHOOK_SUBSCRIPTION_TABLE = """
        CREATE TABLE IF NOT EXISTS webhook_subscription
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            webhook_url VARCHAR(2083) NOT NULL,
            request_id VARCHAR(40) NOT NULL
        )
    """

    INSERT_WEBHOOK_SUBSCRIPTION = """
        INSERT INTO webhook_subscription
        (webhook_url, request_id)
        VALUES (%s, %s)
    """

    GET_WEBHOOK_FROM_REQUEST_ID = """
        SELECT webhook_url FROM webhook_subscription
        WHERE request_id = %s
        """
    
    CHECK_REQUEST_COMPLETION = """
        select count(*) from image_processor_request
        where request_id = %s and is_completed = 'N'
    """