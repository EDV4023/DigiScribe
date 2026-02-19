import streamlit as st

st.set_page_config(page_title = "DigiScribe")

pages = st.navigation([
    st.Page("DigiScribe.py", title = "DigiScribe"), 
    st.Page("TextEditor.py", title = "Text Editor")])

pages.run()