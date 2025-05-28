import os
import time
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env que está no mesmo diretório do config.py
# Supondo que cleanup_uploads.py está na raiz do projeto, assim como o .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Importar configurações DEPOIS de carregar o .env
# Para isso, precisamos garantir que o config.py possa ser importado.
# Adicionaremos o diretório do projeto ao sys.path temporariamente se necessário,
# ou podemos reestruturar para que config seja mais facilmente acessível.
# Por simplicidade aqui, vamos tentar importar diretamente, assumindo que o PYTHONPATH pode estar configurado
# ou que o script será executado do diretório raiz.

# Uma forma mais robusta de importar config:
import sys
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from config import UPLOAD_FOLDER, UPLOAD_FILE_MAX_AGE_MINUTES

# Configuração do logging para o script de limpeza
log_file_path = os.path.join(project_root, 'cleanup.log')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file_path),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def cleanup_old_files():
    logger.info(f"Iniciando verificação da pasta de uploads: {UPLOAD_FOLDER}")
    logger.info(f"Tempo máximo de retenção de arquivo: {UPLOAD_FILE_MAX_AGE_MINUTES} minutos.")

    if not os.path.isdir(UPLOAD_FOLDER):
        logger.warning(f"Diretório de uploads {UPLOAD_FOLDER} não encontrado. Saindo.")
        return

    now = time.time()
    files_deleted_count = 0
    files_checked_count = 0

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
            logger.error(f"Erro ao processar o arquivo {file_path}: {e}")

    logger.info(f"Verificação concluída. {files_checked_count} arquivos verificados, {files_deleted_count} arquivos excluídos.")

if __name__ == "__main__":
    logger.info("Script de limpeza de uploads iniciado manualmente.")
    cleanup_old_files()
    logger.info("Script de limpeza de uploads concluído.")
