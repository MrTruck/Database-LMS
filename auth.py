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

    cursor.execute(
        "SELECT userID, email, password, fullName AS name, role "
        "FROM user WHERE email=%s",
        (username,)
    )
    user = cursor.fetchone()

    if user:
        if password == user['password']:
            
            st.success(f"Logged in successfully as: {user['name']}")
            
            st.session_state.logged_in = user["role"]
            st.session_state.user_id = user["userID"]
            st.session_state.username = user["name"]
            
            cursor.close()
            conn.close()
            
            initialize_role_id()
            st.switch_page("pages/courses.py")
            return

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


def initialize_role_id():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if (st.session_state.logged_in == 'student'):
        cursor.execute(
            """
            SELECT 
                studentID 
            FROM 
                student 
            WHERE 
                userID = %s;
            """, (st.session_state.user_id,)
        )
        student = cursor.fetchone()
        if student:
            st.session_state.student_id = student["studentID"]
        
    elif (st.session_state.logged_in == 'instructor'):
        cursor.execute(
            """
            SELECT instructorID FROM instructor
            WHERE
                userID = %s;
            """, (st.session_state.user_id,)
        )
        instructor = cursor.fetchone()
        if instructor:
            st.session_state.instructor_id = instructor["instructorID"]
    

    cursor.close()
    conn.close()