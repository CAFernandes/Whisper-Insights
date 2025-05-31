from flask import Flask, render_template, request, jsonify
import os
import threading
import time
from werkzeug.utils import secure_filename
import logging # Adicionado

# Configuração básica do logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"), # Salva logs em um arquivo
                        logging.StreamHandler() # Mostra logs no console
                    ])
logger = logging.getLogger(__name__) # Adicionado

# Importações refatoradas
from config import (
    UPLOAD_FOLDER, MAX_FILE_SIZE, DEFAULT_INSIGHTS_PROMPT,
    OLLAMA_BASE_URL, WHISPER_MODEL_NAME, ALLOWED_EXTENSIONS, UPLOAD_FILE_MAX_AGE_MINUTES # Adicionado UPLOAD_FILE_MAX_AGE_MINUTES
)
from helpers.file_utils import allowed_file, start_cleanup_scheduler # Modificado
from services import whisper_service, ollama_service, task_service

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'transcritor_audio_secret_key_2025') # Carrega do .env

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
            logger.error(f"Task {task_id}: Arquivo {file_path} não encontrado para processamento.") # Adicionado
            return

        # Executar transcrição com diarização se solicitado
        include_diarization = task_service.get_task_option(task_id, 'include_diarization', False)
        transcription_result, error = whisper_service.transcribe_audio(
            file_path,
            include_timestamps=True,
            include_diarization=include_diarization
        )

        if error:
            task_service.update_task_status(task_id, status="error", message=error)
            logger.error(f"Task {task_id}: Erro na transcrição Whisper: {error}")
            return

        if transcription_result is None:
            task_service.update_task_status(task_id, status="error", message="Transcrição retornou resultado vazio.")
            logger.error(f"Task {task_id}: Transcrição retornou resultado vazio para o arquivo {original_filename}.")
            return

        # Extrair texto principal para compatibilidade
        transcribed_text = transcription_result.get('text', '')

        # Verificar conexão e modelos Ollama
        available_models, ollama_conn, _ = ollama_service.get_available_ollama_models()

        task_service.update_task_status(
            task_id,
            status="transcription_completed",
            text=transcribed_text,
            transcription_data=transcription_result,  # Dados completos da transcrição
            message="Transcrição concluída! Pronto para gerar insights.",
            current_prompt=DEFAULT_INSIGHTS_PROMPT,
            available_ollama_models=available_models,
            ollama_connected=ollama_conn
        )

    except FileNotFoundError as fnf_error:
        error_message = f"Erro: Arquivo não encontrado durante o processamento da tarefa: {fnf_error}"
        logger.error(f"Task {task_id}: {error_message}")
        task_service.update_task_status(task_id, status="error", message=error_message)
    except ConnectionError as conn_error: # Exemplo para erros de conexão (ajustar conforme os serviços)
        error_message = f"Erro de conexão durante o processamento da tarefa: {conn_error}"
        logger.error(f"Task {task_id}: {error_message}")
        task_service.update_task_status(task_id, status="error", message=error_message)
    except Exception as e:
        error_message = f"Erro inesperado durante o processamento da tarefa: {e}"
        if "ffmpeg" in str(e).lower():
            error_message += "\\nVerifique se o ffmpeg está instalado no sistema e acessível no PATH."
        logger.exception(f"Task {task_id}: {error_message}") # Usar logger.exception para incluir o stack trace
        task_service.update_task_status(task_id, status="error", message=error_message)

    finally:
        try:
            if os.path.exists(file_path):
                time.sleep(2)
                os.remove(file_path)
                logger.info(f"Task {task_id}: Arquivo {file_path} removido com sucesso.") # Modificado
        except Exception as e:
            logger.warning(f"Task {task_id}: Aviso - Não foi possível remover o arquivo {file_path}: {e}") # Modificado

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

    # Processa parâmetro de diarização
    enable_diarization = request.form.get('enable_diarization', 'false').lower() == 'true'
    task_service.set_task_option(task_id, 'include_diarization', enable_diarization)

    # Salvar arquivo com task_id no nome para unicidade e rastreamento
    # A pasta UPLOAD_FOLDER já é verificada/criada no início do app.py
    filename = f"{task_id}_{secure_filename(original_filename)}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(file_path)
        logger.info(f"Task {task_id}: Arquivo {original_filename} salvo como {file_path}.") # Adicionado
    except Exception as e:
        logger.error(f"Task {task_id}: Erro ao salvar o arquivo {original_filename}: {e}") # Adicionado
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
        logger.warning(f"Task {task_id}: Tentativa de gerar insights sem transcrição.") # Adicionado
        return jsonify({"success": False, "message": "Tarefa ou transcrição não encontrada para gerar insights."}), 404

    if task_info.get("status") not in ["transcription_completed", "completed_with_insights", "error_insights"]:
        logger.warning(f"Task {task_id}: Tentativa de gerar insights no estado inválido {task_info.get('status')}.") # Adicionado
        return jsonify({"success": False, "message": f"Não é possível gerar insights no estado atual da tarefa: {task_info.get('status')}."}), 400

    data = request.get_json()
    if not data:
        logger.warning(f"Task {task_id}: Tentativa de gerar insights sem dados no corpo da requisição.") # Adicionado
        return jsonify({"success": False, "message": "Dados não enviados no corpo da requisição."}), 400

    custom_prompt = data.get('prompt', DEFAULT_INSIGHTS_PROMPT)
    selected_model = data.get('model_name')

    if not selected_model:
        logger.warning(f"Task {task_id}: Tentativa de gerar insights sem selecionar modelo Ollama.") # Adicionado
        return jsonify({"success": False, "message": "Nenhum modelo Ollama foi selecionado."}), 400

    # Escolher melhor fonte de texto para insights: diarização > timestamps > texto simples
    transcribed_text = task_info['text']
    text_source = "texto simples"

    # Verificar se há dados de transcrição completos disponíveis
    transcription_data = task_info.get('transcription_data', {})

    # Priorizar texto com diarização (mais contexto)
    if transcription_data.get('speakers_text'):
        transcribed_text = transcription_data['speakers_text']
        text_source = "transcrição com identificação de locutores"
        logger.info(f"Task {task_id}: Usando texto com diarização para insights (melhor contexto)")
    # Segunda opção: texto com timestamps
    elif transcription_data.get('timestamped_text'):
        transcribed_text = transcription_data['timestamped_text']
        text_source = "transcrição com timestamps"
        logger.info(f"Task {task_id}: Usando texto com timestamps para insights")
    # Fallback: texto simples (já definido acima)
    else:
        logger.info(f"Task {task_id}: Usando texto simples para insights")

    task_service.update_task_status(
        task_id,
        status="generating_insights",
        progress=f"Gerando insights com o modelo {selected_model} baseado em {text_source}...",
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
        logger.error(f"Task {task_id}: Erro ao gerar insights com Ollama: {error_message}") # Adicionado
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
        logger.info(f"Task {task_id}: Insights gerados com sucesso com o modelo {selected_model}.") # Adicionado
        return jsonify({
            "success": True,
            "message": "Insights gerados com sucesso!",
            "insights": insights_text,
            "current_prompt": custom_prompt,
            "selected_model": selected_model
        })

@app.route('/toggle_diarization/<task_id>', methods=['POST'])
def toggle_diarization_route(task_id):
    """
    Ativa ou desativa a diarização para uma tarefa específica.
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Dados não enviados."}), 400

    enable_diarization = data.get('enable_diarization', False)

    # Salvar opção da tarefa
    task_service.set_task_option(task_id, 'include_diarization', enable_diarization)

    return jsonify({
        "success": True,
        "message": f"Diarização {'ativada' if enable_diarization else 'desativada'} para esta tarefa."
    })

@app.route('/get_transcription_formats/<task_id>')
def get_transcription_formats_route(task_id):
    """
    Retorna diferentes formatos da transcrição (simples, com timestamps, com diarização).
    """
    task_info = task_service.get_task_status(task_id)

    if not task_info or 'transcription_data' not in task_info:
        return jsonify({"success": False, "message": "Dados de transcrição não encontrados."}), 404

    transcription_data = task_info['transcription_data']

    formats = {
        'simple_text': transcription_data.get('text', ''),
        'with_timestamps': transcription_data.get('formatted_text', ''),
        'language': transcription_data.get('language', 'pt')
    }

    # Se há dados de diarização
    if 'diarization' in transcription_data:
        formats['with_speakers'] = transcription_data.get('combined_text', '')
        formats['speakers_only'] = transcription_data.get('diarization_text', '')
        formats['speakers_summary'] = transcription_data.get('speakers_summary', {})
        formats['has_diarization'] = True
    else:
        formats['has_diarization'] = False
        if 'diarization_error' in transcription_data:
            formats['diarization_error'] = transcription_data['diarization_error']

    return jsonify({"success": True, "formats": formats})

@app.route('/check_diarization_availability')
def check_diarization_availability_route():
    """
    Verifica se o serviço de diarização está disponível.
    """
    from services.diarization_service import is_diarization_available

    available = is_diarization_available()

    return jsonify({
        "available": available,
        "message": "Diarização disponível" if available else "Diarização não disponível - verifique as dependências"
    })

@app.route('/test_dialogue', methods=['GET'])
def test_dialogue():
    """Endpoint de teste para a visualização do diálogo com dados sintéticos."""
    import json

    # Dados sintéticos de diarização para teste
    synthetic_data = {
        'text': 'Olá, como você está? Estou bem, obrigado. E você? Também estou bem. Que bom!',
        'speakers_text': 'SPEAKER_00: Olá, como você está?\nSPEAKER_01: Estou bem, obrigado. E você?\nSPEAKER_00: Também estou bem.\nSPEAKER_01: Que bom!',
        'timestamped_text': '[00:00] Olá, como você está? [00:03] Estou bem, obrigado. E você? [00:06] Também estou bem. [00:08] Que bom!',
        'speakers_summary': {
            'speakers': [
                {
                    'label': 'SPEAKER_00',
                    'total_duration': 5.5,
                    'percentage': 60
                },
                {
                    'label': 'SPEAKER_01',
                    'total_duration': 3.7,
                    'percentage': 40
                }
            ],
            'total_speakers': 2,
            'total_duration': 9.2,
            'total_segments': 4
        },
        'transcription_data': {
            'segments': [
                {
                    'speaker': 'SPEAKER_00',
                    'text': 'Olá, como você está?',
                    'start': 0.0,
                    'end': 2.5
                },
                {
                    'speaker': 'SPEAKER_01',
                    'text': 'Estou bem, obrigado. E você?',
                    'start': 2.8,
                    'end': 5.2
                },
                {
                    'speaker': 'SPEAKER_00',
                    'text': 'Também estou bem.',
                    'start': 5.5,
                    'end': 7.0
                },
                {
                    'speaker': 'SPEAKER_01',
                    'text': 'Que bom!',
                    'start': 7.3,
                    'end': 8.5
                }
            ]
        },
        'available_ollama_models': ['llama3.2:3b', 'mistral:latest', 'phi3:latest'],
        'current_prompt': 'Prompt de teste para insights.'
    }

    return jsonify(synthetic_data)

# Inicialização do modelo Whisper
logger.info("Tentando carregar o modelo Whisper na inicialização do aplicativo...") # Modificado
model_loaded, model_msg = whisper_service.load_whisper_model() # Usa WHISPER_MODEL_NAME de config.py
if model_loaded:
    logger.info(f"Servidor Flask: {model_msg}") # Modificado
else:
    logger.warning(f"Servidor Flask: AVISO - {model_msg}. O modelo será carregado na primeira requisição, se possível.") # Modificado


if __name__ == '__main__':
    # A chamada para load_whisper_model() já ocorreu globalmente.
    # O Flask development server não é ideal para produção.
    port = int(os.getenv('FLASK_RUN_PORT', 5001))
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Iniciar o agendador de limpeza de uploads
    # O intervalo pode ser o mesmo que UPLOAD_FILE_MAX_AGE_MINUTES ou um valor fixo.
    # Se UPLOAD_FILE_MAX_AGE_MINUTES for 10, ele verificará a cada 10 minutos.
    start_cleanup_scheduler(interval_minutes=UPLOAD_FILE_MAX_AGE_MINUTES)

    app.run(debug=debug_mode, host='0.0.0.0', port=port)
