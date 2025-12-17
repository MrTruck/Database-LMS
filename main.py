import streamlit as st
from auth import verify_pass



st.set_page_config(page_title="Login", page_icon="🔐")

# Available session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False   # False / student/ instructor
    st.session_state.username = None
    st.session_state.student_id = None
    st.session_state.instructor_id = None
    st.session_state.selected_course = None
    st.session_state.manage_course = None
    st.session_state.major = None
    st.session_state.semester = None
    st.session_state.department = None


def login():
    """
        Renders the login page form
    """
    st.title("🔐 LMS User Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            verify_pass(email, password)

def logout():
    """
        Resets all session states to default values
    """
    st.session_state.logged_in = False   # False / student/ instructor
    st.session_state.username = None
    st.session_state.student_id = None
    st.session_state.instructor_id = None
    st.session_state.selected_course = None
    st.session_state.manage_course = None
    st.session_state.major = None
    st.session_state.semester = None
    st.session_state.department = None
    st.rerun()


if not st.session_state.logged_in: # Not logged in
    login()
else:   # logged in
    st.title(f"Welcome, {st.session_state.username} 👋")
    st.write("You are logged in!")

    if st.button("Go to courses"):
        st.switch_page("pages/courses.py")

    if st.button("Logout"):
        logout()
