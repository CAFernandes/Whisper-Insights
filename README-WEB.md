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

---

# 🚀 Sobre o Projeto

Este projeto converteu uma aplicação desktop de transcrição de áudio (tkinter) em uma **aplicação web moderna** baseada em Flask, com integração de IA para geração de insights usando Whisper (OpenAI) e Ollama (Llama 3.2:3b).

## 🛠️ Funcionalidades Principais

- **Transcrição automática de áudio** com Whisper AI
- **Geração de insights** com Ollama (Llama 3.2:3b via Docker)
- **Interface web responsiva** (HTML5, CSS3, JS)
- **Upload drag & drop** e seleção de arquivos
- **Status em tempo real** do processamento
- **Retry de insights** com prompt customizável e seleção de modelo
- **Limpeza automática** de arquivos temporários
- **Validação robusta** de arquivos e segurança
- **Testes automatizados** (unitários e integração)

## 🧠 Exemplo de Insights Gerados

```
**RESUMO EXECUTIVO**
O áudio contém uma conversa entre duas pessoas, identificadas como David e um confino, que discutem sobre um negócio a ser resolvido...

**TEMAS PRINCIPAIS**
1. Negócios e Problemas
2. Vídeo e Tecnologia
3. Comunicação e Coordenação

**OBJETIVOS IDENTIFICADOS**
* Conhecer o conceito de vídeo "Conor Héctor"
* Resolver o problema com o grupo de integradores
* Comunicar-se de forma eficaz sobre os objetivos...

**CLASSIFICAÇÃO**
* Tipo de conteúdo: Conversa informal
* Tom geral: Urgente e desesperado
```

## 🏗️ Arquitetura

### Backend (Flask)
- Flask 3.1.1
- OpenAI Whisper (transcrição)
- Requests (Ollama)
- Threading para processamento assíncrono
- API RESTful

### Frontend
- HTML5, CSS3, JavaScript ES6
- Drag & drop, status real-time, responsividade

### IA e Processamento
- Ollama (Docker) + Llama 3.2:3b
- PyTorch (Whisper)
- Timeout e tratamento de erros robusto

## 📊 Testes Automatizados

- **test_complete_workflow.py**: Testa upload, transcrição, insights, erros e retry
- **test_units.py**: Testes unitários para utilitários, serviços e validações
- **Cobertura**: Upload, transcrição, insights, erros, retry, múltiplos formatos

## 📁 Estrutura Recomendada

```
transcribe_audio/
├── app.py                  # Servidor Flask principal
├── config.py               # Configurações centralizadas
├── helpers/                # Utilitários (file_utils.py)
├── services/               # Lógica de negócio (whisper, ollama, task)
├── templates/index.html    # Interface web
├── static/                 # Arquivos estáticos
├── uploads/                # Arquivos temporários
├── requirements-web.txt    # Dependências
├── start_web.sh            # Script de inicialização
├── test_complete_workflow.py # Teste de integração
├── test_units.py           # Testes unitários
└── ...
```

## 🏆 Diferenciais

- Conversão desktop → web com arquitetura profissional
- IA de ponta (Whisper + Llama)
- Testes completos e automação
- Interface moderna e usável
- Pronto para produção (basta rodar o Flask)

## 💡 Dicas de Produção

- Para produção, use Gunicorn/Nginx
- Considere integrar banco de dados para histórico
- Adicione autenticação para multiusuário
- Monitore logs e uso de recursos

---

Para mais detalhes, veja também o arquivo `PROJETO_CONCLUIDO.md`.
