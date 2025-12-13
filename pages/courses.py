import streamlit as st
import streamlit as st
from data import get_connection
from auth import login_check
from helper import heading


login_check()
heading()


def course_card(title, instructor, course_id, instructorID):
    # Include an HTML link-button that navigates by setting a query parameter
    return f"""
    <div style="
        padding: 10px 0;
        border-radius: 6px;
        margin-bottom: 10px;
        width: 100%;
        height:150px;
        border: solid 1px #fff;
        padding: 15px;
    ">
        <h5 style="margin: 0 0 5px 0;">{title}</h4>
        <div style="
            font-size:14px;
            color:#fff;
            font-family:monospace;
        ">
            {instructor} <span style="color:#17fc03;">[iID {instructorID}]</span>
        </div>
        <div style="margin-top:10px;">
            <a href="?selected_course={course_id}" target="_self" style="text-decoration:none;">
                <button style="background:#007bff;color:#fff;border:none;padding:8px 12px;border-radius:4px;cursor:pointer;">
                    Check course
                </button>
            </a>
        </div>
    </div>
    """


def get_student_courses(student_id):
    """
    Retrieve all courses a student is enrolled in.
    Args:
        student_id (int): Student.studentID
    Returns:
        list[dict]: List of courses with courseID, courseName, instructorName
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            c.courseID,
            c.courseName,
            i.instructorName,
            i.instructorID
        FROM Enrollment e
        JOIN Course c ON e.courseID = c.courseID
        JOIN Instructor i ON c.instructorID = i.instructorID
        WHERE e.studentID = %s
    """
    cursor.execute(query, (student_id,))
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses


def get_courses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM Course c
        JOIN Instructor i ON c.instructorID = i.instructorID
    """

    cursor.execute(query, )
    courses = cursor.fetchall()

    return courses


# If a course was selected via query param, navigate to its page
params = st.query_params
if "selected_course" in params:
    sc = params["selected_course"]
    st.session_state.selected_course = sc
    # clear params then switch page
    st.query_params.clear()
    st.switch_page("pages/course.py")


col1, col2 = st.columns(2)
current_col = 0

conn = get_connection()
cursor = conn.cursor()


if st.session_state.logged_in == "student":
    student_courses = get_student_courses(st.session_state.student_id)
    for course in student_courses:
        button_key = f"check_course_{course['courseID']}"

        if current_col == 0:
            with col1:
                st.markdown(course_card(course["courseName"], course["instructorName"], course["courseID"], course["instructorID"]),
                            unsafe_allow_html=True)
            current_col = 1
        else:
            with col2:
                st.markdown(course_card(course["courseName"], course["instructorName"], course["courseID"], course["instructorID"]),
                            unsafe_allow_html=True)
            current_col = 0


elif st.session_state.logged_in == "instructor":
    courses = get_courses()

    for course in courses:
        button_key = f"check_course_{course['courseID']}"

        if current_col == 0:
            with col1:
                st.markdown(course_card(course["courseName"], course["instructorName"], course["courseID"], course["instructorID"]),
                            unsafe_allow_html=True)
            current_col = 1
        else:
            with col2:
                st.markdown(course_card(course["courseName"], course["instructorName"], course["courseID"], course["instructorID"]),
                            unsafe_allow_html=True)
            current_col = 0


cursor.close()
conn.close()
