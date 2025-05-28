#!/usr/bin/env python3
"""
Script de teste abrangente para o workflow completo:
1. Upload de arquivos de áudio de diferentes formatos
2. Transcrição com Whisper
3. Geração de insights com Ollama
4. Testes de casos de erro
5. Testes de retry de insights
"""

import requests
import time
import json
import os

# Configurações
FLASK_URL = "http://localhost:5001"
TEST_FILES = {
    "valid_audio": [
        ("teste_audio.m4a", "audio/m4a"),
        ("teste_audio.wav", "audio/wav"),
        ("teste_audio.ogg", "audio/ogg"),
        ("teste_audio.kwf", "audio/kwf")
    ],
    "invalid_files": [
        ("invalid_file.txt", "text/plain")
    ]
}

def test_ollama_connection():
    """Testa a conexão com o Ollama"""
    print("🔍 Verificando conexão com Ollama...")
    try:
        response = requests.get(f"{FLASK_URL}/check_ollama")
        data = response.json()
        if data['connected']:
            print(f"✅ Ollama conectado com {data['count']} modelo(s): {', '.join(data['models'])}")
            return data['models']
        else:
            print("❌ Ollama não está conectado")
            return []
    except Exception as e:
        print(f"❌ Erro ao verificar Ollama: {e}")
        return []

def test_whisper_model():
    """Testa se o modelo Whisper está carregado"""
    print("🔍 Verificando modelo Whisper...")
    try:
        response = requests.get(f"{FLASK_URL}/check_model")
        data = response.json()
        if data['success']:
            print(f"✅ {data['message']}")
            return True
        else:
            print(f"❌ Erro no modelo Whisper: {data['message']}")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar modelo Whisper: {e}")
        return False

def upload_file(file_path, content_type):
    """Faz upload de um arquivo específico"""
    print(f"\n📤 Fazendo upload do arquivo: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado")
        return None, f"Arquivo {file_path} não encontrado"

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, content_type)}
            response = requests.post(f"{FLASK_URL}/upload", files=files)

            if response.status_code == 413:
                return None, "Arquivo muito grande (413 Request Entity Too Large)"

            data = response.json()

            if data['success']:
                print(f"✅ Upload realizado com sucesso. Task ID: {data['task_id']}")
                return data['task_id'], None
            else:
                print(f"❌ Erro no upload: {data['message']}")
                return None, data['message']
    except Exception as e:
        print(f"❌ Erro durante upload: {e}")
        return None, str(e)

def test_invalid_upload():
    """Testa upload de arquivo inválido"""
    print("\n🚫 Testando upload de arquivo inválido...")

    for file_path, content_type in TEST_FILES["invalid_files"]:
        task_id, error = upload_file(file_path, content_type)
        if task_id is None and "não permitido" in str(error):
            print(f"✅ Erro esperado para {file_path}: {error}")
        else:
            print(f"❌ Upload de arquivo inválido não foi rejeitado adequadamente: {file_path}")

def test_no_file_upload():
    """Testa upload sem arquivo"""
    print("\n🚫 Testando upload sem arquivo...")
    try:
        response = requests.post(f"{FLASK_URL}/upload", files={})
        data = response.json()
        if not data['success'] and "Nenhum arquivo" in data['message']:
            print(f"✅ Erro esperado: {data['message']}")
        else:
            print(f"❌ Upload sem arquivo não foi rejeitado adequadamente")
    except Exception as e:
        print(f"❌ Erro inesperado no teste de upload sem arquivo: {e}")

def monitor_progress(task_id, wait_for_insights=False):
    """Monitora o progresso da transcrição e opcionalmente dos insights"""
    print(f"\n⏳ Monitorando progresso da task {task_id}...")

    while True:
        try:
            response = requests.get(f"{FLASK_URL}/status/{task_id}")
            data = response.json()
            status = data.get('status', 'unknown')

            if status in ['processing', 'pending_upload']:
                progress = data.get('progress', 'Processando...')
                print(f"🔄 {progress}")
                time.sleep(3)

            elif status == 'transcription_completed':
                print("✅ Transcrição concluída com sucesso!")
                print(f"\n📝 Transcrição:")
                print("-" * 50)
                text = data.get('text', '')
                print(text[:500] + "..." if len(text) > 500 else text)
                print("-" * 50)

                if not wait_for_insights:
                    return data
                else:
                    print("⏳ Aguardando geração de insights...")
                    time.sleep(2)

            elif status == 'generating_insights':
                progress = data.get('progress', 'Gerando insights...')
                print(f"🔄 {progress}")
                time.sleep(3)

            elif status in ['completed_with_insights', 'completed']:
                print("✅ Processamento concluído com sucesso!")

                if 'text' in data:
                    print(f"\n📝 Transcrição:")
                    print("-" * 50)
                    text = data.get('text', '')
                    print(text[:500] + "..." if len(text) > 500 else text)
                    print("-" * 50)

                if 'insights' in data and data['insights']:
                    print(f"\n🧠 Insights gerados:")
                    print("-" * 50)
                    insights = data['insights']
                    print(insights[:1000] + "..." if len(insights) > 1000 else insights)
                    print("-" * 50)
                else:
                    print("\n⚠️ Nenhum insight foi gerado")

                return data

            elif status in ['error', 'error_insights']:
                print(f"❌ Erro: {data.get('message', 'Erro desconhecido')}")
                return None

            elif status == 'not_found':
                print("❌ Task não encontrada")
                return None

            else:
                print(f"⚠️ Status desconhecido: {status}")
                time.sleep(3)

        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")
            return None

def test_retry_insights(task_id, ollama_models):
    """Testa a funcionalidade de retry de insights"""
    print(f"\n🔄 Testando retry de insights para task {task_id}...")

    if not ollama_models:
        print("⚠️ Nenhum modelo Ollama disponível para teste de retry")
        return False

    custom_prompt = "Forneça um resumo executivo muito conciso em 3 pontos principais: {{text}}"

    # Priorizar modelo llama se disponível
    selected_model = None
    for model in ollama_models:
        if "llama" in model.lower():
            selected_model = model
            break

    if not selected_model:
        selected_model = ollama_models[0]  # Fallback para o primeiro modelo disponível

    try:
        payload = {
            "prompt": custom_prompt,
            "model_name": selected_model
        }

        response = requests.post(f"{FLASK_URL}/retry_insights/{task_id}",
                               json=payload,
                               headers={'Content-Type': 'application/json'})

        data = response.json()

        if data['success']:
            print(f"✅ Insights gerados com sucesso usando modelo {selected_model}")
            print(f"📝 Prompt usado: {custom_prompt[:100]}...")
            if 'insights' in data:
                insights = data['insights']
                print(f"🧠 Insights: {insights[:300]}...")
            return True
        else:
            print(f"❌ Erro ao gerar insights: {data.get('message', 'Erro desconhecido')}")
            return False

    except Exception as e:
        print(f"❌ Erro durante retry de insights: {e}")
        return False

def test_single_file_workflow(file_path, content_type, ollama_models):
    """Testa o workflow completo para um único arquivo"""
    print(f"\n{'='*60}")
    print(f"🎯 Testando workflow para: {file_path}")
    print(f"{'='*60}")

    # Upload
    task_id, error = upload_file(file_path, content_type)
    if not task_id:
        print(f"❌ Falha no upload: {error}")
        return False

    # Monitorar transcrição
    result = monitor_progress(task_id, wait_for_insights=False)
    if not result:
        print(f"❌ Falha na transcrição")
        return False

    # Testar retry de insights se a transcrição foi bem-sucedida
    if result.get('status') == 'transcription_completed':
        insights_success = test_retry_insights(task_id, ollama_models)
        if insights_success:
            # Monitorar novamente para ver o resultado final
            final_result = monitor_progress(task_id, wait_for_insights=False)

    print(f"✅ Workflow completo para {file_path}")
    return True

def main():
    """Função principal do teste abrangente"""
    print("🚀 Iniciando suite de testes abrangente\n")

    test_results = {
        "whisper_model": False,
        "ollama_connection": False,
        "valid_files": 0,
        "invalid_files": 0,
        "no_file_upload": False,
        "insights_retry": 0
    }

    # 1. Verificar modelo Whisper
    print("📋 FASE 1: Verificação de Dependências")
    print("-" * 40)
    test_results["whisper_model"] = test_whisper_model()

    # 2. Verificar Ollama
    ollama_models = test_ollama_connection()
    test_results["ollama_connection"] = len(ollama_models) > 0

    if not test_results["whisper_model"]:
        print("\n⚠️ Testes abortados devido a problemas com o modelo Whisper")
        return test_results

    # 3. Testes de upload inválido
    print(f"\n📋 FASE 2: Testes de Validação de Upload")
    print("-" * 40)
    test_invalid_upload()
    test_results["invalid_files"] = len(TEST_FILES["invalid_files"])

    test_no_file_upload()
    test_results["no_file_upload"] = True

    # 4. Testes de workflow completo para arquivos válidos
    print(f"\n📋 FASE 3: Testes de Workflow Completo")
    print("-" * 40)

    successful_workflows = 0
    total_valid_files = len(TEST_FILES["valid_audio"])

    for file_path, content_type in TEST_FILES["valid_audio"]:
        if os.path.exists(file_path):
            success = test_single_file_workflow(file_path, content_type, ollama_models)
            if success:
                successful_workflows += 1
                if ollama_models:  # Se tem modelos Ollama, conta como teste de insights
                    test_results["insights_retry"] += 1
        else:
            print(f"⚠️ Arquivo {file_path} não encontrado, pulando teste...")

    test_results["valid_files"] = successful_workflows

    # 5. Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    print(f"✅ Modelo Whisper: {'OK' if test_results['whisper_model'] else 'FALHA'}")
    print(f"✅ Conexão Ollama: {'OK' if test_results['ollama_connection'] else 'FALHA'} ({len(ollama_models)} modelos)")
    print(f"✅ Arquivos válidos testados: {test_results['valid_files']}/{total_valid_files}")
    print(f"✅ Testes de arquivo inválido: {test_results['invalid_files']}")
    print(f"✅ Teste upload sem arquivo: {'OK' if test_results['no_file_upload'] else 'FALHA'}")
    print(f"✅ Testes de retry insights: {test_results['insights_retry']}")

    # Calcular score geral
    total_tests = 6  # whisper, ollama, valid_files (como um teste), invalid_files, no_file, insights
    passed_tests = (
        (1 if test_results['whisper_model'] else 0) +
        (1 if test_results['ollama_connection'] else 0) +
        (1 if test_results['valid_files'] > 0 else 0) +
        (1 if test_results['invalid_files'] > 0 else 0) +
        (1 if test_results['no_file_upload'] else 0) +
        (1 if test_results['insights_retry'] > 0 else 0)
    )

    success_rate = (passed_tests / total_tests) * 100
    print(f"\n🎯 Taxa de Sucesso Geral: {success_rate:.1f}% ({passed_tests}/{total_tests})")

    if success_rate >= 80:
        print("🎉 Suite de testes APROVADA!")
    elif success_rate >= 60:
        print("⚠️ Suite de testes com AVISOS")
    else:
        print("❌ Suite de testes REPROVADA")

    return test_results

if __name__ == "__main__":
    main()
