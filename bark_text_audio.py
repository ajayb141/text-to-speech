from transformers import BarkModel, AutoProcessor
import torch
import scipy

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = BarkModel.from_pretrained("suno/bark-small").to(device)
processor = AutoProcessor.from_pretrained("suno/bark")

def tts_bark_text_audio(text_prompt, voice_preset):
    inputs = processor(text_prompt, voice_preset=voice_preset, return_tensors="pt")
    inputs = inputs.to(device)
    speech_output = model.generate(**inputs)
    sampling_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write("output.wav", rate=sampling_rate, data=speech_output[0].cpu().numpy())
    return "output.wav"
