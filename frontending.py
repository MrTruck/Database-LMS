import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

#DATABASE SETUP---------------------------------------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="${A3NdE(z*Vju<6Q",
    database="lms"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
""")

#Create default admin if not exists
cur.execute("SELECT * FROM users WHERE username='admin'")
if cur.fetchone() is None:
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                ('admin', 'admin', 'admin'))
    conn.commit()

#Create default student 
cur.execute("SELECT * FROM users WHERE username='student'")
if cur.fetchone() is None:
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                ('student', 'student', 'student'))
    conn.commit()


root = tk.Tk()
root.title("LMS")
root.geometry("500x350")


#Clear page function
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()



#LOGIN SCREEN---------------------------------------------------------------------------

def login_screen():
    clear_frame(root)

    tk.Label(root, text="LMS Login", font=("Arial", 18)).pack(pady=20)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    

    def login():
        username = username_entry.get()
        password = password_entry.get()

        cur.execute("SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password))
        result = cur.fetchone()

        if result:
            role = result[0]
            if role == "admin":
                admin_dashboard()
            else:
                student_dashboard(username)
        else:
            messagebox.showerror("Error", "Username or Password Was Not Found")

    tk.Button(root, text="Login", command=login).pack(pady=15)

    tk.Button(root, text="Register", command=register_screen).pack(pady=5)

#REGISTER SCREEN---------------------------------------------------------------------------

def register_screen():
    clear_frame(root)
    tk.Label(root, text="LMS Registration", font=("Arial", 18)).pack(pady=20)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Fullname").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Email").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Label(root, text="Confirm Password").pack()
    passwordConfirm_entry = tk.Entry(root, show="*")
    passwordConfirm_entry.pack()

    def register(): #Assuming only student can register and admins go through a different channel
        username = username_entry.get()
        password = password_entry.get()
        password_confirm = passwordConfirm_entry.get()
        role = "student"

        #Simple validation
        if not username or not password or role not in ("admin", "student"):
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return
        elif password_confirm != password :
            messagebox.showerror("Error", "Confirm password does not match password")
            return


        try:
            cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            login_screen()

        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
    tk.Button(root, text="Register", command=register).pack(pady=10)
    tk.Button(root, text="Back to Login", command=login_screen).pack(pady=20)

#ADMIN DASHBOARD---------------------------------------------------------------------------

def admin_dashboard():
    clear_frame(root)

    tk.Label(root, text="Admin Dashboard", font=("Arial", 18)).pack(pady=10)

    #Add course 
    tk.Label(root, text="Add New Course").pack()
    course_entry = tk.Entry(root)
    course_entry.pack()

    def add_course():
        course = course_entry.get()
        if course:
            cur.execute("INSERT INTO courses (name) VALUES (%s)", (course,))
            conn.commit()
            messagebox.showinfo("Success", "Course added!")
        else:
            messagebox.showerror("Error", "Enter course name")

    tk.Button(root, text="Add Course", command=add_course).pack(pady=5)

    #View users 
    def view_users():
        clear_frame(root)
        tk.Label(root, text="All Users", font=("Arial", 18)).pack(pady=10)

        cur.execute("SELECT username, role FROM users")
        users = cur.fetchall()

        for u in users:
            tk.Label(root, text=f"{u[0]} - {u[1]}").pack()

        tk.Button(root, text="Back", command=admin_dashboard).pack(pady=20)

    tk.Button(root, text="View Registered Users", command=view_users).pack(pady=15)
    tk.Button(root, text="Logout", command=login_screen).pack(pady=10)



#STUDENT DASHBOARD---------------------------------------------------------------------------

def student_dashboard(username):
    clear_frame(root)

    tk.Label(root, text=f"Welcome, {username}", font=("Arial", 18)).pack(pady=10)
    tk.Label(root, text="Available Courses:", font=("Arial", 14)).pack(pady=10)

    cur.execute("SELECT name FROM courses")
    courses = cur.fetchall()

    for c in courses:
        tk.Label(root, text="- " + c[0]).pack()

    tk.Button(root, text="Logout", command=login_screen).pack(pady=20)



login_screen() #starts at login 
root.mainloop()
