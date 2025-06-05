# 🧪 Guia de Testes - Whisper-Insights

Esta pasta contém todos os testes automatizados, demonstrações e validações do sistema de transcrição de áudio com IA.

## 📁 Estrutura dos Testes

### 🐍 **Testes Python Automatizados**
- **`test_units.py`** - Testes unitários de funções principais
- **`test_complete_workflow.py`** - Teste completo do fluxo de transcrição
- **`test_dialogue_view.py`** - Teste da visualização de diálogo com diarização
- **`test_diarization_insights.py`** - Teste específico dos insights de diarização

### 🌐 **Testes de Interface Web**
- **`test_dialogue.html`** - Página de teste da visualização de diálogo
- **`test_javascript_functions.html`** - Teste das funções JavaScript

### 🎵 **Arquivos de Áudio para Teste**
- **`teste_audio.wav`** - Arquivo WAV para testes básicos
- **`teste_audio.m4a`** - Arquivo M4A para testes de compatibilidade
- **`teste_audio.ogg`** - Arquivo OGG para testes de formato
- **`teste_audio.kwf`** - Arquivo KWF para teste de fallback automático

### 🔧 **Scripts e Utilitários**
- **`demo.sh`** - Script de demonstração completa do sistema
- **`invalid_file.txt`** - Arquivo inválido para teste de validação

## 🚀 Executando os Testes

### Preparação do Ambiente
```bash
# Ativar ambiente virtual
source transcribe/bin/activate

# Instalar dependências de teste (se necessário)
pip install pytest

# Verificar se aplicação está funcionando
python app.py &
sleep 3
curl -f http://localhost:5001
```

### Testes Unitários
```bash
# Todos os testes unitários
python -m pytest tests/test_units.py -v

# Teste específico
python -m pytest tests/test_units.py::test_whisper_service -v
python -m pytest tests/test_units.py::test_file_validation -v
```

### Testes de Integração
```bash
# Workflow completo (requer Whisper funcionando)
python tests/test_complete_workflow.py

# Teste de diarização (requer token Hugging Face)
python tests/test_diarization_insights.py

# Visualização de diálogo
python tests/test_dialogue_view.py
```

### Todos os Testes
```bash
# Execução completa
python -m pytest tests/ -v

# Com saída detalhada
python -m pytest tests/ -v -s

# Apenas testes que passam
python -m pytest tests/ --tb=short
```

### Demonstração Interativa
```bash
# Script de demonstração completa
./tests/demo.sh

# Torna executável se necessário
chmod +x tests/demo.sh
```

## 📊 Tipos de Teste

### 🔍 **Testes Unitários (`test_units.py`)**
- Validação de arquivos
- Configuração do sistema
- Utilitários de arquivo
- Serviços individuais
- Tratamento de erros

### 🔄 **Testes de Workflow (`test_complete_workflow.py`)**
- Upload de arquivo
- Transcrição básica
- Geração de insights
- Fluxo completo end-to-end
- Limpeza automática

### 🎭 **Testes de Diarização (`test_diarization_insights.py`)**
- Identificação de locutores
- Geração de insights com diarização
- Fallback automático
- Integração Hugging Face

### 🌐 **Testes de Interface (`test_dialogue_view.py`)**
- Renderização HTML
- Funções JavaScript
- Visualização de resultados
- Responsividade

## ✅ Checklist de Validação

### Antes de Executar Testes
- [ ] Ambiente virtual ativo (`source transcribe/bin/activate`)
- [ ] Dependências instaladas (`pip install -r requirements-web.txt`)
- [ ] Arquivo `.env` configurado
- [ ] Aplicação iniciando sem erros (`python app.py`)

### Testes Básicos (Devem Sempre Passar)
- [ ] `test_units.py` - Validação básica
- [ ] Upload de arquivo funciona
- [ ] Transcrição básica funciona
- [ ] Interface web carrega

### Testes Avançados (Requerem Configuração)
- [ ] `test_diarization_insights.py` - Requer token Hugging Face
- [ ] Geração de insights - Requer Ollama rodando
- [ ] Todos os formatos de arquivo

## 🐛 Debugging de Testes

### Testes Falhando
```bash
# Executar com debugging detalhado
python -m pytest tests/ -v -s --tb=long

# Executar teste específico com prints
python -m pytest tests/test_units.py::test_specific -v -s

# Verificar logs durante testes
tail -f app.log
```

### Problemas Comuns
```bash
# Erro: "Application not running"
# Solução: Verificar se app.py está rodando
ps aux | grep python
python app.py &

# Erro: "No module named 'pytest'"
# Solução: Instalar pytest
pip install pytest

# Erro: "Permission denied"
# Solução: Ajustar permissões
chmod +x tests/demo.sh
chmod 755 uploads/
```

### Verificação de Ambiente
```bash
# Script de verificação rápida
python -c "
import sys, os
print(f'Python: {sys.version}')
print(f'Working dir: {os.getcwd()}')
print(f'Uploads exists: {os.path.exists(\"uploads\")}')
try:
    import whisper, flask, torch
    print('✅ Dependências principais OK')
except ImportError as e:
    print(f'❌ Dependência faltando: {e}')
"
```

## 📈 Relatórios de Teste

### Executar com Relatório
```bash
# Relatório simples
python -m pytest tests/ --tb=short

# Relatório detalhado
python -m pytest tests/ -v --tb=long

# Salvar resultado em arquivo
python -m pytest tests/ -v > test_results.txt 2>&1
```

### Cobertura de Código (Opcional)
```bash
# Instalar coverage
pip install pytest-cov

# Executar com cobertura
python -m pytest tests/ --cov=services --cov=helpers --cov-report=html

# Ver relatório
open htmlcov/index.html
```

## 🔧 Criando Novos Testes

### Template para Novo Teste
```python
# tests/test_nova_funcionalidade.py
import unittest
import sys
import os

# Adicionar pasta raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.meu_service import minha_funcao

class TestNovaFuncionalidade(unittest.TestCase):

    def setUp(self):
        """Preparação antes de cada teste"""
        pass

    def test_funcionalidade_basica(self):
        """Teste da funcionalidade básica"""
        resultado = minha_funcao("input_teste")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.status, "success")

    def tearDown(self):
        """Limpeza após cada teste"""
        pass

if __name__ == "__main__":
    unittest.main()
```

### Convenções de Teste
- **Nomenclatura**: `test_*.py` para arquivos, `test_*` para métodos
- **Organização**: Um arquivo por serviço/módulo
- **Isolamento**: Cada teste deve ser independente
- **Limpeza**: Sempre limpar recursos após testes

---

**💡 Dica**: Execute `./tests/demo.sh` para uma demonstração completa do sistema ou `python -m pytest tests/ -v` para validação rápida da instalação.
