# Serviço para interagir com o modelo Whisper para transcrição de áudio
import whisper
import logging
from config import WHISPER_MODEL_NAME
from .diarization_service import perform_diarization, get_speakers_summary, format_diarization_for_display

logger = logging.getLogger(__name__)
loaded_model = None

def load_whisper_model():
    global loaded_model
    if loaded_model is None:
        try:
            loaded_model = whisper.load_model(WHISPER_MODEL_NAME)
            logger.info(f"Modelo Whisper '{WHISPER_MODEL_NAME}' carregado com sucesso.")
            return True, f"Modelo Whisper '{WHISPER_MODEL_NAME}' carregado e pronto."
        except Exception as e:
            logger.error(f"Erro ao carregar o modelo Whisper: {e}")
            return False, f"Erro ao carregar o modelo Whisper: {e}"
    return True, f"Modelo Whisper '{WHISPER_MODEL_NAME}' já carregado."

def transcribe_audio(file_path, include_timestamps=True, include_diarization=False):
    """
    Transcreve áudio com opções para timestamps e diarização de locutores.

    Args:
        file_path (str): Caminho para o arquivo de áudio
        include_timestamps (bool): Se deve incluir informações de tempo
        include_diarization (bool): Se deve incluir identificação de locutores

    Returns:
        tuple: (transcription_result, error_message)
    """
    global loaded_model
    if loaded_model is None:
        return None, "Modelo Whisper não carregado."

    try:
        logger.info(f"Iniciando transcrição de: {file_path}")

        # Detectar se é arquivo kwf e tratá-lo especialmente
        is_kwf = file_path.lower().endswith('.kwf')

        # Parâmetros de transcrição ajustados para diferentes formatos
        transcribe_params = {
            'fp16': False,
            'word_timestamps': include_timestamps,
            'language': 'pt'  # Forçar português para melhor precisão
        }

        # Para arquivos kwf, usar parâmetros mais conservadores
        if is_kwf:
            logger.info("Detectado arquivo KWF, usando parâmetros otimizados...")
            transcribe_params['beam_size'] = 1  # Reduzir complexidade
            transcribe_params['best_of'] = 1

        # Transcrição com tratamento de erro específico
        try:
            result = loaded_model.transcribe(file_path, **transcribe_params)
        except Exception as whisper_error:
            # Se o erro for relacionado ao 'src', tentar abordagem alternativa
            if "'src'" in str(whisper_error) or "Cannot set attribute" in str(whisper_error):
                logger.warning(f"Erro específico detectado, tentando abordagem alternativa: {whisper_error}")
                # Remover timestamps para resolver problema de compatibilidade
                transcribe_params['word_timestamps'] = False
                include_timestamps = False  # Desabilitar timestamps
                result = loaded_model.transcribe(file_path, **transcribe_params)
            else:
                raise whisper_error

        transcription_data = {
            'text': result["text"],
            'language': result.get("language", "pt"),
            'segments': result.get("segments", [])
        }

        # Se timestamps foram solicitados, formatar melhor
        if include_timestamps and 'segments' in result:
            transcription_data['timestamped_text'] = format_transcription_with_timestamps(result['segments'])

        # Se diarização foi solicitada, executar
        if include_diarization:
            logger.info("Executando diarização de locutores...")
            diarization_segments, diar_error = perform_diarization(file_path)

            if diar_error:
                logger.warning(f"Erro na diarização: {diar_error}")
                transcription_data['diarization_error'] = diar_error
            else:
                transcription_data['diarization'] = diarization_segments
                transcription_data['speakers_summary'] = get_speakers_summary(diarization_segments)
                transcription_data['speakers_text'] = format_diarization_for_display(diarization_segments)

                # Tentar combinar transcrição com diarização
                if 'segments' in result:
                    combined_text = combine_transcription_with_diarization(
                        result['segments'],
                        diarization_segments
                    )
                    transcription_data['combined_text'] = combined_text

        return transcription_data, None

    except Exception as e:
        error_msg = f"Erro durante a transcrição: {e}"
        logger.error(error_msg)
        return None, error_msg

def format_transcription_with_timestamps(segments):
    """
    Formata a transcrição com timestamps.

    Args:
        segments (list): Segmentos do Whisper com timestamps

    Returns:
        str: Texto formatado com timestamps
    """
    formatted_text = ""

    for segment in segments:
        start_time = format_time(segment['start'])
        end_time = format_time(segment['end'])
        text = segment['text'].strip()
        formatted_text += f"[{start_time} - {end_time}] {text}\n"

    return formatted_text

def format_time(seconds):
    """
    Converte segundos para formato MM:SS ou HH:MM:SS.

    Args:
        seconds (float): Tempo em segundos

    Returns:
        str: Tempo formatado
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def combine_transcription_with_diarization(transcription_segments, diarization_segments):
    """
    Combina transcrição do Whisper com diarização de locutores.

    Args:
        transcription_segments (list): Segmentos do Whisper
        diarization_segments (list): Segmentos de diarização

    Returns:
        str: Texto combinado com identificação de locutores
    """
    combined_text = ""

    for t_segment in transcription_segments:
        start_time = t_segment['start']
        end_time = t_segment['end']
        text = t_segment['text'].strip()

        # Encontrar locutor correspondente
        speaker = find_speaker_for_time(start_time, end_time, diarization_segments)

        time_formatted = f"[{format_time(start_time)} - {format_time(end_time)}]"
        combined_text += f"{time_formatted} {speaker}: {text}\n"

    return combined_text

def find_speaker_for_time(start_time, end_time, diarization_segments):
    """
    Encontra o locutor para um determinado período de tempo.

    Args:
        start_time (float): Tempo de início
        end_time (float): Tempo de fim
        diarization_segments (list): Segmentos de diarização

    Returns:
        str: Identificação do locutor
    """
    # Calcular o ponto médio do segmento
    mid_time = (start_time + end_time) / 2

    # Encontrar o segmento de diarização que contém este tempo
    for d_segment in diarization_segments:
        if d_segment['start'] <= mid_time <= d_segment['end']:
            return d_segment['speaker']

    # Se não encontrar, procurar o mais próximo
    best_overlap = 0
    best_speaker = "SPEAKER_UNKNOWN"

    for d_segment in diarization_segments:
        # Calcular sobreposição
        overlap_start = max(start_time, d_segment['start'])
        overlap_end = min(end_time, d_segment['end'])
        overlap = max(0, overlap_end - overlap_start)

        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = d_segment['speaker']

    return best_speaker

def transcribe_audio_simple(file_path):
    """
    Função simples de transcrição para compatibilidade.
    """
    result, error = transcribe_audio(file_path, include_timestamps=False, include_diarization=False)
    if error:
        return None, error
    return result['text'], None

def is_model_loaded():
    """
    Verifica se o modelo Whisper está carregado.

    Returns:
        bool: True se o modelo está carregado, False caso contrário
    """
    global loaded_model
    return loaded_model is not None
