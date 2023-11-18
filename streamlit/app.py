import streamlit as st
from text_generation import generate_recipe
import time
import os
from audiorecorder import audiorecorder
from Models.Voice_To_Text_Local import transcribe_audio_wav2vec



# Set page config for custom theme
st.set_page_config(
    page_title="Mood-Based Recipe Generator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# This is a Mood-Based Recipe Generator App!"
    }
)

# Custom theme
primaryColor = "#00cc66"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#000000"
font = "sans serif"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: {backgroundColor}
    }}
    .sidebar .sidebar-content {{
        background: {secondaryBackgroundColor}
    }}
    .widget-label {{
        color: {textColor};
        font-family: {font};
    }}
    .st-bb {{
        background-color: {primaryColor};
    }}
    .st-at {{
        background-color: {primaryColor};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Define pages as functions
def main_page():
    st.title("Welcome to the Mood-Based App")
    st.markdown("""
        <div style="display: flex; justify-content: space-around;">
            <a href="?page=text_input_output"><div class="square">Text Input/Output</div></a>
            <a href="?page=voice_recording"><div class="square">Voice Recording</div></a>
            <a href="?page=camera_interaction"><div class="square">Camera Interaction</div></a>
        </div>
        <style>
            .square {
                width: 100px;
                height: 100px;
                background-color: #00cc66;
                margin: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 20px;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

def text_input_output():
    st.title('Mood-Based Recipe Generator')
    with st.form("recipe_form", clear_on_submit=True):
        st.write("Enter your details to get a personalized recipe:")
        age = st.text_input("Write your age")
        gender = st.text_input("Your gender")
        mood = st.text_input("What do you feel")

        submit_button = st.form_submit_button(label='Get Recipe')

        if submit_button:
            recipe = generate_recipe(age, gender, mood)
            st.success("Here's your personalized recipe:")
            st.write(recipe)

def voice_recording():
    st.title('Voice Recording and Playback')
    st.title("Audio Recorder")
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:
        # To play audio in frontend:
        st.audio(audio.export().read())  

        # To save audio to a file, use pydub export method:
        audio.export("audio.wav", format="wav")

        # To get audio properties, use pydub AudioSegment properties:
        st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

        transcription = transcribe_audio_wav2vec('audio.wav')
        print(transcription)

def camera_interaction():
    st.title('Camera Interaction')
    st.markdown("## Take a picture")
    st.markdown("Please use your camera to take a picture, then upload it here.")

    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        # Display the image
        st.image(uploaded_image, caption="Uploaded Image.")

# Main app logic
page = st.experimental_get_query_params().get("page", ["main_page"])[0]

if page == "main_page":
    main_page()
elif page == "text_input_output":
    text_input_output()
elif page == "voice_recording":
    voice_recording()
elif page == "camera_interaction":
    camera_interaction()