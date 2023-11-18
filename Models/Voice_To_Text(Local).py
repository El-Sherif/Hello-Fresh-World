# !pip install transformers
# !pip install datasets
import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from scipy.signal import resample

# Load pretrained model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def read_audio(file_path, target_sample_rate=16000):
    audio, sample_rate = sf.read(file_path)
    if sample_rate != target_sample_rate:
        audio = resample(audio, int(len(audio) * target_sample_rate / sample_rate))
    return audio, target_sample_rate

def transcribe_audio_wav2vec(file_path):
    audio_input, sample_rate = read_audio(file_path)
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    
    return transcription


# Usage

# # main.py or any other file where you want to use this functionality
# from Voice_To_Text(Local) import transcribe_audio_wav2vec

# file_path = 'path/to/audio_file.wav'  # Replace with your audio file path
# transcription = transcribe_audio_wav2vec(file_path)
# print(transcription)