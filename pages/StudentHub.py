import streamlit as st

st.set_page_config(page_title = "DigiScribe - Student Hub")
st.logo(image = r"DigiScribe_Logo.png", icon_image = r"DigiScribe_logo_icon.png", size = "large")

# Sidebar customized menu
st.sidebar.markdown("**Extract Text from Images:**")
st.sidebar.page_link(r"DigiScribe.py", label = "DigiScribe", icon = ":material/image:")

st.sidebar.markdown("**Markdown Text Editor:**")
st.sidebar.page_link(r"pages/TextEditor.py", label = "Text Editor", icon = ":material/edit:")

st.sidebar.markdown("**Student Hub:**")
st.sidebar.page_link(r"pages/TextEditor.py", label = "Student Hub", icon = ":material/school:")


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