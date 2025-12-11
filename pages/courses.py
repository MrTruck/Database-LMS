import streamlit as st
import streamlit as st
from data import fake_courses
from auth import login_check
from helper import heading


login_check()
heading()

MAX_DESC_CHAR = 300

def format_desc(desc: str):
    desc = desc[:MAX_DESC_CHAR]
    return desc.ljust(MAX_DESC_CHAR, " ")   # pad spaces (works in monospace)

def course_card(title, desc):
    return f"""
    <div style="
        padding: 10px 0;
        border-radius: 6px;
        margin-bottom: 10px;
        width: 100%;
        height:150px;
    ">
        <h5 style="margin: 0 0 5px 0;">{title}</h4>
        <div style="
            font-size:14px;
            color:#fff;
            font-family:monospace;
        ">
            {desc}
        </div>
    </div>
    """

col1, col2 = st.columns(2)
current_col = 0

for title in fake_courses:
    desc = format_desc(fake_courses[title])

    if current_col == 0:
        target_col = col1
        current_col = 1
    else:
        target_col = col2
        current_col = 0

    with target_col:
        with st.container(border=True):   # <-- new wrapper
            st.markdown(course_card(title, desc), unsafe_allow_html=True)
            
            if st.button("Go to course", key=f"btn_{title}"):
                st.session_state.selected_course = title
                st.switch_page("pages/course")