
from transformers import AutoTokenizer, pipeline
import subprocess
import tempfile
from langid.langid import LanguageIdentifier, model


# === CONVERT THE WEBM AUDIO TO MP3 ===
def convert_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
        temp_file.write(audio_bytes)
        tempfile_path = temp_file.name
            
    output_file_path = tempfile_path.replace('.webm', '.mp3')

    command = f'ffmpeg -i {tempfile_path} -ar 16000 -ac 2 {output_file_path}'
    subprocess.run(command, shell=True)

    print("===============================================================================")
    print("Output file path:", output_file_path)
    print("===============================================================================")

    return output_file_path


def detect_language(text):
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    return identifier.classify(text)[0]
