#!/usr/bin/env python3
"""
Script para testar a visualização do diálogo com dados sintéticos de diarização.
"""

import requests
import json
import time

def create_synthetic_diarization_data():
    """Cria dados sintéticos de diarização para teste."""
    return {
        'text': 'Olá, como você está? Estou bem, obrigado. E você? Também estou bem. Que bom!',
        'speakers_text': 'SPEAKER_00: Olá, como você está?\nSPEAKER_01: Estou bem, obrigado. E você?\nSPEAKER_00: Também estou bem.\nSPEAKER_01: Que bom!',
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
        }
    }

def test_dialogue_visualization():
    """Testa a visualização do diálogo usando dados sintéticos."""

    print("🧪 TESTE: Visualização do Diálogo com Dados Sintéticos")
    print("=" * 60)

    # Criar dados sintéticos
    synthetic_data = create_synthetic_diarization_data()

    print("📝 Dados sintéticos criados:")
    print(f"   - Locutores: {synthetic_data['speakers_summary']['total_speakers']}")
    print(f"   - Segmentos: {synthetic_data['speakers_summary']['total_segments']}")
    print(f"   - Duração total: {synthetic_data['speakers_summary']['total_duration']}s")

    print("\n💬 Texto com locutores:")
    print(synthetic_data['speakers_text'])

    print("\n📊 Segmentos detalhados:")
    for i, segment in enumerate(synthetic_data['transcription_data']['segments'], 1):
        print(f"   {i}. {segment['speaker']}: \"{segment['text']}\" ({segment['start']:.1f}s - {segment['end']:.1f}s)")

    print("\n✅ Dados prontos para teste na interface web!")
    print("🌐 Acesse: http://localhost:5001")
    print("📋 Use estes dados para testar a funcionalidade de diálogo manualmente na interface.")

    # Salvar dados para uso posterior se necessário
    with open('/tmp/synthetic_diarization_data.json', 'w', encoding='utf-8') as f:
        json.dump(synthetic_data, f, indent=2, ensure_ascii=False)

    print("💾 Dados salvos em: /tmp/synthetic_diarization_data.json")

if __name__ == "__main__":
    test_dialogue_visualization()
