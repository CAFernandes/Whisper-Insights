# ⚡ Guia Rápido: Configurar Diarização em 5 Minutos

## 🎯 O que é isso?
Permite identificar **quem está falando** em gravações com múltiplas pessoas.

**Exemplo de resultado:**
```
[00:00 - 00:03] SPEAKER_00: Olá, como você está?
[00:04 - 00:07] SPEAKER_01: Estou bem, obrigado!
[00:08 - 00:11] SPEAKER_00: Que bom ouvir isso.
```

---

## 🚀 Configuração Rápida (5 passos)

### 1️⃣ Criar conta Hugging Face
🔗 https://huggingface.co/join

### 2️⃣ Aceitar termos dos modelos
🔗 https://hf.co/pyannote/speaker-diarization-3.1 → **"Agree and access repository"**
🔗 https://hf.co/pyannote/segmentation-3.0 → **"Agree and access repository"**

### 3️⃣ Criar token
🔗 https://hf.co/settings/tokens → **"New token"** → Tipo: **"Read"** → **Copiar token**

### 4️⃣ Configurar token (escolha UMA opção)

**🏆 MAIS FÁCIL:**
```bash
pip install huggingface_hub
huggingface-cli login
# Cole seu token quando solicitado
```

**OU variável de ambiente:**
```bash
export HUGGINGFACE_HUB_TOKEN="hf_xxxxxxxxxxxxxxxxx"
```

**OU arquivo .env:**
```bash
echo 'HUGGINGFACE_HUB_TOKEN=hf_xxxxxxxxxxxxxxxxx' > .env
```

### 5️⃣ Testar
```bash
python app.py
# Acesse http://localhost:5001
# Procure pelo toggle "Identificação de Locutores"
```

---

## ✅ Status Atual (Maio 2025)

### 🎉 **100% Funcional**
- ✅ Token do Hugging Face detectado automaticamente
- ✅ Modelo carregado com sucesso na GPU/CPU
- ✅ Interface mostra "Diarização disponível"
- ✅ Processamento funcionando para todos os formatos
- ✅ Warnings desnecessários suprimidos

### 🔧 **Melhorias Implementadas**
- ✅ **Detecção automática** do token via arquivo .env
- ✅ **Logs informativos** para debug ("Token encontrado", "Modelo carregado")
- ✅ **Compatibilidade** com pyannote.audio 3.3.2 mais recente
- ✅ **Fallback inteligente** para arquivos problemáticos (KWF)
- ✅ **Interface limpa** sem warnings do SpeechBrain

---

## ✅ Funcionou?

### **✅ SIM** - Toggle habilitado
- Parabéns! Agora você pode identificar locutores
- Faça upload de um áudio e ative a diarização

### **❌ NÃO** - Toggle desabilitado

**Verificações rápidas:**
1. Aceitou os termos dos **2 modelos**?
2. Token começa com `hf_`?
3. Aguardou 5 minutos após aceitar termos?
4. Reiniciou a aplicação?

**Teste manual:**
```bash
python -c "
from services.diarization_service import load_diarization_model
print('✅ Funcionou!' if load_diarization_model() else '❌ Erro')
"
```

---

## 💡 Dicas

### **🎧 Melhores resultados:**
- Áudio claro, sem muito ruído
- Pessoas falando alternadamente (não muito simultâneo)
- Arquivo MP3/WAV de boa qualidade

### **⏱️ Performance:**
- Primeira vez: ~2-3 minutos (baixa modelos)
- Depois: ~30-60s por minuto de áudio

### **🔄 Sem diarização:**
- Aplicação funciona normalmente
- Apenas não identifica locutores
- Transcrição e timestamps funcionam

---

## 🆘 Precisa de Ajuda?

📖 **Guia completo:** `DIARIZATION_SETUP.md`
🐛 **Problemas:** Verifique a seção "Solução de problemas" no guia completo
💬 **Dúvidas:** https://github.com/pyannote/pyannote-audio/discussions

---

**🎉 Em 5 minutos você terá identificação automática de locutores funcionando!**
