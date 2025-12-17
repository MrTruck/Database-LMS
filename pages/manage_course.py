import streamlit as st
from data import get_connection
from auth import login_check, verify_instructor
from helper import heading, course_header, display_time_24h
from datetime import timedelta
import uuid


login_check()
verify_instructor()
heading()


st.set_page_config(page_title="Course Management", page_icon="📚")

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

        col1, col2, col3 = st.columns([2,4,6])
        col1.caption(s['sessionDate'])
        delta_time = s['sessionTime']
        col2.caption(f"{display_time_24h(delta_time)} - {display_time_24h(delta_time + timedelta(hours=2))}")
        col3.caption("")

        # ---------- INIT ----------
        links_key = f"links_{session_id}"
        input_key = f"new_link_{session_id}"

        # Initialize links with unique IDs if not in session state
        if links_key not in st.session_state:
            if s["contentLink"]:
                # Create list of dicts with unique IDs for each link
                st.session_state[links_key] = [
                    {"id": str(uuid.uuid4()), "url": link} 
                    for link in s["contentLink"].split()
                ]
            else:
                st.session_state[links_key] = []
        else:
            # Migrate old format (plain strings) to new format (dicts with id and url)
            if st.session_state[links_key] and isinstance(st.session_state[links_key][0], str):
                st.session_state[links_key] = [
                    {"id": str(uuid.uuid4()), "url": link}
                    for link in st.session_state[links_key]
                ]

        links = st.session_state[links_key]

        # ---------- EXISTING LINKS ----------
        for idx, link_obj in enumerate(links):
            link_id = link_obj["id"]
            col1, col2 = st.columns([5, 1])

            with col1:
                # Use unique ID in the key to maintain widget identity
                new_value = st.text_input(
                    f"Attachment {idx + 1}",
                    value=link_obj["url"],
                    key=f"link_{session_id}_{link_id}"
                )
                # Update the URL in session state
                link_obj["url"] = new_value

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("❌", key=f"del_{session_id}_{link_id}"):
                    # Remove by ID, not by index
                    st.session_state[links_key] = [
                        l for l in st.session_state[links_key] if l["id"] != link_id
                    ]
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
                new_link = st.session_state.get(input_key, "").strip()
                if new_link:
                    st.session_state[links_key].append({
                        "id": str(uuid.uuid4()),
                        "url": new_link
                    })
                    st.rerun()
                else:
                    warning = True

        # ---------- SAVE ----------
        with save_col:
            if st.button("💾 Save", key=f"save_{session_id}"):
                # Extract URLs from the link objects
                new_content = " ".join(
                    link_obj["url"] for link_obj in st.session_state[links_key] 
                    if link_obj["url"].strip()
                )

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