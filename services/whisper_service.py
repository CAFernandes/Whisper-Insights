# Serviço para interagir com o modelo Whisper para transcrição de áudio
import whisper
from config import WHISPER_MODEL_NAME

loaded_model = None

def load_whisper_model():
    global loaded_model
    if loaded_model is None:
        try:
            loaded_model = whisper.load_model(WHISPER_MODEL_NAME)
            print(f"Modelo Whisper '{WHISPER_MODEL_NAME}' carregado com sucesso.")
            return True, f"Modelo Whisper '{WHISPER_MODEL_NAME}' carregado e pronto."
        except Exception as e:
            print(f"Erro ao carregar o modelo Whisper: {e}")
            return False, f"Erro ao carregar o modelo Whisper: {e}"
    return True, f"Modelo Whisper '{WHISPER_MODEL_NAME}' já carregado."

def transcribe_audio(file_path):
    global loaded_model
    if loaded_model is None:
        return None, "Modelo Whisper não carregado."
    try:
        result = loaded_model.transcribe(file_path)
        return result["text"], None
    except Exception as e:
        return None, f"Erro durante a transcrição: {e}"
