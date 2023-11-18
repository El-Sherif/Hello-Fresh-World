import streamlit as st
from datetime import datetime
from text_generation import generate_response
from image_recognition import run_rekognition
from audiorecorder import audiorecorder
from Models.Voice_To_Text_Local import transcribe_audio_wav2vec

# Setting the layout
st.set_page_config(layout="wide")

if 'user_history' not in st.session_state:
    st.session_state.user_history = []
if 'system_history' not in st.session_state:
    st.session_state.system_history = []

options = ["Healthy", "Junk food", "Gym mood", "Family mood"]

# Function to apply custom styles
def apply_custom_styles():
    st.markdown("""
    <style>
    .stButton>button {
        border: 2px solid green;
        border-radius: 20px;
        padding: 5px 15px;
        margin: 5px;
        color: green;
        background-color: white;
    }
    .stButton>button:active {
        position: relative;
        top: 1px;
    }
    .selected {
        color: green;
        background-color: green;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# Initialize session state for button states
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []

# Create buttons for each option
for option in options:
    # Check if the option is already selected
    if option in st.session_state.selected_options:
        button_style = "selected"
    else:
        button_style = ""

    # Create a button for the option
    if st.button(option, key=option, args={"class": button_style}):
        # Toggle the option in the selected list
        if option in st.session_state.selected_options:
            st.session_state.selected_options.remove(option)
        else:
            st.session_state.selected_options.append(option)


col1, col2, col3 = st.columns([6, 2, 2])

with col1:
       with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message")

        # Send Button
        submit_button = st.form_submit_button(label='Get Recipe')

        if submit_button:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_message = f"You ({timestamp}): {user_input}"
            st.session_state.user_history.append(user_message)
            # Dummy AI Response
            response = generate_response(user_input)
            ai_response = f"AI ({timestamp}): {response}."
            st.session_state.system_history.append(ai_response)


with col2:
      picture = st.camera_input("Take a picture")

      if picture:
        picture = picture.getvalue()
        res = run_rekognition(picture)
        #st.write(res)
        st.session_state.system_history.append(res)


with col3:
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:
        # To play audio in frontend:
        st.audio(audio.export().read())  

        # To save audio to a file, use pydub export method:
        audio.export("audio.wav", format="wav")

        # To get audio properties, use pydub AudioSegment properties:
        st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

        transcription = transcribe_audio_wav2vec('audio.wav')
        st.session_state.system_history.append(transcription)

st.write("Chat History:")
with st.chat_message("User"):
    for message in st.session_state.user_history:
        st.text(message)

with st.chat_message("Hello Fresh"):
    for message in st.session_state.system_history:
        st.text(message)

