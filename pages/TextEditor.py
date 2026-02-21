import easyocr 
import cv2
import streamlit as st
from google import genai
from google.genai import types
import numpy as np
# import pyperclip
from PIL import Image
import PIL
import markdownify
from streamlit_quill import st_quill
# import os

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


@st.dialog("**Configurations**", on_dismiss = "rerun")
def configurations():
    st.pills("**Mode:**", options = ["Lite", "Performance"], selection_mode = "single", key = "MODE_input")

    st.text_input("**Provide context/topic for image:**", placeholder = "Enter context", key = "context_input")

    st.write(f"**Current allowed list of characters:** [space]{st.session_state.allowlist}")
    st.text_input("**Enter allowed list of characters**", placeholder = "abcdefg...",key = "allowlist")

    def submit():
        if st.session_state.MODE_input:
            st.session_state.MODE = st.session_state.MODE_input
        if st.session_state.context_input.strip() != "":
            st.session_state.context_sentence = "**The context for the image:** \"" + st.session_state.context_input + "\"."
        if " " not in st.session_state.allowlist:
            st.session_state.allowlist = st.session_state.allowlist + " "



    submit_container = st.container(horizontal_alignment = "right")
    submit_container.button("Confirm", type = "primary", on_click = submit)


title, config = st.columns([0.93, 0.07])
if st.session_state.MODE == "Lite":
    title.title("**:blue[Digi]:blue[Scribe]**   :yellow[  Lite]")
elif st.session_state.MODE == "Performance":
    title.title("**:blue[Digi]:blue[Scribe]**   :red[  Performance]")

config.button("", icon = ":material/settings:", on_click = configurations)


with st.container(border = True):
    st.markdown(st.session_state.refined_text)
    st.caption("Bolded text represents segments where the model was unsure of.")

content = st_quill(value = st.session_state.refined_text.replace("*", ""), html = True)
markdown_text = markdownify.markdownify(content)

