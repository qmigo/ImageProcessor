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
