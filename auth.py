import bcrypt
import streamlit as st
from data import get_connection

# Fake users (replace with DB later)
users = {
    "teacher": bcrypt.hashpw("teach123".encode(), bcrypt.gensalt()),
    "student": bcrypt.hashpw("student123".encode(), bcrypt.gensalt()),
}

def verify_pass(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ---- Check Student table ----
    cursor.execute(
        "SELECT studentID AS id, studentName AS name "
        "FROM Student WHERE studentName=%s AND password=%s",
        (username, password)
    )
    student = cursor.fetchone()

    if student:
        st.success(f"Logged in as Student: {student['name']}")
        st.session_state.logged_in = "student"
        st.session_state.user_id = student["id"]
        st.session_state.username = student["name"]
        cursor.close()
        conn.close()
        st.switch_page("pages/courses.py")
        return

    # ---- Check Instructor table ----
    cursor.execute(
        "SELECT instructorID AS id, instructorName AS name "
        "FROM Instructor WHERE instructorName=%s AND password=%s",
        (username, password)
    )
    instructor = cursor.fetchone()

    if instructor:
        st.success(f"Logged in as Instructor: {instructor['name']}")
        st.session_state.logged_in = "instructor"
        st.session_state.user_id = instructor["id"]
        st.session_state.username = instructor["name"]
        cursor.close()
        conn.close()
        st.switch_page("pages/courses.py")
        return

    # ---- If not found ----
    cursor.close()
    conn.close()
    st.error("Invalid username or password. Please try again.")


def login_check():
    # If not logged in
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("🚫 You must log in first.")
        if st.button("Go to Login"):
            st.switch_page("main.py")
        st.stop()

def verify_instructor():
    if st.session_state.logged_in != "instructor":
        st.error("🚫 Instructor only feature")
        st.stop()