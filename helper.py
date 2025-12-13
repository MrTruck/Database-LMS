import streamlit as st


def heading():
    # Render heading with a bottom border using HTML so we can style it
    if (st.session_state.logged_in == "student"):
        id_display = str(st.session_state.student_id)
    else:
        id_display = str(st.session_state.instructor_id)

    html = f"""
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e0e0e0; padding:6px 0;">
      <div style="font-size:25px; font-weight:600;">Hello, {st.session_state.username}!</div>
      <div style="font-size:21px; color:#666;">{st.session_state.logged_in} ID: {id_display}</div>
    </div>
    <br>
    """

    st.markdown(html, unsafe_allow_html=True)

