# 🧪 Pasta de Testes

Esta pasta contém todos os arquivos relacionados a testes, demonstrações e validações do sistema de transcrição de áudio.

## 📁 Estrutura dos Testes

### 🐍 **Testes Python**
- `test_units.py` - Testes unitários das funções principais
- `test_complete_workflow.py` - Teste completo do fluxo de transcrição
- `test_dialogue_view.py` - Teste da visualização de diálogo com diarização
- `test_diarization_insights.py` - Teste dos insights de diarização

### 🌐 **Testes HTML/JavaScript**
- `test_dialogue.html` - Página de teste da visualização de diálogo
- `test_javascript_functions.html` - Teste das funções JavaScript (showStatus, showProgress)

### 🎵 **Arquivos de Áudio para Teste**
- `teste_audio.wav` - Arquivo WAV de teste
- `teste_audio.m4a` - Arquivo M4A de teste
- `teste_audio.ogg` - Arquivo OGG de teste
- `teste_audio.kwf` - Arquivo de formato específico para teste

### 🔧 **Scripts e Utilitários**
- `demo.sh` - Script de demonstração do sistema
- `invalid_file.txt` - Arquivo inválido para teste de validação de formato

## 🚀 Como Executar os Testes

### Testes Python
```bash
# Ativar ambiente virtual
source transcribe/bin/activate

# Executar todos os testes
python -m pytest tests/

# Executar teste específico
python tests/test_units.py
python tests/test_complete_workflow.py
python tests/test_dialogue_view.py
python tests/test_diarization_insights.py
```

### Testes HTML
```bash
# Iniciar servidor Flask
python app.py

# Abrir no navegador:
# http://localhost:5001/
# file:///.../tests/test_dialogue.html
# file:///.../tests/test_javascript_functions.html
```

### Script de Demonstração
```bash
# Executar demonstração completa
chmod +x tests/demo.sh
./tests/demo.sh
```

## 📊 Cobertura dos Testes

### ✅ **Funcionalidades Testadas**
- Upload e validação de arquivos
- Transcrição com Whisper
- Diarização de locutores
- Geração de insights com Ollama
- Interface web e JavaScript
- Visualização de diálogo
- Processamento de diferentes formatos de áudio

### 🔄 **Fluxos Testados**
- Fluxo completo: Upload → Transcrição → Diarização → Insights
- Tratamento de erros e validações
- Interface do usuário e interações
- Integração entre componentes

## 🛠️ **Desenvolvimento**

Para adicionar novos testes:

1. **Testes Python:** Criar arquivo `test_nome_funcionalidade.py`
2. **Testes HTML:** Criar arquivo `test_nome_interface.html`
3. **Dados de teste:** Adicionar arquivos de exemplo nesta pasta
4. **Documentar:** Atualizar este README com as novas funcionalidades

## 📝 **Notas**

- Todos os testes são independentes e podem ser executados isoladamente
- Os arquivos de áudio são pequenos e servem apenas para validação
- Os testes HTML podem ser abertos diretamente no navegador
- Use sempre o ambiente virtual para executar os testes Python

---

**Mantido por:** Sistema de Transcrição de Áudio com Diarização
**Última atualização:** Maio 2025
