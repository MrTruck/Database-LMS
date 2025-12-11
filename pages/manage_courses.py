import streamlit as st
import streamlit as st
from auth import login_check, verify_instructor
from helper import heading



login_check()
heading()
verify_instructor()

st.write("testing")
