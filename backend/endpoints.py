from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import VitsModel, AutoTokenizer, pipeline
from transformers import Wav2Vec2ForCTC, AutoProcessor
from pydub import AudioSegment
from functions import convert_audio, detect_language
import soundfile as sf
import numpy as np
import torchaudio
import uvicorn
import torch
import io


app = FastAPI()
origins = [
    "http://localhost:3000",  # React application running on localhost:3000
    "http://192.168.18.148:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === TTS GENERAL ===
hg_models = {
    "qu": "facebook/mms-tts-quy",  # -> Quechua Ayacucho (Chanka)
    "es": "facebook/mms-tts-spa"
}

@app.post("/tts-general")
async def tts(data: dict):
    try:
        text = data["text"]
        language = detect_language(text)
        print(language)
        default = "facebook/mms-tts-quy"

        # Verifica si hay una GPU disponible y configura PyTorch para usarla
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")


        # === LOAD THE HUGGING FACE MODELS ===
        selected_language = hg_models.get(language, default)  
        model = VitsModel.from_pretrained(selected_language)  # -> loads the model itself
        tokenizer = AutoTokenizer.from_pretrained(selected_language)   # ... token

        # === GENERATE THE AUDIO FILE ===
        inputs = tokenizer(text, return_tensors="pt") 

        with torch.no_grad():  # -> ensures no gradients (as only inference)
            output = model(**inputs).waveform.cpu().numpy()  # -> generates the audio w model and inputs
        output = output / np.max(np.abs(output))  # -> normalizes the waveform

        # Convert to IOBytes WAV first
        wav_io = io.BytesIO()
        sf.write(wav_io, output.T, samplerate=16000, format='WAV', subtype='PCM_16')
        wav_io.seek(0)  # Back to the beginnning of BytesIO

        # Convert to MP3 with pydub
        audio_segment = AudioSegment.from_file(wav_io, format="wav")
        mp3_io = io.BytesIO()
        audio_segment.export(mp3_io, format="mp3")
        mp3_io.seek(0)  # Back to the beginnning of BytesIO

        # Create the Streaming Response
        headers = {"Content-Disposition": "attachment; filename=output.mp3"}
        response = StreamingResponse(mp3_io, headers=headers, media_type="audio/mp3")

        return response
    
    except Exception as e:
        return {"error": str(e)}
	

# === STT GENERAL ===
@app.post("/stt-general")
async def stt(audio_file: UploadFile = File(...)):
    try:
        audio_bytes = await audio_file.read()
        audio_data = convert_audio(audio_bytes)

        model_id = "facebook/mms-1b-all"
        processor = AutoProcessor.from_pretrained(model_id)
        model = Wav2Vec2ForCTC.from_pretrained(model_id)

        audio_data, original_sampling_rate = torchaudio.load(audio_data)
        resampled_audio_data = torchaudio.transforms.Resample(original_sampling_rate, 16000)(audio_data)

        inputs = processor(resampled_audio_data.numpy(), sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs).logits

        ids = torch.argmax(outputs, dim=-1)[0]
        transcription = processor.decode(ids)

        return transcription
    
    except Exception as e:
        return {"error": str(e)}
    

# === TRANSLATION ENDPOINT ===
@app.post("/translate-free")
def translate_free(data: dict):
    text = data["text"]
    language = detect_language(text)
    print("LANGUAGE DETECTED: ", language)

    src_language = "spa_Latn" if language == "es" else "quy_Latn"
    target_language = "quy_Latn" if language == "es" else "spa_Latn"
    print(f"{src_language} -> {target_language}")
 
    model = 'facebook/nllb-200-distilled-600M'
    tokenizer = AutoTokenizer.from_pretrained(model)

    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=src_language, tgt_lang=target_language)
    output = translator(text, max_length=400)
    return output[0]['translation_text']
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8085, log_level="info")
