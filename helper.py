import streamlit as st

def heading():
    col1, col2 = st.columns(2)
    col1.header(st.session_state.username)
    col2.header("ID: " + str(st.session_state.user_id))

