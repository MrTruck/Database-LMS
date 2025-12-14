import mysql.connector


# SQL connector METHOD
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="william",
        database="lms_database"
    )
