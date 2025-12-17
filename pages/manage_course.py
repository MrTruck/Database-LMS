import streamlit as st
from data import get_connection
from auth import login_check, verify_instructor
from helper import heading, course_header, display_time_24h


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


for s_num, s in enumerate(course_sessions):
    session_id = s["sessionID"]
    warning = False
    save = False

    with st.container(border=True):
        st.caption(f"Session {s_num+1}")
        st.markdown(f"**{s['sessionTitle']}**")

        col1, col2, col3 = st.columns([2,2,8])
        col1.caption(s['sessionDate'])
        col2.caption(display_time_24h(s['sessionTime']))
        col3.caption("")

        # ---------- INIT ----------
        links_key = f"links_{session_id}"
        input_key = f"new_link_{session_id}"

        if links_key not in st.session_state:
            if s["contentLink"]:
                st.session_state[links_key] = s["contentLink"].split()
            else:
                st.session_state[links_key] = []

        links = st.session_state[links_key]

        # ---------- EXISTING LINKS (FIXED) ----------
        for idx in range(len(links)):
            col1, col2 = st.columns([5, 1])

            with col1:
                links[idx] = st.text_input(
                    f"Attachment {idx + 1}",
                    value=links[idx],
                    key=f"link_{session_id}_{idx}"
                )

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("❌", key=f"del_{session_id}_{idx}"):
                    del links[idx]
                    st.rerun()

        # ---------- ADD NEW LINK ----------
        st.text_input(
            "New attachment",
            key=input_key,
            placeholder="https://example.com/file.pdf"
        )

        attachment_col, save_col, empty_col = st.columns([8,7,16])

        with attachment_col:
            if st.button("➕ Add attachment", key=f"add_{session_id}"):
                new_link = st.session_state[input_key].strip()
                if new_link:
                    links.append(new_link)
                    st.rerun()
                else:
                    warning = True

        # ---------- SAVE ----------
        with save_col:
            if st.button("💾 Save", key=f"save_{session_id}"):
                new_content = " ".join(link for link in links if link.strip())

                cursor.execute(
                    "UPDATE Session SET contentLink = %s WHERE sessionID = %s",
                    (new_content, session_id)
                )
                conn.commit()
                save = True

        if warning:
            st.warning("Attachment link cannot be empty")

        if save:
            st.success("Attachments updated successfully")


cursor.close()
conn.close()
