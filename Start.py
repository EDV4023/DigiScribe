import streamlit as st

pages = st.navigation([
    st.Page("DigiScribe.py", title = "DigiScribe"), 
    st.Page("TextEditor.py", title = "Text Editor")])

pages.run()