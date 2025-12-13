import streamlit as st
from auth import verify_pass, initialize_role_id


st.set_page_config(page_title="Login", page_icon="🔐")

# Available session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.student_id = None
    st.session_state.instructor_id = None
    st.session_state.selected_course = None


def login():
    st.title("🔐 LMS User Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if verify_pass(email, password):
                st.success("Login successful!")
            else:
                st.error("Invalid email or password.")

def logout():
    st.session_state.logged_in = False   # student/instructor/False
    st.session_state.username = None
    st.session_state.user_id = None
    st.session_state.instructor_id = None
    st.session_state.student_id = None
    st.rerun()

# Page Logic
if not st.session_state.logged_in:
    login()
else:
    st.title(f"Welcome, {st.session_state.username} 👋")
    st.write("You are logged in!")

    if st.button("Go to courses"):
        st.switch_page("pages\courses.py")

    if st.button("Logout"):
        logout()
