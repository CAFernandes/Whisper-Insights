# 🎙️ Transcritor de Áudio Web

Uma aplicação web moderna para transcrição de áudio usando inteligência artificial Whisper da OpenAI.

## ✨ Características

- 🌐 **Interface Web moderna e responsiva**
- 🎯 **Drag & Drop** - Arraste arquivos diretamente para a interface
- 🔄 **Processamento assíncrono** - Upload e processamento em background
- 📱 **Design responsivo** - Funciona em desktop e mobile
- 🎨 **Interface intuitiva** - Design limpo e fácil de usar
- 📋 **Funcionalidades extras** - Copiar texto, baixar resultado
- ⚡ **Suporte a múltiplos formatos** - mp3, wav, m4a, ogg, flac, mp4, avi

## 🚀 Como usar

### Método 1: Script automático (Recomendado)
```bash
./start_web.sh
```

### Método 2: Manual
```bash
# 1. Ative o ambiente virtual
source transcribe/bin/activate

# 2. Instale dependências (se necessário)
pip install -r requirements-web.txt

# 3. Execute a aplicação
python app.py
```

### Método 3: Primeira execução
```bash
# Se é a primeira vez, configure o ambiente:
python3 -m venv transcribe
source transcribe/bin/activate
pip install -r requirements-web.txt
python app.py
```

## 🌐 Acesso

Após iniciar, acesse no seu navegador:
- **Local**: http://localhost:5000
- **Rede local**: http://seu-ip:5000

## 📁 Estrutura do projeto

```
transcribe_audio/
├── app.py                    # Aplicação Flask principal
├── start_web.sh             # Script de inicialização
├── requirements-web.txt     # Dependências Python
├── templates/
│   └── index.html          # Interface web
├── static/                 # Arquivos estáticos (CSS, JS)
├── uploads/                # Arquivos temporários (criado automaticamente)
├── transcribe/             # Ambiente virtual Python
└── transcritor_audio.py    # Versão desktop original
```

## 🔧 Dependências

- **Python 3.8+**
- **Flask** - Framework web
- **OpenAI Whisper** - Motor de transcrição
- **ffmpeg** (opcional) - Para suporte completo a formatos de áudio

### Instalar ffmpeg (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🎯 Como funciona

1. **Selecione ou arraste** um arquivo de áudio
2. **Clique em "Transcrever"** para iniciar o processamento
3. **Aguarde** - o modelo Whisper processará o áudio
4. **Receba o resultado** - texto transcrito aparecerá na tela
5. **Copie ou baixe** o resultado conforme necessário

## 🔒 Segurança

- Arquivos são automaticamente removidos após processamento
- Uploads limitados a 500MB
- Apenas formatos de áudio/vídeo permitidos
- Processamento local (nenhum dado é enviado para serviços externos)

## 🐛 Solução de problemas

### Erro de modelo não carregado
- Verifique sua conexão com internet (primeira execução)
- O modelo é baixado automaticamente na primeira vez

### Erro com formatos de áudio
- Instale ffmpeg: `sudo apt install ffmpeg`
- Use formatos mais comuns como mp3 ou wav

### Erro de permissão
- Verifique se o script tem permissão de execução: `chmod +x start_web.sh`

### Porta ocupada
- Mude a porta no arquivo `app.py` (linha final):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude 5000 para 5001
```

## 🆚 Comparação: Desktop vs Web

| Recurso | Desktop (tkinter) | Web (Flask) |
|---------|------------------|-------------|
| **Interface** | Aplicação nativa | Navegador |
| **Responsividade** | Fixa | Adaptável |
| **Acesso remoto** | ❌ Não | ✅ Sim |
| **Drag & Drop** | ✅ Sim | ✅ Sim |
| **Mobile** | ❌ Não | ✅ Sim |
| **Instalação** | Complexa | Simples |

## 📝 Notas

- O modelo Whisper é carregado na memória durante a execução
- Primeira execução pode demorar (download do modelo)
- Processamento de áudios longos pode levar vários minutos
- Recomendado usar em máquinas com pelo menos 4GB RAM
