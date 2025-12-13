import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="william",
        database="lms_database"
    )

fake_courses = {}