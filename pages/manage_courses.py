import streamlit as st
import streamlit as st
from auth import login_check, verify_instructor
from helper import heading
from pages.courses import course_card
from data import get_connection


def get_instructor_course(): # TODO: finish this function
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM Course c
        JOIN Instructor i ON c.instructorID = i.instructorID
        WHERE c.instructorID = %s
    """

    cursor.execute(query, )
    courses = cursor.fetchall()

    return courses


# Page code start
login_check()
verify_instructor()
heading()

st.markdown(course_card("yo", "lol", 10, 10), unsafe_allow_html=True)



