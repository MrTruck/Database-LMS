import streamlit as st
from data import get_connection
from auth import login_check
from helper import heading, course_header, display_time_24h

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
    SELECT sessionTitle, sessionDate, contentLink, sessionTime
    FROM Session
    WHERE courseID = %s
    ORDER BY sessionDate
""", (course_id,))

sessions = cursor.fetchall()

if st.session_state.logged_in == "student":
    enrolled_date_query = """
        SELECT enrollmentDate FROM enrollment
        WHERE courseID = %s
        AND studentID = %s
    """

    cursor.execute(enrolled_date_query, (course_id, st.session_state.student_id,))
    enrollment = cursor.fetchone()
    st.caption("Enrolled on " + str(enrollment["enrollmentDate"]))

cursor.close()
conn.close()

# ----------------------------
# Display sessions
# ----------------------------
st.subheader("Course Sessions")


for s_num, s in enumerate(sessions):
    with st.container(border=True):
        st.caption(f"Session {s_num+1}")
        st.markdown(f"**{s['sessionTitle']}**")
        col1, col2, col3 = st.columns([2,2,8])
        col1.caption(s['sessionDate'])
        col2.caption(display_time_24h(s['sessionTime']))
        col3.caption("")
        if s['contentLink']:
            content_links = str(s["contentLink"]).split()
            for link in content_links:
                st.markdown(f"**[{link}]({link})**")

# ----------------------------
# Back button
# ----------------------------
if st.button("← Back to Courses"):
    del st.session_state.selected_course
    st.switch_page("pages/courses.py")
