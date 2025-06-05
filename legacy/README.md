# 📁 Legacy Files

Esta pasta contém arquivos antigos que não são mais utilizados na versão atual do Whisper-Insights, mas são mantidos para referência histórica.

## Arquivos

### `transcritor_audio.py`
- **Descrição**: Versão original do transcritor com interface desktop (Tkinter)
- **Status**: Descontinuado na versão 2.0.0
- **Substituto**: Interface web atual (`app.py` + `templates/index.html`)
- **Última atualização**: Janeiro 2024

## Migração

Se você estava usando a versão desktop (1.x), migre para a versão web atual:

1. **Configure o ambiente**: Siga o [📦 Guia de Instalação](../docs/INSTALLATION.md)
2. **Configure o .env**: Copie `.env.example` para `.env`
3. **Execute a aplicação**: `python app.py`
4. **Acesse**: http://localhost:5001

## Diferenças Principais

| Versão Desktop (Legacy) | Versão Web (Atual) |
|--------------------------|---------------------|
| Interface Tkinter | Interface Web Moderna |
| Processamento síncrono | Processamento assíncrono |
| Apenas transcrição básica | Diarização + Insights IA |
| Sem testes automatizados | Suíte completa de testes |
| Configuração manual | Configuração via .env |

---

**⚠️ Nota**: Os arquivos nesta pasta são mantidos apenas para referência e não recebem atualizações ou suporte.
