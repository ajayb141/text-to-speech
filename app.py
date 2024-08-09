import gradio as gr
from parler import tts_parler
from bark_text import tts_bark_text
from bark_text_audio import tts_bark_text_audio
from xttsv2 import tts_xttsv2
from dotenv import load_dotenv 
import os
load_dotenv()

bark_languages = {
    "English": "v2/en_speaker_0",
    "Chinese": "v2/zh_speaker_2",
    "French": "v2/fr_speaker_1",
    "German": "v2/de_speaker_6",
    "Hindi": "v2/hi_speaker_3",
    "Italian": "v2/it_speaker_4",
    "Japanese": "v2/ja_speaker_2",
    "Korean": "v2/ko_speaker_5",
    "Russian": "v2/ru_speaker_0",
}

xtts_language = {"English": "en", "French": "fr", "Hindi": "hi"}


def bark_preset_lang(text, voice_preset):
    return tts_bark_text_audio(text, bark_languages[voice_preset])


def xtts_lang(text, audio, lang):
    return tts_xttsv2(text, audio, xtts_language[lang])


with gr.Blocks() as trail:
    with gr.Tab("Parler-TTS"):
        gr.Interface(
            fn=tts_parler,
            inputs=["text", "text"],
            outputs="audio",
            examples=[
                [
                    "Remember - this is only the first iteration of the model! To improve the prosody and naturalness of the speech further, we're scaling up the amount of training data by a factor of five times.",
                    "A male speaker with a low-pitched voice delivering his words at a fast pace in a small, confined space with a very clear audio and an animated tone.",
                ],
                [
                    "'This is the best time of my life, Bartley,' she said happily.",
                    "A female speaker with a slightly low-pitched, quite monotone voice delivers her words at a slightly faster-than-average pace in a confined space with very clear audio.",
                ],
                [
                    "Montrose also, after having experienced still more variety of good and bad fortune, threw down his arms, and retired out of the kingdom.",
                    "A male speaker with a slightly high-pitched voice delivering his words at a slightly slow pace in a small, confined space with a touch of background noise and a quite monotone tone.",
                ],
                [
                    "Montrose also, after having experienced still more variety of good and bad fortune, threw down his arms, and retired out of the kingdom.",
                    "A male speaker with a low-pitched voice delivers his words at a fast pace, in a very spacious environment, accompanied by noticeable background noise.",
                ],
            ],
            title="Text to Speech using Parler-mini",
            description="Enter the Prompt for audio and describe the speaker's voice",
            allow_flagging=False,
        )
    with gr.Tab("Suno/bark-Prompt"):
        gr.Interface(
            fn=tts_bark_text,
            inputs="text",
            outputs="audio",
            examples=[
                ["'This is the best time of my life, Bartley,' she said happily."],
                ["Montrose also, after having experienced still more variety of good and bad fortune, threw down his arms, and retired out of the kingdom."],
                [
                    "Les progrès technologiques ont conduit à des changements importants dans la société. La plus ancienne technologie connue est l'outil en pierre, utilisé à l'époque préhistorique, suivi par le contrôle du feu, qui a contribué à la croissance du cerveau humain et au développement du langage pendant la période glaciaire"
                ],
            ],
            title="Text to Speech using suno/bark-Text",
            allow_flagging=False,
        )
    with gr.Tab("Suno/bark-Prompt_voice"):
        gr.Interface(
            fn=bark_preset_lang,
            inputs=["text", gr.Dropdown(label="Language", choices=list(bark_languages.keys()))],
            outputs="audio",
            examples=[
                ["Montrose also, after having experienced still more variety of good and bad fortune, threw down his arms, and retired    out of the kingdom."],
                ["技术进步给社会带来了重大变化。已知最早的技术是石器。"],
                [
                    "Les progrès technologiques ont conduit à des changements importants dans la société. La plus ancienne technologie connue est l'outil en pierre."
                ],
                [
                    "Der technologische Fortschritt hat zu erheblichen Veränderungen in der Gesellschaft geführt. Die früheste bekannte Technologie ist das Steinwerkzeug."
                ],
                ["तकनीकी प्रगति ने समाज में महत्वपूर्ण परिवर्तन लाये हैं। सबसे प्रारंभिक ज्ञात तकनीक पत्थर का उपकरण है।"],
                ["I progressi tecnologici hanno portato a cambiamenti significativi nella società. La prima tecnologia conosciuta è lo strumento di pietra."],
                ["テクノロジーの進歩は社会に大きな変化をもたらしました。知られている最古の技術は石器です。"],
                ["기술의 발전은 사회에 큰 변화를 가져왔습니다. 가장 먼저 알려진 기술은 석기 도구입니다."],
                ["Технологические достижения привели к значительным изменениям в обществе. Самая ранняя известная технология - каменный инструмент."],
            ],
            title="Text to Speech using suno/bark-Prompt_voice",
            description="For voice preset supported languages are en(English),zh(Chinese),fr(French),de(German),hi(Hindi),it(Italian),ja(Japanese),ko(Korean) and ru(Russian). According to the text language, You need to set voice preset.You can set from 0 to 9.",
            allow_flagging=False,
        )
    with gr.Tab("XTTS_V2"):
        audio_input = ["text", gr.Audio(type="filepath"), gr.Dropdown(label="Language", choices=list(xtts_language.keys()))]
        audio_output = gr.Audio(type="filepath", label="Generated Audio")
        gr.Interface(
            fn=xtts_lang,
            inputs=audio_input,
            outputs=audio_output,
            examples=[
                [
                    "Technological advancements have led to significant changes in society. The earliest known technology is the stone tool, used during prehistoric times, followed by the control of fire, which contributed to the growth of the human brain and the development of language during the Ice Age. The invention of the wheel in the Bronze Age allowed greater travel and the creation of more complex machines. More recent technological inventions, including the printing press, telephone, and the Internet, have lowered barriers to communication and ushered in the knowledge economy.",
                    os.path.join(os.getenv("TEXT_TO_SPEECH_IO"),"examples/English.mp3")
                ],
                [
                    "भूगोल प्रवेशद्वार में आपका स्वागत् हैं। भूगोल एक अत्यधिक पुराना, रोचक तथा ज्ञानवर्धक विषय रहा हैं। वर्तमान में इसका महत्व अत्यधिक बढ़ गया हैं जहां एक ओर पारिस्थितिकी, स्थलाकृति, जलवायु, भूमंडलीय ऊष्मीकरण, महासागर जैसे भौतिक भूगोल के प्रमुख उप-विषय हैं वही दूसरी ओर संसाधन, पर्यटन, जनसंख्या, सांस्कृतिक, धर्म, कृषि जैसे विषय मानव भूगोल के उप-विषय हैं। भूगोल में नयी तकनीकों जैसे, रिमोट सेंसिंग, जीआईएस और डिजिटल कार्टोग्राफी के अधुनातन प्रयोगों ने इसकी उपयोगिता को पहले स",
                    os.path.join(os.getenv("TEXT_TO_SPEECH_IO"),"examples/Hindi.wav")
                ],
                [
                    "Les progrès technologiques ont conduit à des changements importants dans la société. La plus ancienne technologie connue est l'outil en pierre, utilisé à l'époque préhistorique, suivi par le contrôle du feu, qui a contribué à la croissance du cerveau humain et au développement du langage pendant la période glaciaire. L'invention de la roue à l'âge du bronze a permis de plus grands déplacements et la création de machines plus complexes. Des inventions technologiques plus récentes, notamment l'imprimerie, le téléphone et Internet, ont abaissé les barrières à la communication et ont ouvert la voie à l'économie du savoir.",
                    os.path.join(os.getenv("TEXT_TO_SPEECH_IO"),"examples/French.wav")
                ],
            ],
            title="Text-to-Speech using xtts_v2",
            description="Enter text and upload a speaker audio file to generate speech.",
            allow_flagging=False,
        )
trail.launch()
