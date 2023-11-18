from openai import OpenAI

def transcribe_audio(file_path):
    client = OpenAI(api_key='your-api-key')
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )
    return transcript
