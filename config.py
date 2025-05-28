"""
Configuration settings for the Transcriber Web App.
"""
import os

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac', 'mp4', 'avi', 'kwf'}
MAX_FILE_SIZE = 500 * 1024 * 1024 # 500 MB

# Whisper Model Configuration
WHISPER_MODEL_NAME = "base"  # ou "small", "medium", "large" conforme necessário

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_INSIGHTS_PROMPT = "Analise a seguinte transcrição e forneça um resumo dos principais pontos, identifique os principais tópicos discutidos e quaisquer ações ou decisões mencionadas. Considere o tom geral da conversa e quaisquer sentimentos expressos. O texto é: {{text}}"

# Task Management
TASK_STATUS_DICT = {} # Mantém o status das tarefas de transcrição/insights

# Outras configurações podem ser adicionadas aqui
# Por exemplo, configurações de logging, chaves de API (se aplicável no futuro), etc.
