import streamlit as st


st.set_page_config(page_title = "DigiScribe - Student Hub", page_icon = r"DigiScribe_logo_icon.png", layout = "wide")
st.logo(image = r"DigiScribe_Logo.png",icon_image = r"DigiScribe_logo_icon.png", size = "large")


# Sidebar customized menu
st.sidebar.title("**DigiScribe Menu**")
st.sidebar.space(1)

st.sidebar.subheader("**Extract Text:**")
st.sidebar.page_link(r"DigiScribe.py", label = "*DigiScribe*", icon = ":material/image:")

st.sidebar.subheader("**Markdown Text Editor:**")
st.sidebar.page_link(r"pages/TextEditor.py", label = "*Text Editor*", icon = ":material/edit:")

st.sidebar.subheader("**Student Hub:**")
st.sidebar.page_link(r"pages/StudentHub.py", label = "*Student Hub*", icon = ":material/school:")


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



st.image(r"DigiScribe_Logo.png", width = 750)
st.title("**:blue[Student Hub]**")
