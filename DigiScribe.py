import easyocr 
import os
import cv2
import numpy
import streamlit as st
from google import genai
from google.genai import types
import numpy as np
# import pyperclip


handwriting_reader = easyocr.Reader(['en'], gpu = False, verbose=True)
client = genai.Client(api_key = st.secrets["API_KEY"])

st.session_state["uploaded"] = False

def extract_text(file_param):
    # Read bytes from Streamlit file
    file_bytes = np.frombuffer(file_param.read(), np.uint8)
    # Decode into OpenCV image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Sharpen edges in image to enhance accuracy:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Turn image into grayscale
    sharpener = numpy.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]) # Define Filter Kernel
    sharpen = cv2.filter2D(gray, -1, sharpener) # Apply Filter Kernel
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    text = handwriting_reader.readtext(thresh, detail = 1, allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?$ ")
    simple_text = str(" ".join(handwriting_reader.readtext(thresh, detail = 0, allowlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?$ ", paragraph = True)))
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


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = f"This text was taken out of an OCR software. Refine the words, phrases, or sentences that are nonsensical so that the final text is intelligible. Only output the final, refined text. Add punctuation accordingly. The confidence scores from the OCR model are also given, for high confidence segments avoid changing it unless there are clarity/spelling/context issues. Here is the input text: {annotated_text}",
        config = types.GenerateContentConfig(
            temperature = 0.1 # Using a Lower temperature since the task does not necessitate variety 
        )
    )

    return simple_text, response.text, annotated_text, average_confidence


st.title("***Digi:blue[Scribe]***")

upload, cam = st.columns([0.5,0.5])

with upload:
    FILE = st.file_uploader(label = "Upload an Image for Conversion (PNG, JPG, JPEG)", type = ["jpg", "jpeg", "png"])  # r"Handwriting Recognition\Images_Examples\aTfamilymovingsentence.png"
with cam:
    FILE = st.camera_input("Take a picture", )

if FILE != None:
    st.session_state["uploaded"] = True
elif FILE == None:
    st.session_state["uploaded"] = False

refined_text = "" 
text = "" 
extra_details = ""

if st.session_state["uploaded"]:
    refined_text = "" 
    text = "" 
    extra_details = ""
    with st.spinner("Extracting...", show_time = True):
        text, refined_text, extra_details, avg = extract_text(FILE)


extracted, refined, img = st.tabs(["Initially Extracted Text","Refined Text", "Image"])

with extracted:
    st.text_area(label = " ", placeholder = text, disabled = True, key = "extr")
    # extracted_copy, extracted_download = st.columns([0.05,0.95])
    # with extracted_copy:
    #     if st.button(label = "", icon=":material/content_copy:", type = "tertiary", key = 'ec'):
    #         pyperclip.copy(text)
    # with extracted_download:
    st.download_button("Download Extracted Text", data = text, file_name = "digi_scribe_extracted_text.txt", icon=":material/download:", on_click = "ignore")

with refined:
    st.text_area(label = " ",placeholder = refined_text, disabled = True, key = "ref")
    # refined_copy, refined_download = st.columns([0.05,0.95])
    # with refined_copy:
    #     if st.button(label = "", icon=":material/content_copy:", type = "tertiary", key = 'rc'):
    #         pyperclip.copy(refined_text)
    # with refined_download:
    st.download_button("Download Refined Text", data = text, file_name = "digi_scribe_refined_text.txt", icon=":material/download:", on_click = "ignore")

with img:
    if FILE != None:
        st.image(FILE)


if st.session_state["uploaded"]:
    st.divider()
    with st.expander("Extra Data/Stats:"):
        st.write(f"***Average Confidence:*** {avg}")
        st.write(extra_details)




# TODO: Add confidence based threshold selection ---> Add contrast parameter and regularization parameters
# TODO: Add batch processing multiple images
# TODO: Add settings popover for allowlist, numbers, extra topic content for notes for the AI etc.


##### Later #####
# TODO: Change font to Indie Flower from google fonts by using tutorial: https://docs.streamlit.io/develop/tutorials/configuration-and-theming/external-fonts 
# TODO: Make third tab with Image with Bounded Box of words