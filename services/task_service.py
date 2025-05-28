# Serviço para gerenciar o status das tarefas de transcrição e insights
import uuid
from config import TASK_STATUS_DICT, DEFAULT_INSIGHTS_PROMPT

def create_task():
    task_id = str(uuid.uuid4())
    TASK_STATUS_DICT[task_id] = {
        "status": "pending",
        "message": "Tarefa criada",
        "progress": "0%",
        "text": None,
        "insights": None,
        "transcription_data": None,
        "current_prompt": DEFAULT_INSIGHTS_PROMPT,
        "selected_model": None,
        "available_ollama_models": [],
        "ollama_connected": False,
        "options": {}
    }
    return task_id

def update_task_status(task_id, status, message=None, progress=None, text=None, insights=None, current_prompt=None, selected_model=None, available_ollama_models=None, ollama_connected=None, transcription_data=None):
    if task_id in TASK_STATUS_DICT:
        task = TASK_STATUS_DICT[task_id]
        task["status"] = status
        if message is not None: task["message"] = message
        if progress is not None: task["progress"] = progress
        if text is not None: task["text"] = text
        if insights is not None: task["insights"] = insights
        if current_prompt is not None: task["current_prompt"] = current_prompt
        if selected_model is not None: task["selected_model"] = selected_model
        if available_ollama_models is not None: task["available_ollama_models"] = available_ollama_models
        if ollama_connected is not None: task["ollama_connected"] = ollama_connected
        if transcription_data is not None: task["transcription_data"] = transcription_data
        return True
    return False

def get_task_status(task_id):
    return TASK_STATUS_DICT.get(task_id)

def set_task_option(task_id, option_name, option_value):
    """
    Define uma opção específica para uma tarefa.
    """
    if task_id in TASK_STATUS_DICT:
        if "options" not in TASK_STATUS_DICT[task_id]:
            TASK_STATUS_DICT[task_id]["options"] = {}
        TASK_STATUS_DICT[task_id]["options"][option_name] = option_value
        return True
    return False

def get_task_option(task_id, option_name, default_value=None):
    """
    Obtém uma opção específica de uma tarefa.
    """
    if task_id in TASK_STATUS_DICT and "options" in TASK_STATUS_DICT[task_id]:
        return TASK_STATUS_DICT[task_id]["options"].get(option_name, default_value)
    return default_value
