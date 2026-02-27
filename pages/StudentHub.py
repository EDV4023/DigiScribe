import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title = "DigiScribe - Student Hub", page_icon = r"DigiScribe_logo_icon.png", layout = "wide")
st.logo(image = r"DigiScribe_Logo.png",icon_image = r"DigiScribe_logo_icon.png", size = "large")

client = genai.Client(api_key = st.secrets["API_KEY"])

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
    st.session_state.MODE = "Performance"
    st.session_state.context = ""
    st.session_state.context_sentence = ""
    st.session_state.allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?$ "
    st.session_state.text = ""
    st.session_state.refined_text = ""
    st.session_state.extra_detail = ""
    st.session_state.avg = 0.0
    st.session_state.uploaded = False

if "edited_text" not in st.session_state and st.session_state.refined_text:
    st.session_state.edited_text = st.session_state.refined_text

st.image(r"DigiScribe_Logo.png", width = 750)
st.title("**:blue[Student Hub]**")

concise_summary_cont = st.container(border = True)

if "concise_summary" not in st.session_state and st.session_state.edited_text and st.session_state.refined_text:
    st.session_state.concise_summary = ""

def get_concise_summary():
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents = f"Provide a short and quick summary of the text in bullet point format. No more than 5 bullet points with each bullet point being a maximum of one sentence. Here is the text to be summarized: {st.session_state.edited_text}",
            )
        st.session_state.concise_summary = response.text
        concise_summary_cont.markdown(st.session_state.concise_summary)
    except:
        st.error("Too many server requests. Try again later.")
        st.stop()


st.button("Summarize Text", on_click = get_concise_summary)