import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS

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
audio_cont = st.container()
if "edited_text" in st.session_state:
    concise_summary_cont = st.container(border = True)

    if "concise_summary" not in st.session_state and "edited_text" in st.session_state:
        st.session_state.concise_summary = ""

    if "study_guide" not in st.session_state and "edited_text" in st.session_state:
        st.session_state.study_guide = ""


    def get_concise_summary():
        try:
            response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = f"Do not start the response with any formalities, greetings or messages like \"Here is a concise 5 bullet point summary\". Provide a short and quick summary of the text in bullet point format. No more than 5 bullet points with each bullet point being a maximum of one sentence. If not text given respond with no text as well. Here is the text to be summarized: {st.session_state.edited_text}",
                )
            st.session_state.concise_summary = response.text
            concise_summary_cont.markdown(st.session_state.concise_summary)
        except:
            st.error("Too many server requests. Try again later.")
            st.stop()


    st.button("Summarize Text", on_click = get_concise_summary)


    study_guide_cont = st.container(border = True, height = 500)


    def get_study_guide():
        try:
            response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = f"Do not start the response with any formalities, greetings or messages like \"Here is a study guide on...\". Provide a highly detailed summary of the given text/notes. Bold important vocabulary, phrases, and explanations (All Done with Markdown Formating). Format it so that it starts with an in depth summary of the text. Then Important vocabulary and their definitions. Finally, at the end create a 20 question quiz (Without showing the answers) with an assorted mix of multiple choice, free response, True or False, and Select all that are correct questions. In the end list the answers for the quiz with #Number then Answer. Here is the inputted text to create a study guide for: {st.session_state.edited_text}",
                )
            st.session_state.study_guide = response.text
            study_guide_cont.markdown(st.session_state.study_guide)
        except:
            st.error("Too many server requests. Try again later.")
            st.stop()

    def play_audio_teach():
        try:
            response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = f"Do not start the response with any formalities, greetings or messages like \"Here is an teacher instructing a student on...\". Provide a summary of the text's main points, vocabulary, and explanations in the format of a teacher instructing one student using simple breakdown, analogies, and step by step guidelines on how to understand the topic. Here is the text to turn into educational lecture format: {st.session_state.study_guide}",
                )
            st.session_state.audio_teach = response.text
            audio_teach = gTTS(st.session_state.audio_teach, lang = "en", slow = False)
            audio_teach.save("digiscribe_audio_teach.mp3")
            audio_cont.audio("digiscribe_audio_teach.mp3")
        except:
            st.error("Too many server requests. Try again later.")
            st.stop()

    

    empty = st.empty()
    study_guide_button =  empty.button("Create Study Guide", on_click = get_study_guide)
    if study_guide_button:
        with empty.container(horizontal_alignment = "left"):
            st.download_button("Download as Markdown", file_name = "digiscribe_study_guide.md", data = st.session_state.study_guide, on_click = "ignore")
            st.button("Play Audio Teach", icon = ":material/music_note:", on_click = play_audio_teach)
else:
    st.info("Extract Text to use Student Hub tools.")