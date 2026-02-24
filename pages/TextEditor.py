import streamlit as st
import markdownify
from streamlit_quill import st_quill

st.set_page_config(page_title = "DigiScribe - Text Editor", page_icon = r"DigiScribe_logo_icon.png")
st.logo(image = r"DigiScribe_Logo.png",icon_image = r"DigiScribe_logo_icon.png", size = "large")

# Sidebar customized menu
st.sidebar.title("**DigiScribe Menu**")
st.sidebar.space(2)

st.sidebar.subheader("**Extract Text from Images:**")
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



st.title("**:blue[Digi]:blue[Scribe]**   :gray[  Text Editor]")

with st.container(border = True):
    st.markdown(st.session_state.refined_text)
    st.caption("Bolded text represents segments where the model confidence was low.")

content = st_quill(value = st.session_state.refined_text.replace("*", ""), html = True)
markdown_text = markdownify.markdownify(content)

with open("digiscribe_md.md", "w") as f:
        f.write(markdown_text)

col1, col2 = st.columns(2)
dowload_cont = col1.container(horizontal_alignment = "left")
next_cont = col2.container(horizontal_alignment = "right")
download_md = dowload_cont.download_button("Download as Markdown", file_name = r"digiscribe_md.md", data = markdown_text, icon=":material/download:", on_click = "ignore")
next_button = next_cont.page_link(page = r"pages/StudentHub.py",icon = ":material/school:", label = "Student Hub")
