import streamlit as st
from data import get_connection
from auth import login_check
from helper import heading, course_header

selected_course = st.session_state.get("selected_course")

# determining title page
if selected_course:
    page_title = f"Course {selected_course}"
else:
    page_title = "Course"
st.set_page_config(page_title=page_title, page_icon="📚")  # configure page title and icon


login_check()
heading()

# ----------------------------
# Guard: no course selected
# ----------------------------
if "selected_course" not in st.session_state:
    st.error("No course selected.")
    if st.button("Back to courses"):
        st.switch_page("pages/courses.py")
    st.stop()

course_id = st.session_state.selected_course

# ----------------------------
# Fetch course info
# ----------------------------
conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT
        c.courseID, 
        c.courseName,
        i.instructorName,
        i.instructorID
    FROM Course c
    JOIN Instructor i ON c.instructorID = i.instructorID
    WHERE c.courseID = %s
""", (course_id,))

course = cursor.fetchone()

if not course:
    st.error("No course selected")
    st.stop()

course_header(course["courseID"], course["courseName"], course["instructorName"], course["instructorID"])

# ----------------------------
# Fetch sessions
# ----------------------------
cursor.execute("""
    SELECT sessionTitle, sessionDate, contentLink
    FROM Session
    WHERE courseID = %s
    ORDER BY sessionDate
""", (course_id,))

sessions = cursor.fetchall()

cursor.close()
conn.close()

# ----------------------------
# Display sessions
# ----------------------------
st.subheader("Course Sessions")

for s in sessions:
    with st.container(border=True):
        st.markdown(f"**{s['sessionTitle']}**")
        st.caption(s['sessionDate'])
        if s['contentLink']:
            st.markdown(f"[Attatchments]({s['contentLink']})")

# ----------------------------
# Back button
# ----------------------------
if st.button("← Back to Courses"):
    del st.session_state.selected_course
    st.switch_page("pages/courses.py")
