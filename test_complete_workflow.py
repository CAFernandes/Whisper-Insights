#!/usr/bin/env python3
"""
Script de teste para demonstrar o workflow completo:
1. Upload de arquivo de áudio
2. Transcrição com Whisper
3. Geração de insights com Ollama
"""

import requests
import time
import json
import os

# Configurações
FLASK_URL = "http://localhost:5000"
AUDIO_FILE = "Evoy Call 1.m4a"

def test_ollama_connection():
    """Testa a conexão com o Ollama"""
    print("🔍 Verificando conexão com Ollama...")
    try:
        response = requests.get(f"{FLASK_URL}/check_ollama")
        data = response.json()
        if data['connected']:
            print(f"✅ Ollama conectado com {data['count']} modelo(s): {', '.join(data['models'])}")
            return True
        else:
            print("❌ Ollama não está conectado")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar Ollama: {e}")
        return False

def upload_and_transcribe():
    """Faz upload e transcreve o arquivo de áudio"""
    print(f"\n📤 Fazendo upload do arquivo: {AUDIO_FILE}")

    if not os.path.exists(AUDIO_FILE):
        print(f"❌ Arquivo {AUDIO_FILE} não encontrado")
        return None

    try:
        with open(AUDIO_FILE, 'rb') as f:
            files = {'file': (AUDIO_FILE, f, 'audio/m4a')}
            response = requests.post(f"{FLASK_URL}/upload", files=files)
            data = response.json()

            if data['success']:
                print(f"✅ Upload realizado com sucesso. Task ID: {data['task_id']}")
                return data['task_id']
            else:
                print(f"❌ Erro no upload: {data['message']}")
                return None
    except Exception as e:
        print(f"❌ Erro durante upload: {e}")
        return None

def monitor_progress(task_id):
    """Monitora o progresso da transcrição"""
    print(f"\n⏳ Monitorando progresso da task {task_id}...")

    while True:
        try:
            response = requests.get(f"{FLASK_URL}/status/{task_id}")
            data = response.json()

            if data['status'] == 'processing':
                progress = data.get('progress', 'Processando...')
                print(f"🔄 {progress}")
                time.sleep(3)

            elif data['status'] == 'completed':
                print("✅ Transcrição concluída com sucesso!")
                print(f"\n📝 Transcrição:")
                print("-" * 50)
                print(data['text'][:500] + "..." if len(data['text']) > 500 else data['text'])
                print("-" * 50)

                if 'insights' in data and data['insights']:
                    print(f"\n🧠 Insights gerados:")
                    print("-" * 50)
                    print(data['insights'][:1000] + "..." if len(data['insights']) > 1000 else data['insights'])
                    print("-" * 50)
                else:
                    print("\n⚠️ Nenhum insight foi gerado")

                return data

            elif data['status'] == 'error':
                print(f"❌ Erro na transcrição: {data['message']}")
                return None

            elif data['status'] == 'not_found':
                print("❌ Task não encontrada")
                return None

        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")
            return None

def main():
    """Função principal do teste"""
    print("🚀 Iniciando teste do workflow completo\n")

    # 1. Verificar Ollama
    if not test_ollama_connection():
        print("\n⚠️ Teste abortado devido a problemas com Ollama")
        return

    # 2. Upload e transcrição
    task_id = upload_and_transcribe()
    if not task_id:
        print("\n⚠️ Teste abortado devido a problemas no upload")
        return

    # 3. Monitorar progresso
    result = monitor_progress(task_id)
    if result:
        print("\n🎉 Teste concluído com sucesso!")
        print("\n📊 Resumo:")
        print(f"- Arquivo processado: {AUDIO_FILE}")
        print(f"- Tamanho da transcrição: {len(result['text'])} caracteres")
        if 'insights' in result and result['insights']:
            print(f"- Tamanho dos insights: {len(result['insights'])} caracteres")
        print(f"- Task ID: {task_id}")
    else:
        print("\n💥 Teste falhou")

if __name__ == "__main__":
    main()
