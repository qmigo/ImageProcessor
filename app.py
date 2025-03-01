from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        user='21YmjuJeBcuBTgR.root',
        password='7xfC0BJo2Iabph2I',
        database='public',
        port=4000
    )
    return connection

@app.route('/upload', methods=['POST'])
def upload_file():
    file_payload = request.files.get('file', None)
    if not file_payload:
        return "File Payload is missing, check if key is set to file"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("select * from user")
    users = cursor.fetchall()
    print(users)

    return "hi"

if __name__ == '__main__':
    app.run(debug=True, port=5500)