# 🎙️ Transcritor de Áudio Web

Uma aplicação web moderna para transcrição de áudio usando inteligência artificial Whisper da OpenAI e geração de insights com Ollama (Llama 3.2:3b).

## ✨ Características

- 🌐 Interface web responsiva e intuitiva
- 🎯 Drag & Drop para upload de arquivos
- 🔄 Processamento assíncrono (threading)
- 📱 Design adaptável (desktop/mobile)
- ⚡ Suporte a múltiplos formatos: mp3, wav, m4a, ogg, flac, mp4, avi, kwf
- 🧠 Geração de insights com IA (Ollama + Llama)
- 🔒 Validação e segurança de arquivos
- 🧹 Limpeza automática de uploads
- 🧪 Testes automatizados (unitários e integração)

## 🚀 Como usar

```bash
# 1. Ative o ambiente virtual
source transcribe/bin/activate

# 2. Instale as dependências
pip install -r requirements-web.txt

# 3. Inicie a aplicação
python app.py
```

Ou use o script:
```bash
./start_web.sh
```

Acesse em: http://localhost:5000 ou http://localhost:5001

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

Para mais detalhes, veja também o arquivo `PROJETO_CONCLUIDO.md` e o `README-WEB.md`.