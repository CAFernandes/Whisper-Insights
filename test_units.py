#!/usr/bin/env python3
"""
Testes unitários para os módulos de serviço da aplicação.
Execute com: python -m pytest test_units.py -v
"""

import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Importar os módulos a serem testados
from helpers.file_utils import allowed_file, cleanup_old_files
from services import task_service, whisper_service, ollama_service
from config import ALLOWED_EXTENSIONS


class TestFileUtils:
    """Testes para helpers/file_utils.py"""

    def test_allowed_file_valid_extensions(self):
        """Testa se arquivos com extensões válidas são aceitos"""
        valid_files = [
            "audio.mp3",
            "recording.wav",
            "video.m4a",
            "sound.ogg",
            "music.flac",
            "clip.mp4",
            "movie.avi",
            "test.kwf"
        ]

        for filename in valid_files:
            assert allowed_file(filename), f"Arquivo {filename} deveria ser aceito"

    def test_allowed_file_invalid_extensions(self):
        """Testa se arquivos com extensões inválidas são rejeitados"""
        invalid_files = [
            "document.txt",
            "image.jpg",
            "data.json",
            "script.py",
            "readme.md",
            "file.exe",
            "archive.zip"
        ]

        for filename in invalid_files:
            assert not allowed_file(filename), f"Arquivo {filename} deveria ser rejeitado"

    def test_allowed_file_no_extension(self):
        """Testa se arquivos sem extensão são rejeitados"""
        assert not allowed_file("arquivo_sem_extensao")
        assert not allowed_file(".")
        assert not allowed_file("")

    def test_allowed_file_case_insensitive(self):
        """Testa se a verificação de extensão é case-insensitive"""
        assert allowed_file("AUDIO.MP3")
        assert allowed_file("Recording.WAV")
        assert allowed_file("Video.M4A")

    @patch('helpers.file_utils.logger')
    def test_cleanup_old_files_no_directory(self, mock_logger):
        """Testa cleanup quando o diretório não existe"""
        with patch('os.path.isdir', return_value=False):
            cleanup_old_files()
            mock_logger.warning.assert_called()


class TestTaskService:
    """Testes para services/task_service.py"""

    def test_create_task(self):
        """Testa criação de nova task"""
        task_id = task_service.create_task()
        assert task_id is not None
        assert len(task_id) > 0
        assert isinstance(task_id, str)

    def test_update_and_get_task_status(self):
        """Testa atualização e recuperação do status da task"""
        task_id = task_service.create_task()

        # Testar atualização de status
        task_service.update_task_status(
            task_id,
            status="processing",
            progress="Iniciando...",
            message="Teste"
        )

        # Recuperar status
        status = task_service.get_task_status(task_id)
        assert status is not None
        assert status['status'] == "processing"
        assert status['progress'] == "Iniciando..."
        assert status['message'] == "Teste"

    def test_get_nonexistent_task(self):
        """Testa recuperação de task inexistente"""
        status = task_service.get_task_status("task_inexistente")
        assert status is None

    def test_update_task_with_text_and_insights(self):
        """Testa atualização com texto transcrito e insights"""
        task_id = task_service.create_task()

        task_service.update_task_status(
            task_id,
            status="completed_with_insights",
            text="Texto transcrito de teste",
            insights="Insights gerados de teste",
            current_prompt="Prompt de teste"
        )

        status = task_service.get_task_status(task_id)
        assert status['text'] == "Texto transcrito de teste"
        assert status['insights'] == "Insights gerados de teste"
        assert status['current_prompt'] == "Prompt de teste"


class TestWhisperService:
    """Testes para services/whisper_service.py"""

    @patch('services.whisper_service.whisper')
    def test_load_whisper_model_success(self, mock_whisper):
        """Testa carregamento bem-sucedido do modelo Whisper"""
        mock_model = Mock()
        mock_whisper.load_model.return_value = mock_model

        success, message = whisper_service.load_whisper_model()

        assert success is True
        assert "carregado" in message.lower()
        mock_whisper.load_model.assert_called_once()

    @patch('services.whisper_service.whisper')
    def test_load_whisper_model_failure(self, mock_whisper):
        """Testa falha no carregamento do modelo Whisper"""
        mock_whisper.load_model.side_effect = Exception("Erro de teste")

        success, message = whisper_service.load_whisper_model()

        assert success is False
        assert "erro" in message.lower()

    def test_transcribe_audio_no_file(self):
        """Testa transcrição com arquivo inexistente"""
        result_text, error = whisper_service.transcribe_audio("arquivo_inexistente.mp3")

        assert result_text is None
        assert error is not None
        assert "não encontrado" in error.lower()


class TestOllamaService:
    """Testes para services/ollama_service.py"""

    @patch('services.ollama_service.requests.get')
    def test_get_available_ollama_models_success(self, mock_get):
        """Testa recuperação bem-sucedida de modelos Ollama"""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "model1:latest"},
                {"name": "model2:latest"}
            ]
        }
        mock_get.return_value = mock_response

        models, connected, count = ollama_service.get_available_ollama_models()

        assert connected is True
        assert count == 2
        assert "model1:latest" in models
        assert "model2:latest" in models

    @patch('services.ollama_service.requests.get')
    def test_get_available_ollama_models_connection_error(self, mock_get):
        """Testa erro de conexão com Ollama"""
        mock_get.side_effect = Exception("Connection refused")

        models, connected, count = ollama_service.get_available_ollama_models()

        assert connected is False
        assert count == 0
        assert models == []

    @patch('services.ollama_service.requests.post')
    def test_generate_ollama_insights_success(self, mock_post):
        """Testa geração bem-sucedida de insights"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "Insights gerados com sucesso"
        }
        mock_post.return_value = mock_response

        insights, error = ollama_service.generate_ollama_insights(
            "Texto de teste",
            "Prompt de teste: {{text}}",
            "model1:latest"
        )

        assert insights == "Insights gerados com sucesso"
        assert error is None

    @patch('services.ollama_service.requests.post')
    def test_generate_ollama_insights_error(self, mock_post):
        """Testa erro na geração de insights"""
        mock_post.side_effect = Exception("Server error")

        insights, error = ollama_service.generate_ollama_insights(
            "Texto de teste",
            "Prompt de teste: {{text}}",
            "model1:latest"
        )

        assert insights is None
        assert error is not None
        assert "erro" in error.lower()


class TestConfigValidation:
    """Testes para validação de configurações"""

    def test_allowed_extensions_format(self):
        """Testa se ALLOWED_EXTENSIONS está no formato correto"""
        assert isinstance(ALLOWED_EXTENSIONS, set)
        assert len(ALLOWED_EXTENSIONS) > 0

        # Verificar se todas as extensões são strings válidas
        for ext in ALLOWED_EXTENSIONS:
            assert isinstance(ext, str)
            assert len(ext) > 0
            assert '.' not in ext  # Extensões não devem conter ponto


def test_file_utils_allowed_file():
    """Testa a função allowed_file"""
    from helpers.file_utils import allowed_file

    # Testes de arquivos válidos
    assert allowed_file("audio.mp3") == True
    assert allowed_file("recording.wav") == True
    assert allowed_file("test.kwf") == True

    # Testes de arquivos inválidos
    assert allowed_file("document.txt") == False
    assert allowed_file("image.jpg") == False
    assert allowed_file("") == False


def test_task_service_basic():
    """Testa funcionalidades básicas do task service"""
    from services import task_service

    # Criar task
    task_id = task_service.create_task()
    assert task_id is not None
    assert len(task_id) > 0

    # Atualizar status
    task_service.update_task_status(task_id, status="processing", progress="Teste")

    # Recuperar status
    status = task_service.get_task_status(task_id)
    assert status is not None
    assert status['status'] == "processing"
    assert status['progress'] == "Teste"


def test_config_validation():
    """Testa se a configuração está válida"""
    from config import ALLOWED_EXTENSIONS

    assert isinstance(ALLOWED_EXTENSIONS, set)
    assert len(ALLOWED_EXTENSIONS) > 0

    # Verificar algumas extensões esperadas
    expected_extensions = {'mp3', 'wav', 'm4a', 'kwf'}
    for ext in expected_extensions:
        assert ext in ALLOWED_EXTENSIONS


def test_simple():
    """Um teste simples para verificar se o pytest funciona"""
    assert True


if __name__ == "__main__":
    # Executar os testes se o arquivo for chamado diretamente
    # Requer pytest: pip install pytest
    print("Para executar os testes, use: python -m pytest test_units.py -v")
    print("Ou para este arquivo: python -m pytest test_units.py::TestFileUtils -v")
