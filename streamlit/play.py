import streamlit as st
from datetime import datetime
from text_generation import generate_response, run_rekognition_prompt
from image_recognition import run_rekognition
<<<<<<< Updated upstream
from text_generation import generate_recipe , generate_recipe_dyn
from audiorecorder import audiorecorder
from Models.Voice_To_Text_Local import transcribe_audio_wav2vec
from Models.Voice_To_Emotion_Local import query
from Models.Text_To_Voice_Local import text_to_speech
from prompt_store import get_prompt_2

=======
from streamlit_tags import st_tags, st_tags_sidebar
import os
>>>>>>> Stashed changes
# Define your questions and options
question1 = "Do you have any food allergies?"
options1 = ["dairy-free", "Blue", "Green"]

question2 = "Do you follow any of these diets?"
options2 = ["Vegan", "Vegeterian", "Keto", "High Protein"]

question3 = "How would you describe your cooking skills?"
options3 = ["Begginer", "Intermediate", "Expert"]

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'vision_history' not in st.session_state:
    st.session_state.vision_history = []

<<<<<<< Updated upstream
if 'audio_processed' not in st.session_state:
    st.session_state.audio_processed = False

if 'recipe_generated' not in st.session_state:
    st.session_state.recipe_generated = False
=======
# Function to load images
def load_images(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"): # Add more formats if needed
            images.append(filename)
    return images

# Function to handle button click
def handle_click(image_index):
    # Redirect to home page with the image index
    d = {0:'junkie mood', 1:'healthy mood'}
    st.session_state['selected_persona'] = d[image_index]
    st.write(f"Selected image index: {image_index}")

# Display images in a grid
def display_images():
    images = ["./personas/junky.png", "./personas/healthy.png"]
    # Check if selected_image is already in session state
    if 'selected_image' not in st.session_state:
        st.session_state['selected_image'] = None

    # Display images with buttons
    st.write('## Choose from existing personas')
    for index, image in enumerate(images):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.image(image, width=300)  # Adjust width as necessary
        with col2:
            unique_key = f"select_button_{index}"
            st.button("Select", key=unique_key, on_click=handle_click, args=(index,))

    # Display selected image index
    if st.session_state['selected_image'] is not None:
        st.write(f"You have selected image {st.session_state['selected_image']}")

def display_personas():
    keywords = st_tags(
        label='# Create new persona:',
        text='Press enter to add more',
        value=['High protein', 'gym buddy', 'low fat'],
        suggestions=['five', 'six', 'seven', 
                    'eight', 'nine', 'three', 
                    'eleven', 'ten', 'four'],
        maxtags = 20,
        key='1')
    st.button("Create", type="primary")

    
    display_images()
    
>>>>>>> Stashed changes


# Function to display questions
def display_questions():
    answer1 = st.selectbox(question1, options1)
    answer2 = st.selectbox(question2, options2)
    answer3 = st.selectbox(question3, options3)

    if st.button("Submit"):
        # Store the answers in the session state
        st.session_state["answer1"] = answer1
        st.session_state["answer2"] = answer2
        st.session_state["answer3"] = answer3

        # Redirect to the main page
        st.session_state["questions_answered"] = True

# Check if the questions have been answered
if "selected_persona" not in st.session_state or not st.session_state["selected_persona"]:
    display_personas()
else:
    # Display the main page with the answers
    st.write(f"## you are using the {st.session_state['selected_persona']} persona")
    tab1, tab2, tab3 = st.tabs(["chat", "camera", "talk"])
    with tab1:
       
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("Your message")

            # Send Button
            submit_button = st.form_submit_button(label='Send')

            if submit_button:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_message = f"You ({timestamp}): {user_input}"
                st.session_state.chat_history.append(user_message)
                # Dummy AI Response
                response = generate_response(user_input)
                ai_response = f"AI ({timestamp}): {response}."
                st.session_state.chat_history.append(ai_response)
            with st.chat_message("User"):
                for message in st.session_state.chat_history:
                    st.text(message)
            st.balloons()

    with tab2:
        picture = st.camera_input("Take a picture")

        if picture:
            picture = picture.getvalue()
            res = run_rekognition(picture)
            print(res)
            ai_res = run_rekognition_prompt(res[0]['emotion'])
            st.write(f"I can see you feel {res[0]['emotion']}")
            st.session_state.vision_history.append(f"I can see you feel {res[0]['emotion']}")
            st.session_state.vision_history.append(ai_res)
        with st.chat_message("User"):
          for message in st.session_state.vision_history:
                st.text(message)
        st.session_state.vision_history = []
        st.balloons()

    with tab3:
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


