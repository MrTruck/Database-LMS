import streamlit as st


def heading():
    """Render heading of user name & student/instructor id"""
    if (st.session_state.logged_in == "student"):
        id_display = str(st.session_state.student_id)
    else:
        id_display = str(st.session_state.instructor_id)

    html = f"""
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e0e0e0; padding:6px 0;">
      <div style="font-size:25px; font-weight:600;">Hello, {st.session_state.username}!</div>
      <div style="font-size:21px; color:#666;">{st.session_state.logged_in} ID: {id_display}</div>
    </div>
    <br>
    """

    st.markdown(html, unsafe_allow_html=True)

def course_header(course_id, course_name, instructor_name, instructorID):
    """
        Render heading for individual courses
    """
    st.markdown(f'''<span style="color: #fff; padding:0; font-size: 18px; margin: 0;">
            Course {course_id}
        </span>''', unsafe_allow_html=True)
    st.title(course_name)
    st.caption(f"Instructor: {instructor_name} (ID {instructorID})")
    st.divider()
