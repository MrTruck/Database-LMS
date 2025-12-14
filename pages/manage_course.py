import streamlit as st
from data import get_connection
from auth import login_check, verify_instructor
from helper import heading, course_header


login_check()
verify_instructor()
heading()

st.set_page_config(page_title="Course Management", page_icon="📚")  # configure page title and icon

if not st.session_state.manage_course:
    st.error("No course selected")
    st.stop()


conn = get_connection()
cursor = conn.cursor(dictionary=True)

course_query = """
                SELECT * FROM Course c
                JOIN Instructor i ON i.instructorID = c.instructorID
                WHERE courseID = %s
            """

cursor.execute(course_query, (st.session_state.manage_course,))
course_obj = cursor.fetchone()


course_session_query = """
                        SELECT * FROM Session
                        WHERE courseID = %s
                    """

cursor.execute(course_session_query, (st.session_state.manage_course,))
course_sessions = cursor.fetchall()


course_header(course_obj["courseID"], course_obj["courseName"], course_obj["instructorName"], course_obj["instructorID"])


for s in course_sessions:
    with st.container(border=True):
        st.markdown(f"**{s['sessionTitle']}**")
        st.caption(s['sessionDate'])

        # Editable text input
        new_link = st.text_input(
            "Attachment Link",
            value=s["contentLink"] or "",
            key=f"content_link_{s['sessionID']}"
        )

        # Save button per session
        if st.button(
            "Save",
            key=f"save_session_{s['sessionID']}"
        ):
            update_query = """
                UPDATE Session
                SET contentLink = %s
                WHERE sessionID = %s
            """
            cursor.execute(update_query, (new_link, s["sessionID"]))
            conn.commit()
            st.success("Attachment link updated")


cursor.close()
conn.close()
