import streamlit as st
from auth import verify_pass


st.set_page_config(page_title="Login", page_icon="🔐")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

def login():
    st.title("🔐LMS User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_pass(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

def logout():
    st.session_state.logged_in = False   # student/instructor/False
    st.session_state.username = None
    st.session_state.user_id = None
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
