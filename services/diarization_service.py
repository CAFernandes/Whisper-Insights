# Serviço para diarização de locutores usando pyannote.audio
import torch
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment
import tempfile
import os
import logging
import warnings
from config import HUGGINGFACE_TOKEN

# Suprimir warning específico do SpeechBrain
warnings.filterwarnings("ignore", message="Module 'speechbrain.pretrained' was deprecated")

logger = logging.getLogger(__name__)

# Modelo de diarização global
diarization_pipeline = None

def load_diarization_model():
    """
    Carrega o modelo de diarização de locutores.
    Usa o modelo pré-treinado da pyannote.audio do Hugging Face.
    """
    global diarization_pipeline
    if diarization_pipeline is None:
        try:
            # Verificar se temos o token do Hugging Face
            hf_token = HUGGINGFACE_TOKEN

            # Modelo de diarização speaker diarization
            # Nota: Este modelo requer aceitar os termos de uso no Hugging Face
            # Para usar, você precisa:
            # 1. Aceitar os termos em: https://huggingface.co/pyannote/speaker-diarization-3.1
            # 2. Ter um token do Hugging Face configurado

            if hf_token:
                logger.info("Token do Hugging Face encontrado, tentando carregar modelo com autenticação...")
                diarization_pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=hf_token
                )
            else:
                logger.warning("Token do Hugging Face não encontrado, tentando sem autenticação...")
                diarization_pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=False
                )

            # Se tiver GPU disponível, usar
            if torch.cuda.is_available():
                diarization_pipeline = diarization_pipeline.to(torch.device("cuda"))
                logger.info("Modelo de diarização carregado na GPU")
            else:
                logger.info("Modelo de diarização carregado na CPU")

            return True, "Modelo de diarização carregado com sucesso."

        except Exception as e:
            logger.error(f"Erro ao carregar modelo de diarização: {e}")

            # Tentar modelo alternativo menor
            try:
                # Modelo mais simples que pode não precisar de token
                from pyannote.audio.pipelines import SpeakerDiarization
                diarization_pipeline = SpeakerDiarization()
                logger.info("Modelo de diarização alternativo carregado")
                return True, "Modelo de diarização alternativo carregado."
            except Exception as e2:
                logger.error(f"Erro ao carregar modelo alternativo: {e2}")
                return False, f"Erro ao carregar modelos de diarização: {e}, {e2}"

    return True, "Modelo de diarização já carregado."

def perform_diarization(audio_file_path, num_speakers=None, min_speakers=1, max_speakers=10):
    """
    Realiza a diarização de locutores em um arquivo de áudio.

    Args:
        audio_file_path (str): Caminho para o arquivo de áudio
        num_speakers (int, optional): Número específico de locutores (se conhecido)
        min_speakers (int): Número mínimo de locutores (padrão: 1)
        max_speakers (int): Número máximo de locutores (padrão: 10)

    Returns:
        tuple: (annotation_segments, error_message)
        annotation_segments: Lista de dicionários com informações dos segmentos
        error_message: Mensagem de erro se houver
    """
    global diarization_pipeline

    if diarization_pipeline is None:
        success, message = load_diarization_model()
        if not success:
            return None, message

    try:
        if not os.path.exists(audio_file_path):
            return None, f"Arquivo de áudio não encontrado: {audio_file_path}"

        logger.info(f"Iniciando diarização de: {audio_file_path}")

        # Configurar parâmetros da diarização
        if hasattr(diarization_pipeline, 'instantiate'):
            # Configurar número de locutores se especificado
            params = {}
            if num_speakers:
                params['num_speakers'] = num_speakers
            else:
                params['min_speakers'] = min_speakers
                params['max_speakers'] = max_speakers

            # Aplicar diarização
            diarization = diarization_pipeline(audio_file_path, **params)
        else:
            # Para modelos mais simples
            diarization = diarization_pipeline(audio_file_path)

        # Converter resultado para formato útil
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segment_info = {
                'start': round(turn.start, 2),
                'end': round(turn.end, 2),
                'duration': round(turn.duration, 2),
                'speaker': speaker
            }
            segments.append(segment_info)

        logger.info(f"Diarização concluída. {len(segments)} segmentos identificados.")

        # Ordenar segmentos por tempo de início
        segments.sort(key=lambda x: x['start'])

        return segments, None

    except Exception as e:
        error_msg = f"Erro durante a diarização: {e}"
        logger.error(error_msg)
        return None, error_msg

def get_speakers_summary(segments):
    """
    Gera um resumo dos locutores identificados.

    Args:
        segments (list): Lista de segmentos da diarização

    Returns:
        dict: Resumo com informações dos locutores
    """
    if not segments:
        return {}

    speakers = {}
    total_duration = 0

    for segment in segments:
        speaker = segment['speaker']
        duration = segment['duration']

        if speaker not in speakers:
            speakers[speaker] = {
                'total_duration': 0,
                'segments_count': 0,
                'percentage': 0
            }

        speakers[speaker]['total_duration'] += duration
        speakers[speaker]['segments_count'] += 1
        total_duration += duration

    # Calcular percentuais
    for speaker in speakers:
        if total_duration > 0:
            speakers[speaker]['percentage'] = round(
                (speakers[speaker]['total_duration'] / total_duration) * 100, 1
            )
        speakers[speaker]['total_duration'] = round(speakers[speaker]['total_duration'], 2)

    # Adicionar informações gerais
    summary = {
        'speakers': speakers,
        'total_speakers': len(speakers),
        'total_duration': round(total_duration, 2),
        'total_segments': len(segments)
    }

    return summary

def format_diarization_for_display(segments):
    """
    Formata os segmentos de diarização para exibição.

    Args:
        segments (list): Lista de segmentos da diarização

    Returns:
        str: Texto formatado para exibição
    """
    if not segments:
        return "Nenhum segmento de locutor identificado."

    formatted_text = "=== IDENTIFICAÇÃO DE LOCUTORES ===\n\n"

    for segment in segments:
        start_time = format_time(segment['start'])
        end_time = format_time(segment['end'])
        speaker = segment['speaker']
        duration = segment['duration']

        formatted_text += f"[{start_time} - {end_time}] {speaker} ({duration}s)\n"

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

def is_diarization_available():
    """
    Verifica se o serviço de diarização está disponível.

    Returns:
        bool: True se disponível, False caso contrário
    """
    try:
        success, _ = load_diarization_model()
        return success
    except Exception:
        return False
