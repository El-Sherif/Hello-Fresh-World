import requests

# Hardcode the API URL and Authorization Token
API_URL = "https://api-inference.huggingface.co/models/ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
AUTH_TOKEN = "your-huggingface-api-token"  # Replace with your actual token

def query(filename):
    """
    Queries the Hugging Face API for speech emotion recognition.

    Parameters:
    filename (str): Path to the audio file.

    Returns:
    dict: The JSON response from the API.
    """
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


# Usage

# from Voice_To_Emotion(Local) import query

# file_path = 'path/to/audio_file.mp3'  # Replace with your audio file path
# emotion_recognition_output = query(file_path)
# print(emotion_recognition_output)

# Example Output

# [{'score': 0.13720019161701202, 'label': 'sad'}, {'score': 0.12760917842388153, 'label': 'neutral'}, {'score': 0.12616483867168427, 'label': 'happy'}, {'score': 0.12531578540802002, 'label': 'disgust'}, {'score': 0.12471558153629303, 'label': 'fearful'}]

