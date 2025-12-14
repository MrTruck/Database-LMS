import streamlit as st
import streamlit as st
from data import get_connection
from auth import login_check
from helper import heading


login_check()
heading()

st.set_page_config(initial_sidebar_state=None, page_title="Courses", page_icon="📚")  # configure page title and icon


def course_card(title, instructor, course_id, instructorID):
    # Return just the HTML card without button
    return f"""
    <style>
        .course-card-{course_id} {{
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 10px;
            width: 100%;
            height: 180px;
            border: solid 1px #fff;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        }}
        .course-card-{course_id}:hover {{
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(255,255,255,0.2);
        }}
    </style>
    <div class="course-card-{course_id}">
        <span style="color: #d0daf5; padding:0; font-size: 16px;">
            Course {course_id}
        </span>
        <h5 style="margin: 0 0 5px 0;">{title}</h5>
        <div style="
            font-size:14px;
            color:#fff;
            font-family:monospace;
        ">
            {instructor} <span style="color:#d0daf5;">(iID {instructorID})</span>
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


def clickable_course_card(course, col):
    with col:
        container = st.container()

        with container:
            st.markdown(
                course_card(
                    course["courseName"],
                    course["instructorName"],
                    course["courseID"],
                    course["instructorID"],
                ),
                unsafe_allow_html=True,
            )

            # Invisible full-size button
            clicked = st.button(
                "Check Course",
                key=f"course_{course['courseID']}",
                use_container_width=True,
            )

        if clicked:
            st.session_state.selected_course = course["courseID"]
            st.switch_page("pages/course.py")


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
    courses = get_student_courses(st.session_state.student_id)
else:
    courses = get_courses()

for course in courses:
    if current_col == 0:
        clickable_course_card(course, col1)
        current_col = 1
    else:
        clickable_course_card(course, col2)
        current_col = 0


cursor.close()
conn.close()
