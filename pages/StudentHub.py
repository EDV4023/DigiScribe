import streamlit as st

st.set_page_config(page_title = "DigiScribe - Student Hub")
st.logo(image = r"DigiScribe_Logo.png", icon_image = r"DigiScribe_logo_icon.png")


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



st.title("**:blue[Digi]:blue[Scribe]**   :green[  Student Hub]")