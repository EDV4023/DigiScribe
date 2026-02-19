import easyocr 
import cv2
import streamlit as st
from google import genai
from google.genai import types
import numpy as np
# import pyperclip
from PIL import Image
import PIL
# import os

st.set_page_config(page_title = "DigiScribe")

if "MODE" not in st.session_state:
    st.session_state.MODE = "Lite"
    st.session_state.context = ""
    st.session_state.context_sentence = ""
    st.session_state.allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?$ "
    st.session_state.text = ""
    st.session_state.refined_text = ""
    st.session_state.extra_detail = ""
    st.session_state.avg = 0.0


@st.cache_resource
def load_easyocr():
    return easyocr.Reader(['en'], gpu = False, verbose=True)
handwriting_reader = load_easyocr()


client = genai.Client(api_key = st.secrets["API_KEY"])
if "uploaded" not in st.session_state:  
    st.session_state["uploaded"] = False


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

    

def resize(image):
    max_side = 1200
    height, width = image.shape[0:2]
    scale = max_side / max(height, width)

    if scale < 1:
        image = cv2.resize(image, (int(scale*width),int(scale*height)))
    return image
    


def recognize(image):
    image.seek(0)

    image_bytes = image.getvalue()
    image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    image = resize(image)

    try:
        vision_text = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = [
                types.Part.from_bytes(data = image_bytes, mime_type = "image/jpeg"),
                "Transcribe the text from the image exactly. Do not perform any spelling/grammar/context changes keep the exact layout as it was given."
            ]
        )
    except:
        st.error("Too many server requests. Try again later.")
        st.stop()
        return

    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents = f"This text was taken out of an OCR software. Refine the words, phrases, or sentences that are nonsensical so that the final text is intelligible. Do not change the order of the original characters after refinement. First fix spelling issues then move onto grammar issues. Only output the final, refined text. Add punctuation accordingly. {st.session_state.context_sentence}  Reccomended List of Characters {st.session_state.allowlist}. Put ** (Double Asterisks) around words, sentences or phrases that you are unsure/unconfident on. Here is the input text: {vision_text.text}.",
        config = types.GenerateContentConfig(
            temperature = 0.1 # Using a Lower temperature since the task does not necessitate variety 
            )
            )
    except:
        st.error("Too many server requests. Try again later.")
        st.stop()
        return


    return vision_text.text, response.text


def extract_text(file_param):
    # Read bytes from Streamlit file
    file_bytes = np.frombuffer(file_param.read(), np.uint8)
    # Decode into OpenCV image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Sharpen edges in image to enhance accuracy:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Turn image into grayscale
    sharpener = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]) # Define Filter Kernel
    sharpen = cv2.filter2D(gray, -1, sharpener) # Apply Filter Kernel
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    text = handwriting_reader.readtext(thresh, detail = 1, allowlist = st.session_state.allowlist)
    simple_text = str(" ".join(handwriting_reader.readtext(thresh, detail = 0, allowlist = st.session_state.allowlist, paragraph = True)))
    # simple_text = simple_text[2:-2]

    bbox_list = []
    word_list = []
    confidence_list = []

    average_confidence = 0

    for (bbox, word, confidence) in text:
        bbox_list.append(bbox)
        word_list.append(word)
        confidence_list.append(float(confidence))
        average_confidence += float(confidence)

    average_confidence /= len(confidence_list)

    annotated_text = ""

    for i, segment in enumerate(word_list):
        annotated_text += "***" + str(segment) + "***"
        annotated_text += " (Confidence: " +  str(confidence_list[i]) + "), "

    try: 
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = f"This text was taken out of an OCR software. Refine the words, phrases, or sentences that are nonsensical so that the final text is intelligible. Do not change the order of the original characters after refinement. First fix spelling issues then move onto grammar issues. Only output the final, refined text. Add punctuation accordingly. The confidence scores from the OCR model are also given, for high confidence segments avoid changing it unless there are clarity/spelling/context issues. {st.session_state.context_sentence}  Put ** (Double Asterisks) around words, sentences or phrases that the OCR had below 0.50 in confidence. Here is the input text: {annotated_text}.",
            config = types.GenerateContentConfig(
                temperature = 0.1 # Using a Lower temperature since the task does not necessitate variety 
            )
        )
    except:
        st.error("Too many server requests. Try again later.")
        st.stop()
        return

    return simple_text, response.text, annotated_text, average_confidence

def perform_extraction():
    if st.session_state["uploaded"]:
        refined_text = "" 
        text = "" 
        extra_details = ""
        with st.spinner("Extracting...", show_time = True):
            if st.session_state.MODE == "Lite":
                text, refined_text, extra_details, avg = extract_text(FILE)
                return text, refined_text, extra_details, avg
            elif st.session_state.MODE == "Performance":
                text, refined_text = recognize(FILE)
                return text, refined_text

title, config = st.columns([0.93, 0.07])
if st.session_state.MODE == "Lite":
    title.title("**:blue[Digi]:blue[Scribe]**   :yellow[  Lite]")
elif st.session_state.MODE == "Performance":
    title.title("**:blue[Digi]:blue[Scribe]**   :red[  Performance]")

config.button("", icon = ":material/settings:", on_click = configurations)

with st.container(border = True):
    upload, cam = st.columns([0.5,0.5])

    with upload:
        uploaded_file = st.file_uploader(label = "**Upload an Image for Conversion (PNG, JPG, JPEG)**", type = ["jpg", "jpeg", "png"])  # r"Handwriting Recognition\Images_Examples\aTfamilymovingsentence.png"
        st.space(10)
    with cam:
        captured_file = st.camera_input("**Take a picture**")

if uploaded_file == None and captured_file != None:
    FILE = captured_file
elif captured_file == None and uploaded_file != None:
    FILE = uploaded_file
else:
    FILE = None

if FILE != None:
    st.session_state["uploaded"] = True
elif FILE == None:
    st.session_state["uploaded"] = False

# if st.session_state["uploaded"]:
#     refined_text = "" 
#     text = "" 
#     extra_details = ""

if upload.button("Extract", width = 200, type = "primary"):
    if st.session_state.MODE == "Lite":
        st.session_state.text, st.session_state.refined_text, st.session_state.extra_details, st.session_state.avg = perform_extraction()
    else:
        st.session_state.text, st.session_state.refined_text = perform_extraction()


extracted, refined, img = st.tabs(["Initially Extracted Text","Refined Text", "Image"])

with extracted:
    ex_cont = st.container(height = 200, key = "extc")
    ex_cont.write(st.session_state.text)
    # extracted_copy, extracted_download = st.columns([0.05,0.95])
    # with extracted_copy:
    #     if st.button(label = "", icon=":material/content_copy:", type = "tertiary", key = 'ec'):
    #         pyperclip.copy(text)
    # with extracted_download:
    st.download_button("Download Extracted Text", data = st.session_state.text, file_name = "digi_scribe_extracted_text.txt", icon=":material/download:", on_click = "ignore")

with refined:
    ref_cont = st.container(height = 200, key = "refc")
    ref_cont.write(st.session_state.refined_text)
    # refined_copy, refined_download = st.columns([0.05,0.95])
    # with refined_copy:
    #     if st.button(label = "", icon=":material/content_copy:", type = "tertiary", key = 'rc'):
    #         pyperclip.copy(refined_text)
    # with refined_download:
    st.download_button("Download Refined Text", data = st.session_state.refined_text, file_name = "digi_scribe_refined_text.txt", icon=":material/download:", on_click = "ignore")

with img:
    if FILE != None:
        st.image(FILE)


if st.session_state["uploaded"] and st.session_state.MODE == "Lite":
    st.divider()
    with st.expander("Extra Data/Stats:"):
        st.write(f"***Average Confidence:*** {st.session_state.avg}")
        st.write(st.session_state.extra_details)
        st.write("***Configurations:***")
        st.write("**Allowed characters:** [space]" + st.session_state.allowlist)
        st.write(st.session_state.context_sentence)

with st.container(horizontal_alignment = "right"):
    st.page_link(r"TextEditor.py", icon = ":material/edit:")


# TODO: Turn text, refined_text, extra_details and avg into streamlit session_state vars
# TODO: Add confidence based threshold selection ---> Add contrast parameter and regularization parameters
# TODO: Segment text before recognition
# TODO: Add warning to refrain from uploading personal details on DigiScribe
# TODO: Add a text editor section where low confidence words/phrases/sentences are bolded and the user can edit them and then download
# TODO: Add easyOCR model files to fix bug
# TODO: Add batch processing multiple images
# TODO: Add text to speech capabilities
# TODO: Add AI summaries of text/notes
# TODO: Create DigiScribe Student mode with AI summaries and quizes and different note-taking methods like cornell notes 



#---------- Later ----------#
# TODO: Make third tab with Image with Bounded Box of words
# TODO: Improve speed with pytorch threads
# TODO: Add more languages
# TODO: Add more download formats
