# 🎯 Configuração Completa para Diarização de Locutores

## 📋 Visão Geral

A funcionalidade de identificação de locutores (speaker diarization) utiliza modelos avançados da biblioteca **pyannote.audio** do Hugging Face. Estes modelos são **"gated models"** que requerem autenticação e aceitação de termos de uso para garantir uso adequado e coleta de informações para melhoria da biblioteca.

### ⚡ Processo Simplificado (4 Passos)

1. **Criar conta no Hugging Face**: https://huggingface.co/join

2. **Aceitar os termos dos modelos específicos**:
   - Acesse: https://hf.co/pyannote/speaker-diarization-3.1
   - Clique em **"Agree and access repository"**
   - Acesse: https://hf.co/pyannote/segmentation-3.0
   - Clique em **"Agree and access repository"**

3. **Criar token de acesso**: https://hf.co/settings/tokens
   - Clique em **"New token"**
   - Nome: `pyannote-audio-access` (ou qualquer nome)
   - Tipo: **"Read"** (suficiente para baixar modelos)
   - Clique em **"Generate a token"**
   - **COPIE O TOKEN** - ele só aparece uma vez!

4. **Configurar o token na aplicação** (escolha uma opção abaixo)

## 🔧 Configuração do Token (Escolha UMA opção)

### 🏆 **Opção 1: Login via CLI (RECOMENDADO)**
```bash
# Instalar Hugging Face CLI (se não instalado)
pip install huggingface_hub

# Fazer login (abrirá uma página para colar o token)
huggingface-cli login
```
**Vantagens**: Mais seguro, token armazenado de forma criptografada

### 🌍 **Opção 2: Variável de Ambiente**
```bash
export HUGGINGFACE_HUB_TOKEN="hf_xxxxxxxxxxxxxxxxx"
```
Para tornar permanente, adicione ao seu `~/.bashrc` ou `~/.zshrc`:
```bash
echo 'export HUGGINGFACE_HUB_TOKEN="hf_xxxxxxxxxxxxxxxxx"' >> ~/.bashrc
source ~/.bashrc
```

### 📁 **Opção 3: Arquivo .env (Para desenvolvimento)**
Crie um arquivo `.env` na raiz do projeto:
```bash
# No diretório: /home/cfernandes/python/transcribe_audio/
echo 'HUGGINGFACE_HUB_TOKEN=hf_xxxxxxxxxxxxxxxxx' > .env
```

### 🔐 **Opção 4: Configuração Direta no Código**
Edite o arquivo `config.py` e adicione seu token:
```python
HUGGINGFACE_HUB_TOKEN = "hf_xxxxxxxxxxxxxxxxx"
```
⚠️ **Cuidado**: Não compartilhe o código com o token exposto!

---

## ✅ Validação da Configuração

### 1. **Verificação Rápida via Python**
```bash
python -c "
from services.diarization_service import load_diarization_model
try:
    model = load_diarization_model()
    print('✅ Diarização configurada com sucesso!')
    print(f'Modelo carregado: {type(model).__name__}')
except Exception as e:
    print(f'❌ Erro na configuração: {e}')
"
```

### 2. **Verificação via Interface Web**
1. Inicie a aplicação: `python app.py`
2. Acesse: http://localhost:5001
3. Procure pelo toggle "**Identificação de Locutores**"
4. Se habilitado = ✅ configurado | Se desabilitado = ❌ não configurado

### 3. **Verificação via API**
```bash
curl http://localhost:5001/check_diarization_availability
```
Resposta esperada: `{"available": true}`

---

## 🔍 Por que é Necessário?

### **Contexto dos Modelos "Gated"**
- Os modelos pyannote.audio são **open-source** (licença MIT)
- São **"gated"** para coletar informações do usuário
- Ajuda os desenvolvedores a entender como os modelos são usados
- **Não há cobrança** - é gratuito para uso acadêmico e comercial

### **Informações Coletadas**
- E-mail e organização (apenas para estatísticas)
- Ocasionalmente recebe e-mails sobre novos modelos
- Pode cancelar a qualquer momento

### **Modelos Utilizados**
- **pyannote/speaker-diarization-3.1**: Pipeline principal
- **pyannote/segmentation-3.0**: Modelo de segmentação
- **Versão**: pyannote.audio 3.1+ (já instalada)

---

## 🚀 Uso sem Diarização

A aplicação **funciona perfeitamente** mesmo sem a diarização configurada:

### **Funcionalidades Disponíveis**
- ✅ Transcrição de áudio simples
- ✅ Transcrição com timestamps
- ✅ Múltiplos formatos de arquivo
- ✅ Interface web completa

### **Funcionalidades Indisponíveis**
- ❌ Identificação de locutores
- ❌ Resumo de tempo por locutor
- ❌ Formato com "SPEAKER_00", "SPEAKER_01"

### **Comportamento da Interface**
- Toggle de diarização aparece **desabilitado/cinza**
- Mensagem: "Diarização não disponível - configure o token Hugging Face"
- Todas as outras funcionalidades funcionam normalmente

---

## 🛠️ Solução de Problemas

### **❌ "Token inválido" ou "Authentication failed"**
**Soluções:**
1. Verifique se copiou o token completo (inclui `hf_`)
2. Confirme que aceitou os termos dos **2 modelos** específicos
3. Aguarde 5-10 minutos após aceitar os termos
4. Teste com um novo token

### **❌ "Terms not accepted" ou "Access denied"**
**Soluções:**
1. Acesse novamente os links dos modelos:
   - https://hf.co/pyannote/speaker-diarization-3.1
   - https://hf.co/pyannote/segmentation-3.0
2. Certifique-se de estar logado na **mesma conta** do token
3. Clique em "Agree and access repository" em **ambos**

### **❌ "Out of memory" ou "CUDA error"**
**Soluções:**
1. **RAM insuficiente**: Diarização requer ~4GB livres
2. **GPU opcional**: Funciona em CPU, mas é mais lento
3. **Arquivos grandes**: Teste com áudios menores primeiro

### **❌ "No internet connection"**
**Soluções:**
1. Primeira execução precisa de internet para baixar modelos
2. Modelos são cached localmente após primeira execução
3. Verifique conexão e proxy se necessário

### **❌ "Pipeline failed to load"**
**Soluções:**
1. Atualize pyannote.audio: `pip install --upgrade pyannote.audio`
2. Limpe cache: `rm -rf ~/.cache/huggingface/`
3. Reinstale dependências: `pip install --force-reinstall torch torchaudio`

---

## 💡 Informações Técnicas

### **Requisitos de Sistema**
- **RAM**: 4GB+ livres para diarização
- **CPU**: Qualquer processador moderno
- **GPU**: Opcional (CUDA acelera o processamento)
- **Disco**: ~2GB para cache dos modelos

### **Performance Esperada**
- **Sem GPU**: ~30-60s para cada minuto de áudio
- **Com GPU**: ~10-20s para cada minuto de áudio
- **Primeira execução**: Mais lenta (download dos modelos)

### **Alternativas Comerciais**
Para uso em produção com alta demanda, considere:
- **pyannote.AI**: Versão comercial otimizada
- **Assembly AI**: API paga para diarização
- **Azure Speech Services**: Serviço da Microsoft

---

## 📞 Suporte e Documentação

### **Documentação Oficial**
- **pyannote.audio**: https://github.com/pyannote/pyannote-audio
- **Hugging Face**: https://huggingface.co/docs/hub/security-tokens
- **Speaker Diarization**: https://github.com/pyannote/pyannote-audio#speaker-diarization

### **Comunidade**
- **GitHub Issues**: https://github.com/pyannote/pyannote-audio/issues
- **Hugging Face Community**: https://huggingface.co/pyannote/speaker-diarization-3.1/discussions

### **Licenciamento**
- **pyannote.audio**: MIT License (gratuito para uso comercial)
- **Modelos**: MIT License (gratuito, apenas requer registro)
- **Esta aplicação**: Uso livre

---

**🎉 Após configurar o token, reinicie a aplicação e aproveite a identificação automática de locutores!**
