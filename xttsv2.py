from TTS.api import TTS 

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
output_file_path = "output.wav"
def tts_xttsv2(text_input, speaker_audio_path, language):
    return tts.tts_to_file(text=text_input, file_path=output_file_path, speaker_wav=speaker_audio_path, language=language)