import streamlit as st
import markdownify
from streamlit_quill import st_quill

st.set_page_config(page_title = "DigiScribe - Text Editor")

# Initialize session states
if "MODE" not in st.session_state:
    st.session_state.MODE = "Lite"
    st.session_state.context = ""
    st.session_state.context_sentence = ""
    st.session_state.allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?$ "
    st.session_state.text = ""
    st.session_state.refined_text = ""
    st.session_state.extra_detail = ""
    st.session_state.avg = 0.0
    st.session_state.uploaded = False



st.title("**:blue[Digi]:blue[Scribe]**   :gray[  Text Editor]")

with st.container(border = True):
    st.markdown(st.session_state.refined_text)
    st.caption("Bolded text represents segments where the model confidence was low.")

content = st_quill(value = st.session_state.refined_text.replace("*", ""), html = True)
markdown_text = markdownify.markdownify(content)