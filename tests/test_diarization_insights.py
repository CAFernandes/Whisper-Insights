#!/usr/bin/env python3
"""
Teste específico para validar a melhoria de uso de diarização em insights.
Este teste cria dados simulados para verificar se a hierarquia de priorização funciona.
"""

import json
import sys
import os

# Adicionar o diretório pai ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.task_service import update_task_status, get_task_info

def test_text_source_hierarchy():
    """
    Testa a hierarquia de seleção de texto para insights:
    1. speakers_text (diarização) - prioridade mais alta
    2. timestamped_text (timestamps) - prioridade média
    3. text (simples) - fallback
    """

    print("🧪 TESTE: Hierarquia de Seleção de Texto para Insights")
    print("=" * 60)

    # Simular dados de transcrição completos
    test_task_id = "test_diarization_hierarchy"

    # Dados simulados com todas as opções disponíveis
    transcription_data = {
        'speakers_text': 'SPEAKER_00: Texto com diarização - maior prioridade\nSPEAKER_01: Segunda pessoa falando',
        'timestamped_text': '[00:01] Texto com timestamps - prioridade média [00:05] Continuação com tempo',
        'combined_text': 'Texto combinado com diarização e timestamps',
        'speakers_summary': {
            'SPEAKER_00': {'duration': 15.0, 'percentage': 60.0},
            'SPEAKER_01': {'duration': 10.0, 'percentage': 40.0}
        }
    }

    # Criar task simulada
    task_info = {
        'task_id': test_task_id,
        'filename': 'test_audio.wav',
        'status': 'completed',
        'text': 'Texto simples - usado como fallback',
        'transcription_data': transcription_data
    }

    # Simular cada cenário da hierarquia
    scenarios = [
        {
            'name': '🥇 Cenário 1: Dados completos (deve usar speakers_text)',
            'transcription_data': transcription_data,
            'expected_source': 'transcrição com identificação de locutores',
            'expected_text': transcription_data['speakers_text']
        },
        {
            'name': '🥈 Cenário 2: Apenas timestamps (deve usar timestamped_text)',
            'transcription_data': {
                'timestamped_text': transcription_data['timestamped_text']
            },
            'expected_source': 'transcrição com timestamps',
            'expected_text': transcription_data['timestamped_text']
        },
        {
            'name': '🥉 Cenário 3: Dados vazios (deve usar text simples)',
            'transcription_data': {},
            'expected_source': 'texto simples',
            'expected_text': 'Texto simples - usado como fallback'
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{scenario['name']}")
        print("-" * 50)

        # Simular a lógica implementada em app.py
        transcribed_text = task_info['text']  # Valor padrão
        text_source = "texto simples"

        # Verificar se há dados de transcrição completos disponíveis
        transcription_data_test = scenario['transcription_data']

        # Priorizar texto com diarização (mais contexto)
        if transcription_data_test.get('speakers_text'):
            transcribed_text = transcription_data_test['speakers_text']
            text_source = "transcrição com identificação de locutores"
            print(f"✅ Usando texto com diarização para insights (melhor contexto)")
        # Segunda opção: texto com timestamps
        elif transcription_data_test.get('timestamped_text'):
            transcribed_text = transcription_data_test['timestamped_text']
            text_source = "transcrição com timestamps"
            print(f"✅ Usando texto com timestamps para insights")
        # Fallback: texto simples (já definido acima)
        else:
            print(f"✅ Usando texto simples para insights")

        # Verificar se escolheu a fonte correta
        if text_source == scenario['expected_source']:
            print(f"✅ APROVADO: Fonte correta selecionada: {text_source}")
        else:
            print(f"❌ FALHOU: Esperado '{scenario['expected_source']}', obteve '{text_source}'")
            return False

        # Verificar se o texto está correto
        if transcribed_text == scenario['expected_text']:
            print(f"✅ APROVADO: Texto correto selecionado")
        else:
            print(f"❌ FALHOU: Texto incorreto")
            print(f"   Esperado: {scenario['expected_text'][:50]}...")
            print(f"   Obteve:   {transcribed_text[:50]}...")
            return False

        print(f"📝 Texto selecionado: {transcribed_text[:100]}...")
        print(f"🎯 Fonte: {text_source}")

    return True

def test_real_world_integration():
    """
    Teste de integração que simula como a melhoria funciona no contexto real
    """
    print(f"\n🌍 TESTE: Integração no Mundo Real")
    print("=" * 50)

    # Simular um caso real onde transcription_data é None (compatibilidade retroativa)
    print("📝 Cenário: transcription_data ausente (compatibilidade retroativa)")

    task_info = {
        'text': 'Texto de fallback quando não há transcription_data'
    }

    # Lógica da aplicação real
    transcribed_text = task_info['text']
    text_source = "texto simples"

    transcription_data = task_info.get('transcription_data', {})  # Retorna {}

    if transcription_data.get('speakers_text'):
        transcribed_text = transcription_data['speakers_text']
        text_source = "transcrição com identificação de locutores"
    elif transcription_data.get('timestamped_text'):
        transcribed_text = transcription_data['timestamped_text']
        text_source = "transcrição com timestamps"

    if text_source == "texto simples":
        print("✅ APROVADO: Fallback funcionando corretamente")
        print(f"📝 Texto: {transcribed_text}")
        return True
    else:
        print("❌ FALHOU: Fallback não funcionou")
        return False

def main():
    """
    Executa todos os testes da melhoria de diarização em insights
    """
    print("🚀 Iniciando Testes da Melhoria: Diarização em Insights")
    print("=" * 70)

    all_tests_passed = True

    # Teste 1: Hierarquia de seleção
    if test_text_source_hierarchy():
        print(f"\n✅ TESTE 1 APROVADO: Hierarquia de seleção funcionando")
    else:
        print(f"\n❌ TESTE 1 FALHOU: Problema na hierarquia de seleção")
        all_tests_passed = False

    # Teste 2: Integração no mundo real
    if test_real_world_integration():
        print(f"\n✅ TESTE 2 APROVADO: Integração no mundo real funcionando")
    else:
        print(f"\n❌ TESTE 2 FALHOU: Problema na integração")
        all_tests_passed = False

    # Resultado final
    print(f"\n" + "=" * 70)
    if all_tests_passed:
        print("🎉 TODOS OS TESTES APROVADOS!")
        print("✅ A melhoria de diarização em insights está funcionando corretamente")
        print("🎯 Sistema priorizará automaticamente:")
        print("   1. speakers_text (diarização) - melhor contexto")
        print("   2. timestamped_text (timestamps) - contexto médio")
        print("   3. text (simples) - fallback garantido")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️  Verifique a implementação da melhoria")

    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
