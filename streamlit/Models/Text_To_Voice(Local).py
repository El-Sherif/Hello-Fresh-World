import numpy as np
import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import soundfile as sf

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

def text_to_speech(text, output_file="output.wav"):
    if len(text.strip()) == 0:
        return

    # Processing the text
    inputs = processor(text=text, return_tensors="pt")
    input_ids = inputs["input_ids"]
    input_ids = input_ids[..., :model.config.max_text_positions]

    # Default speaker set to CLB (female)
    speaker_embedding = np.load(speaker_embeddings["CLB"])
    speaker_embedding = torch.tensor(speaker_embedding).unsqueeze(0)

    # Generating speech
    speech = model.generate_speech(input_ids, speaker_embedding, vocoder=vocoder)
    speech = (speech.numpy() * 32767).astype(np.int16)

    # Saving the speech to a file
    sf.write(output_file, speech.T, 16000)

# Example usage
text = "How are you?"
text_to_speech(text, "generated_speech.wav")