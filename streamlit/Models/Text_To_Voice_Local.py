import numpy as np
import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import soundfile as sf

import re
# Load model and processor
checkpoint = "microsoft/speecht5_tts"
processor = SpeechT5Processor.from_pretrained(checkpoint)
model = SpeechT5ForTextToSpeech.from_pretrained(checkpoint)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# Speaker embeddings
speaker_embeddings = {
    "BDL": "spkemb/cmu_us_bdl_arctic-wav-arctic_a0009.npy",
    "CLB": "spkemb/cmu_us_clb_arctic-wav-arctic_a0144.npy",
    "KSP": "spkemb/cmu_us_ksp_arctic-wav-arctic_b0087.npy",
    "RMS": "spkemb/cmu_us_rms_arctic-wav-arctic_b0353.npy",
    "SLT": "spkemb/cmu_us_slt_arctic-wav-arctic_a0508.npy",
}

def split_script(script):
    # Split the script at every full stop
    sentences = re.split(r'(\.)', script)

    # Re-add the full stops to each sentence and handle empty strings
    sentences = [sentence + '.' for sentence in sentences if sentence and not sentence.isspace()]

    # You may want to handle max_length here if necessary
    max_length = 600
    script_parts = []
    current_part = ""
    for sentence in sentences:
        if len(current_part) + len(sentence) > max_length:
            script_parts.append(current_part)
            current_part = sentence
        else:
            current_part += sentence

    if current_part:
        script_parts.append(current_part)

    return script_parts

def text_to_speech(script, output_file="output.wav"):
    if len(script.strip()) == 0:
        return

    # Split the script into parts
    script_parts = split_script(script)

    # Process each part and concatenate
    combined_speech = []
    for part in script_parts:
        inputs = processor(text=part, return_tensors="pt")
        input_ids = inputs["input_ids"]
        input_ids = input_ids[..., :model.config.max_text_positions]

        # Default speaker set to CLB (female)
        speaker_embedding = np.load(speaker_embeddings["CLB"])
        speaker_embedding = torch.tensor(speaker_embedding).unsqueeze(0)

        # Generating speech for each part
        speech = model.generate_speech(input_ids, speaker_embedding, vocoder=vocoder)
        speech = (speech.numpy() * 32767).astype(np.int16)
        combined_speech.append(speech)

    # Concatenate and save the final audio
    final_speech = np.concatenate(combined_speech, axis=0)
    sf.write(output_file, final_speech.T, 16000)

# Example usage
# text = "How are you?"
# text_to_speech(text, "generated_speech.wav")