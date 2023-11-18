import streamlit as st
from datetime import datetime
from text_generation import generate_response, run_rekognition_prompt
from image_recognition import run_rekognition

# Define your questions and options
question1 = "Do you have any food allergies?"
options1 = ["Red", "Blue", "Green"]

question2 = "Do you follow any of these diets?"
options2 = ["Dog", "Cat", "Bird"]

question3 = "How would you describe your cooking skills?"
options3 = ["Begginer", "Medium", "Expert"]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'vision_history' not in st.session_state:
    st.session_state.vision_history = []

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
if "questions_answered" not in st.session_state or not st.session_state["questions_answered"]:
    display_questions()
else:
    # Display the main page with the answers
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

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

