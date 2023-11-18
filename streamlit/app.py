import streamlit as st
from text_generation import generate_recipe , generate_recipe_dyn
from image_recognition import run_rekognition
import time
import boto3
import os
from audiorecorder import audiorecorder
from Models.Voice_To_Text_Local import transcribe_audio_wav2vec
from Models.Voice_To_Emotion_Local import query
from Models.Text_To_Voice_Local import text_to_speech
from prompt_store import get_prompt_2

# Initialize session state variables
if 'audio_processed' not in st.session_state:
    st.session_state.audio_processed = False

if 'recipe_generated' not in st.session_state:
    st.session_state.recipe_generated = False


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

    if len(audio) > 0 and not st.session_state.audio_processed:
        # Process audio only once
        st.audio(audio.export().read())  
        audio.export("audio.wav", format="wav")
        st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

        transcription = transcribe_audio_wav2vec('audio.wav')
        emotion = query('audio.wav')[0]['label']
        
        prompt = get_prompt_2(emotion, transcription)
        recipe = generate_recipe_dyn(prompt)
        st.session_state.recipe = recipe  # Save recipe to session state
        st.session_state.audio_processed = True

    if st.session_state.audio_processed and not st.session_state.recipe_generated:
        st.success("Here's your personalized recipe:")
        st.write(st.session_state.recipe)

    if st.button('Play Audio') and st.session_state.audio_processed:
        text_to_speech(st.session_state.recipe)
        st.audio("output.wav", format='audio/wav')
        st.session_state.recipe_generated = True

def camera_interaction():
    st.title('Camera Interaction')
    st.markdown("## Take a picture")
    st.markdown("Please use your camera to take a picture, then upload it here.")

    picture = st.camera_input("Take a picture")
    picture = picture.getvalue()

    if picture:
        res = run_rekognition(picture)
        st.write(res)


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