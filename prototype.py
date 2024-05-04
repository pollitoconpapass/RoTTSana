'''
==== THIS IS JUST THE FIRST VERSION I TRIED TO DO THE TRANSLATION PROCESS THROUGH CONSOLE ====
(idk, I like to keep it)

'''
# from backend.functions import play_audio, wav_record, translate_free  # these functions doesn't exist anymore :)
# import requests
# import html


# '''
# === FLOW PROCESS ===

# QUECHUA -> SPANISH
# 1. Record Quechua audio
# 2. Store it on a wav
# 3. Pass that wav path on the STT endpoint
# 4. Get the transcription
# 5. Translate it to Spanish
# 6. Pass that text to TTS Spanish endpoint

# SPANISH -> QUECHUA
# 1. Record Spanish Audio
# 2. Speech Recognition of Spanish (STT) endpoint
# 3. Get the text
# 4. Store it on a variable
# 5. Pass that text to TTS Quechua endpoint
# '''


# def from_spanish_to_quechua(region):
#     recording_path = wav_record()
#     stt_data = {
#         "file_path": recording_path,
#         "language": "spanish"
#     }
#     stt_response = requests.post("http://localhost:8085/stt-general", json=stt_data)

#     if stt_response.status_code == 200: 
#         print("...")
#     else: 
#         print(f"Error: {stt_response.text}")

#     transcription_es = stt_response.text
#     print(transcription_es)

#     translated_text = translate_free(transcription_es, "spa_Latn", "quy_Latn")
#     translated_text = html.unescape(translated_text)
#     tts_response = requests.get(f"http://localhost:8085/tts-general?text={translated_text}&language={region}")
    
#     if tts_response.status_code == 200: 
#         print("...")
#         play_audio(tts_response.content)
#         print("Hecho!!")
#     else: 
#         print(f"Error: {tts_response.text}")
    

# def from_quechua_to_spanish():
#     recording_path = wav_record()
#     stt_data = {
#         "file_path": recording_path, 
#         "language": "quechua"
#     }
#     stt_response = requests.post("http://localhost:8000/stt-general", json=stt_data)

#     if stt_response.status_code == 200: 
#         print("...")
#     else: 
#         print(f"Error: {stt_response.text}")

#     transcription_qu = stt_response.text
#     print(transcription_qu)

#     translated_text = translate_free(transcription_qu, "quy_Latn", "spa_Latn")
#     translated_text = html.unescape(translated_text)
#     tts_response = requests.get(f"http://localhost:8000/tts-general?text={translated_text}&language=spanish")
    
#     if tts_response.status_code == 200: 
#         print("...")
#         play_audio(tts_response.content)
#         print("Ñam!!")
#     else: 
#         print(f"Error: {tts_response.text}")


# def main(): 
#     while True:
#         print("\nSelect the language you're gonna speak:")
#         print("1. Spanish")
#         print("2. Quechua")
#         opt = int(input("\nEnter your option:   "))

#         if opt == 1:
#             from_spanish_to_quechua("ayacucho")
#         elif opt == 2:
#             from_quechua_to_spanish()
#         else:
#             print("Invalid option\n")


# if __name__ == "__main__":
#     main()
