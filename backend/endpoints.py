from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from transformers import VitsModel, AutoTokenizer
from transformers import Wav2Vec2ForCTC, AutoProcessor
from pydub import AudioSegment
import soundfile as sf
import numpy as np
import torchaudio
import uvicorn
import torch
import io


app = FastAPI()


# === TTS GENERAL ===
hg_models = {
    "san-martin": "facebook/mms-tts-qvs",
    "cuzco": "facebook/mms-tts-quz",
    "huallaga": "facebook/mms-tts-qub",
    "lambayeque": "facebook/mms-tts-quf",
    "south-bolivia": "facebook/mms-tts-quh",
    "north-bolivia": "facebook/mms-tts-qul",
    "tena-lowland": "facebook/mms-tts-quw",
    "ayacucho": "facebook/mms-tts-quy",
    "cajamarca": "facebook/mms-tts-qvc",
    "eastern-apurimac": "facebook/mms-tts-qve",
    "huamelies": "facebook/mms-tts-qvh",
    "margos-lauricocha": "facebook/mms-tts-qvm",
    "north-junin": "facebook/mms-tts-qvn",
    "huaylas": "facebook/mms-tts-qwh",
    "panao": "facebook/mms-tts-qxh",
    "northern-conchucos": "facebook/mms-tts-qxn",
    "southern-conchucos": "facebook/mms-tts-qxo",
    "salasaca-highland": "facebook/mms-tts-qxl",
    "huaylla-wanca": "facebook/mms-tts-qvw",
    "northern-pastaza": "facebook/mms-tts-qvz",
    "napo": "facebook/mms-tts-qvo",
    "canar": "facebook/mms-tts-qxr",
    "spanish": "facebook/mms-tts-spa"
}

@app.get("/tts-general")
async def tts(text, language):
    global audio_count
    try:
        default = "facebook/mms-tts-quz"

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
async def stt(data: dict):
    try:
        model_id = "facebook/mms-1b-all"
        processor = AutoProcessor.from_pretrained(model_id)
        model = Wav2Vec2ForCTC.from_pretrained(model_id)

        wav_file_path = data["file_path"]
        audio_data, original_sampling_rate = torchaudio.load(wav_file_path)
        resampled_audio_data = torchaudio.transforms.Resample(original_sampling_rate, 16000)(audio_data)

        language = data["language"]
        acronym = "spa" if language == "spanish" else "quz"

        processor.tokenizer.set_target_lang(acronym)  # -> specifying the language...
        model.load_adapter(acronym)

        inputs = processor(resampled_audio_data.numpy(), sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs).logits

        ids = torch.argmax(outputs, dim=-1)[0]
        transcription = processor.decode(ids)

        return transcription
    
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8085, log_level="info")
