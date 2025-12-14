import streamlit as st
import streamlit as st
from auth import login_check, verify_instructor
from helper import heading
from pages.courses import course_card
from data import get_connection


def get_instructor_courses():
    """
        Returns dict containing courses the instructor instructs 
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM Course c
        JOIN Instructor i ON c.instructorID = i.instructorID
        WHERE c.instructorID = %s
    """

    cursor.execute(query, (st.session_state.instructor_id,))
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses


# Page code starter
login_check()
verify_instructor()
heading()

st.set_page_config(page_title="Course Management", page_icon="📚")  # configure page title and icon


for instructor_course in get_instructor_courses():
    row_col1, row_col2 = st.columns([3, 1])

    with row_col1:
        st.markdown(
            course_card(
                instructor_course["courseName"],
                instructor_course["instructorName"],
                instructor_course["courseID"],
                instructor_course["instructorID"]
            ),
            unsafe_allow_html=True
        )

    with row_col2:
        st.markdown("""
        <style>
        div.stButton > button {
            height: 150px;
            width: 100%;
            border-radius: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

        clicked = st.button(
            "Manage Course",
            key=f"manage_course_{instructor_course['courseID']}", # TODO link button to course management
            use_container_width=True
        )
        if clicked:
            st.session_state.manage_course = instructor_course["courseID"]
            st.switch_page("pages/manage_course.py")
