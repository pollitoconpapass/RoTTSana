import os
import pygame
import speech_recognition
from io import BytesIO
from google.cloud import translate_v2 as translate


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jose/Downloads/massive-catfish-411714-89ecb4eed938.json"

# === TRANSLATE TO QUECHUA OR SPANISH === 
def translate_text(text, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]

    print(f"Translated text to {target_language}: {translated_text}")
    return translated_text


# === TO PLAY THE AUDIO ===
def play_audio(audio_content):
    pygame.mixer.init()
    pygame.mixer.music.load(BytesIO(audio_content))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# === TO RECORD A WAV FILE ===
def wav_record():
    r = speech_recognition.Recognizer()
    count = 1

    while True:
        print("Recording... (Press Enter to stop)")
        with speech_recognition.Microphone() as source:
            audio = r.listen(source)

            if (input() == ""): 
                print("Finish Recording! Saving...")
                file_name = f"recordings/recorded_audio_{count}.wav"
                with open(file_name, "wb") as f:
                    f.write(audio.get_wav_data())

                break
        
        count += 1

    return os.getcwd() + f"/{file_name}"
