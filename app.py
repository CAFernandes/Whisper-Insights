from flask import Flask, render_template, request, jsonify
import os
import threading
import time
from werkzeug.utils import secure_filename

# Importações refatoradas
from config import UPLOAD_FOLDER, MAX_FILE_SIZE, DEFAULT_INSIGHTS_PROMPT, OLLAMA_BASE_URL, WHISPER_MODEL_NAME
from helpers.file_utils import allowed_file # save_uploaded_file não é mais usado diretamente aqui
from services import whisper_service, ollama_service, task_service

app = Flask(__name__)
app.secret_key = 'transcritor_audio_secret_key_2025' # Pode ir para config.py

# Configurações do App a partir de config.py
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Criar pasta de uploads se não existir (agora em file_utils ou no momento do save)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def process_audio_task(file_path, task_id, original_filename):
    """
    Função principal da thread para transcrever áudio e preparar para insights.
    """
    try:
        task_service.update_task_status(task_id, status="processing", progress="Iniciando transcrição...")

        # Transcrição
        task_service.update_task_status(task_id, status="processing", progress="Transcrevendo áudio...")
        if not os.path.exists(file_path):
            task_service.update_task_status(task_id, status="error", message="Arquivo não encontrado para processamento.")
            return

        transcribed_text, error = whisper_service.transcribe_audio(file_path)

        if error:
            task_service.update_task_status(task_id, status="error", message=error)
            return

        if transcribed_text is None:
            task_service.update_task_status(task_id, status="error", message="Transcrição retornou texto vazio.")
            return

        # Verificar conexão e modelos Ollama
        available_models, ollama_conn, _ = ollama_service.get_available_ollama_models()

        task_service.update_task_status(
            task_id,
            status="transcription_completed",
            text=transcribed_text,
            message="Transcrição concluída! Pronto para gerar insights.",
            current_prompt=DEFAULT_INSIGHTS_PROMPT,
            available_ollama_models=available_models,
            ollama_connected=ollama_conn
        )

    except Exception as e:
        error_message = f"Erro durante o processamento da tarefa: {e}"
        if "ffmpeg" in str(e).lower():
            error_message += "\\nVerifique se o ffmpeg está instalado no sistema e acessível no PATH."
        task_service.update_task_status(task_id, status="error", message=error_message)

    finally:
        try:
            if os.path.exists(file_path):
                time.sleep(2)
                os.remove(file_path)
                print(f"Arquivo {file_path} removido com sucesso.")
        except Exception as e:
            print(f"Aviso: Não foi possível remover o arquivo {file_path}: {e}")

@app.route('/')
def index():
    return render_template('index.html', default_insights_prompt=DEFAULT_INSIGHTS_PROMPT)

@app.route('/check_model')
def check_model_route():
    success, message = whisper_service.load_whisper_model()
    # A mensagem de sucesso do serviço já inclui o nome do modelo.
    return jsonify({"success": success, "message": message})


@app.route('/check_ollama')
def check_ollama_route():
    models, connected, count = ollama_service.get_available_ollama_models()
    return jsonify({
        "connected": connected,
        "models": models,
        "count": count,
        "message": f"Ollama conectado com {count} modelo(s)" if connected else "Ollama não está disponível"
    })

@app.route('/upload', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "Nenhum arquivo selecionado"}), 400

    if not allowed_file(file.filename): # Usa helper
        return jsonify({"success": False, "message": "Tipo de arquivo não permitido."}), 400

    model_loaded_success, model_message = whisper_service.load_whisper_model()
    if not model_loaded_success:
        return jsonify({"success": False, "message": model_message}), 500

    task_id = task_service.create_task()
    original_filename = file.filename

    # Salvar arquivo com task_id no nome para unicidade e rastreamento
    # A pasta UPLOAD_FOLDER já é verificada/criada no início do app.py
    filename = f"{task_id}_{secure_filename(original_filename)}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(file_path)
    except Exception as e:
        task_service.update_task_status(task_id, status="error", message=f"Erro ao salvar arquivo: {e}")
        return jsonify({"success": False, "message": f"Erro ao salvar o arquivo: {e}"}), 500

    thread = threading.Thread(target=process_audio_task, args=(file_path, task_id, original_filename))
    thread.daemon = True
    thread.start()

    # Atualiza o status inicial da tarefa após o upload e início da thread
    task_service.update_task_status(task_id, status="pending_upload", message="Upload realizado. Processando...")
    return jsonify({"success": True, "task_id": task_id, "message": "Upload realizado. Processando..."})


@app.route('/status/<task_id>')
def get_status_route(task_id):
    status_info = task_service.get_task_status(task_id)
    if status_info:
        return jsonify(status_info)
    else:
        return jsonify({"status": "not_found", "message": "Tarefa não encontrada"}), 404

@app.route('/retry_insights/<task_id>', methods=['POST'])
def retry_insights_generation_route(task_id):
    task_info = task_service.get_task_status(task_id)

    if not task_info or 'text' not in task_info or task_info['text'] is None:
        return jsonify({"success": False, "message": "Tarefa ou transcrição não encontrada para gerar insights."}), 404

    if task_info.get("status") not in ["transcription_completed", "completed_with_insights", "error_insights"]:
         return jsonify({"success": False, "message": f"Não é possível gerar insights no estado atual da tarefa: {task_info.get('status')}."}), 400

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dados não enviados no corpo da requisição."}), 400

    custom_prompt = data.get('prompt', DEFAULT_INSIGHTS_PROMPT)
    selected_model = data.get('model_name')

    if not selected_model:
        return jsonify({"success": False, "message": "Nenhum modelo Ollama foi selecionado."}), 400

    transcribed_text = task_info['text']

    task_service.update_task_status(
        task_id,
        status="generating_insights",
        progress=f"Gerando insights com o modelo {selected_model}...",
        current_prompt=custom_prompt,
        selected_model=selected_model,
        insights=None # Limpa insights anteriores enquanto gera novos
    )

    # A conexão com Ollama é verificada dentro de generate_ollama_insights
    insights_text, error_message = ollama_service.generate_ollama_insights(
        transcribed_text,
        custom_prompt,
        selected_model
    )

    if error_message:
        task_service.update_task_status(
            task_id,
            status="error_insights",
            message=f"Erro ao gerar insights: {error_message}"
            # insights já foi limpo ou permanece None
        )
        return jsonify({
            "success": False,
            "message": f"Erro ao gerar insights: {error_message}",
            "current_prompt": custom_prompt, # Retorna o prompt que foi usado
            "selected_model": selected_model # Retorna o modelo que foi usado
        }), 500 # Pode ser 503 se for erro de conexão com Ollama, ou 500 para outros
    else:
        task_service.update_task_status(
            task_id,
            status="completed_with_insights",
            message="Insights gerados com sucesso!",
            insights=insights_text
            # current_prompt e selected_model já foram atualizados antes
        )
        return jsonify({
            "success": True,
            "message": "Insights gerados com sucesso!",
            "insights": insights_text,
            "current_prompt": custom_prompt,
            "selected_model": selected_model
        })

# Inicialização do modelo Whisper
print("Tentando carregar o modelo Whisper na inicialização do aplicativo...")
model_loaded, model_msg = whisper_service.load_whisper_model() # Usa WHISPER_MODEL_NAME de config.py
if model_loaded:
    print(f"Servidor Flask: {model_msg}")
else:
    print(f"Servidor Flask: AVISO - {model_msg}. O modelo será carregado na primeira requisição, se possível.")


if __name__ == '__main__':
    # A chamada para load_whisper_model() já ocorreu globalmente.
    # O Flask development server não é ideal para produção.
    app.run(debug=True, host='0.0.0.0', port=5001)
