# 📚 Learning Management System (LMS)

A **Learning Management System (LMS)** built with **Streamlit** and **MySQL**, designed for managing courses, instructors, students, and session-based learning materials.  
This project focuses on simplicity, usability, and hands-on database integration.

---

## Features

### Authentication
- Login system for **students** and **instructors**
- Role-based access control
- Session-based authentication using `st.session_state`

### Courses
- Students can view enrolled courses
- Instructors can view and manage their own courses
- Clickable course cards with clean UI

### Instructor Dashboard
- Manage courses they teach
- View and edit course sessions
- Add, update, and remove session attachments (links)

### Course Sessions
- Sessions belong to courses
- Each session can have **multiple attachment links**
- Full **CRUD** support for attachments:
  - Add new links
  - Edit existing links
  - Delete individual links
- Changes persist directly to the MySQL database

### Database Integration
- Fully normalized relational database
- Tables include:
  - User
  - Student
  - Instructor
  - Course
  - Enrollment
  - Session

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Database**: MySQL
- **Connector**: `mysql-connector-python`

---

## 📦 Dependencies

Make sure you have Python **3.9+** installed.

Install dependencies with:

```bash
pip install streamlit mysql-connector-python
