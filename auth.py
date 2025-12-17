import streamlit as st
from data import get_connection



def verify_pass(username: str, password: str):
    """
        Method to verify username & passowrd - 
        If valid change session state & redirect to courses; Invalid output st.error
    """
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
    """
        Method to check session_state for 'logged_in'-
        if not st.stop()
    """
    if "logged_in" not in st.session_state or not st.session_state.logged_in: # If not logged in
        st.error("🚫 You must log in first.")
        if st.button("Go to Login"):  # Output shortcut button to login
            st.switch_page("main.py")
        st.stop()


def verify_instructor():
    """
        Method to check whether user is instructor - 
        if not error message & st.stop()
    """
    if st.session_state.logged_in != "instructor":
        st.error("🚫 Instructor only feature")
        st.stop()

#
#
def initialize_role_id():
    """
        Method to identify role, to update sesion_state either student_id or instructor_id
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if (st.session_state.logged_in == 'student'):
        cursor.execute(
            """
            SELECT 
                studentID, majorName, semester
            FROM 
                student 
            WHERE 
                userID = %s;
            """, (st.session_state.user_id,)
        )
        student = cursor.fetchone()
        if student:
            st.session_state.student_id = student["studentID"]
            st.session_state.major = student["majorName"]
            st.session_state.semester = student["semester"]
        
    elif (st.session_state.logged_in == 'instructor'):
        cursor.execute(
            """
            SELECT instructorID, department FROM instructor
            WHERE
                userID = %s;
            """, (st.session_state.user_id,)
        )
        instructor = cursor.fetchone()
        if instructor:
            st.session_state.instructor_id = instructor["instructorID"]
            st.session_state.department = instructor["department"]
    
    cursor.close()
    conn.close()
