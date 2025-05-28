# Este arquivo pode ser usado para funções utilitárias, como manipulação de arquivos.
import os
import time
import logging
import threading
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, UPLOAD_FILE_MAX_AGE_MINUTES, ALLOWED_EXTENSIONS # Adicionado UPLOAD_FILE_MAX_AGE_MINUTES

# Logger para as funções de file_utils, pode usar o logger raiz configurado em app.py
# ou um logger específico se preferir granularidade.
# Por simplicidade, vamos assumir que o logger configurado em app.py é acessível
# ou que as mensagens de log aqui serão capturadas por ele se este módulo for usado por app.py.
# Se este módulo for executado de forma independente (o que não será o caso com a Opção A),
# um logger local precisaria ser configurado aqui.
logger = logging.getLogger(__name__) # Usará a configuração do logger raiz

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return file_path
    return None

def cleanup_old_files():
    logger.info(f"Iniciando verificação da pasta de uploads para limpeza: {UPLOAD_FOLDER}")
    logger.info(f"Tempo máximo de retenção de arquivo configurado: {UPLOAD_FILE_MAX_AGE_MINUTES} minutos.")

    if not os.path.isdir(UPLOAD_FOLDER):
        logger.warning(f"Diretório de uploads {UPLOAD_FOLDER} não encontrado. Limpeza ignorada.")
        return

    now = time.time()
    files_deleted_count = 0
    files_checked_count = 0

    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            files_checked_count += 1
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    file_age_seconds = now - os.path.getmtime(file_path)
                    file_age_minutes = file_age_seconds / 60

                    if file_age_minutes > UPLOAD_FILE_MAX_AGE_MINUTES:
                        os.remove(file_path)
                        files_deleted_count += 1
                        logger.info(f"Arquivo antigo excluído: {file_path} (idade: {file_age_minutes:.2f} minutos)")
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {file_path} durante a limpeza: {e}")
    except Exception as e:
        logger.error(f"Erro ao listar arquivos no diretório de uploads {UPLOAD_FOLDER}: {e}")

    if files_checked_count > 0:
        logger.info(f"Verificação de limpeza concluída. {files_checked_count} arquivos verificados, {files_deleted_count} arquivos excluídos.")
    else:
        logger.info(f"Verificação de limpeza concluída. Nenhum arquivo encontrado em {UPLOAD_FOLDER}.")

def start_cleanup_scheduler(interval_minutes=None):
    """
    Inicia um agendador em uma thread separada para limpar arquivos antigos periodicamente.
    """
    if interval_minutes is None:
        # Usa UPLOAD_FILE_MAX_AGE_MINUTES como intervalo se não especificado,
        # ou um valor fixo como 10 minutos.
        # Para garantir que a limpeza ocorra com frequência razoável em relação à idade máxima,
        # podemos usar um intervalo menor ou igual à idade máxima.
        # Se a idade máxima for muito curta (ex: 10 min), o intervalo também deve ser curto.
        interval_minutes = max(5, UPLOAD_FILE_MAX_AGE_MINUTES) # Ex: Limpa no mínimo a cada 5 min ou no tempo configurado

    logger.info(f"Agendador de limpeza de uploads iniciado. Verificando a cada {interval_minutes} minutos.")

    def scheduler_task():
        while True:
            cleanup_old_files()
            time.sleep(interval_minutes * 60) # Converte minutos para segundos

    scheduler_thread = threading.Thread(target=scheduler_task, daemon=True)
    scheduler_thread.start()
    logger.info("Thread do agendador de limpeza iniciada.")
