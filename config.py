"""
Configuration settings for the Transcriber Web App.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

# File Upload Configuration
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads'))
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'mp3,wav,m4a,ogg,flac,mp4,avi,kwf').split(','))
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE_MB', 500)) * 1024 * 1024  # Em MB, convertido para Bytes
UPLOAD_FILE_MAX_AGE_MINUTES = int(os.getenv('UPLOAD_FILE_MAX_AGE_MINUTES', 10))

# Whisper Model Configuration
WHISPER_MODEL_NAME = os.getenv('WHISPER_MODEL_NAME', "base")

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_API_URL', "http://localhost:11434")
DEFAULT_INSIGHTS_PROMPT = os.getenv('DEFAULT_INSIGHTS_PROMPT', "Analise a seguinte transcrição e forneça um resumo dos principais pontos, identifique os principais tópicos discutidos e quaisquer ações ou decisões mencionadas. Considere o tom geral da conversa e quaisquer sentimentos expressos. O texto é: {{text}}")
OLLAMA_REQUEST_TIMEOUT_SECONDS = int(os.getenv('OLLAMA_REQUEST_TIMEOUT_SECONDS', 300))

# Task Management
TASK_STATUS_DICT = {} # Mantém o status das tarefas de transcrição/insights

# Outras configurações podem ser adicionadas aqui
# Por exemplo, configurações de logging, chaves de API (se aplicável no futuro), etc.
