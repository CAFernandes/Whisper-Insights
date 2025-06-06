# 📋 Changelog - Whisper-Insights

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Corrigido
- 🐳 **Docker Health Check**: Resolvido problema de arquivo `ollama_service.py` vazio no container
- 🔍 **Error 500 no Health Check**: Corrigido falha na verificação de saúde da aplicação
- 📦 **Build do Container**: Melhorado processo de cópia de arquivos durante o build
- 🔧 **Diagnóstico**: Adicionados logs e verificações para identificar problemas de build

### Adicionado
- 📋 **Documentação Docker**: Seção dedicada a problemas com Docker no Troubleshooting
- 🔍 **Ferramentas de Debug**: Comandos para verificar status de containers e health checks
- 📊 **Logs Detalhados**: Melhor rastreamento de problemas em ambiente Docker

### Alterado
- 📚 **TROUBLESHOOTING.md**: Adicionada seção completa para problemas com Docker
- 🛠️ **CORRECOES_TECNICAS.md**: Documentada correção do health check Docker
- 🔄 **Processo de Build**: Validação automática de arquivos após reconstrução

## [Versão Anterior]

### Adicionado
- Documentação completa reorganizada
- Arquivo `.env.example` com todas as configurações
- Guias detalhados de instalação, configuração e solução de problemas
- Documentação completa da API REST
- Sistema de testes melhorado

### Alterado
- Projeto renomeado para "Whisper-Insights"
- Estrutura de documentação reorganizada na pasta `docs/`
- README principal atualizado e simplificado
- Removidas referências a documentos obsoletos

## [2.0.0] - 2024-05-15

### Adicionado
- ✨ **Identificação de Locutores**: Sistema completo de diarização com pyannote.audio
- 🧠 **Insights com IA**: Integração com Ollama + Llama para análise inteligente
- 🎤 **Diarização Automática**: Detecção de quem fala em cada momento
- 📊 **Resumos Estatísticos**: Tempo de fala por pessoa
- 🔄 **Sistema de Tarefas**: Processamento assíncrono com status em tempo real
- 🧪 **Testes Completos**: Suíte automatizada de testes unitários e integração

### Melhorado
- 🔧 **Interface Web**: Design moderno e responsivo
- ⚡ **Performance**: Threading para melhor experiência
- 🛠️ **Tratamento de Erros**: Sistema robusto de fallbacks
- 📁 **Suporte a Formatos**: Incluindo KWF com fallback automático
- 🔒 **Segurança**: Validação completa de arquivos

### Corrigido
- 🐛 **Arquivos KWF**: Erro "Cannot set attribute 'src'" resolvido
- 🔄 **Compatibilidade**: pyannote.audio 3.3.2 totalmente suportado
- 🔕 **Warnings**: Mensagens desnecessárias do SpeechBrain suprimidas
- 🎯 **Token HF**: Configuração automática via .env funcionando

## [1.5.0] - 2024-03-10

### Adicionado
- 🌐 **Interface Web**: Migração completa do desktop para web
- 📱 **Design Responsivo**: Funciona em desktop e mobile
- 🎯 **Drag & Drop**: Upload intuitivo de arquivos
- 🔄 **Processamento Assíncrono**: Threading para melhor performance

### Alterado
- 🏗️ **Arquitetura**: Refatoração completa para Flask
- 📁 **Estrutura**: Código organizado em módulos (services, helpers)
- ⚙️ **Configuração**: Sistema centralizado em config.py

### Removido
- 🖥️ **Interface Desktop**: Tkinter removido em favor da web

## [1.0.0] - 2024-01-15

### Adicionado
- 🎙️ **Transcrição Básica**: Usando OpenAI Whisper
- 🖥️ **Interface Desktop**: GUI com Tkinter
- 📝 **Múltiplos Formatos**: Suporte a mp3, wav, m4a, ogg, flac
- ⏰ **Timestamps**: Transcrição com marcação temporal
- 💾 **Exportação**: Salvar resultados em arquivo

### Funcionalidades Iniciais
- Transcrição de áudio para texto
- Interface gráfica simples
- Suporte básico a formatos de áudio
- Modelo Whisper configurável

---

## Tipos de Mudanças

- **Adicionado** para novas funcionalidades
- **Alterado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para mudanças relacionadas à segurança

## Versionamento

Este projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/):

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (0.X.0): Funcionalidades adicionadas de forma compatível
- **PATCH** (0.0.X): Correções de bugs compatíveis

## Processo de Release

1. Atualizar este CHANGELOG
2. Atualizar versão em `config.py` (se aplicável)
3. Executar testes: `python -m pytest tests/ -v`
4. Verificar documentação atualizada
5. Criar tag de versão: `git tag v2.0.0`
6. Push com tags: `git push --tags`

## Compatibilidade

### Versão Atual (2.0.0+)
- **Python**: 3.8+
- **Dependências**: requirements-web.txt
- **Configuração**: Arquivo .env
- **API**: REST endpoints estáveis

### Versões Anteriores
- **1.x**: Interface desktop (descontinuada)
- **Migração**: Não há migração automática de 1.x para 2.x

## Roadmap Futuro

### 🔮 Próximas Versões
- [ ] **2.1.0**: Autenticação e multi-usuários
- [ ] **2.2.0**: Banco de dados para histórico
- [ ] **2.3.0**: API de webhooks
- [ ] **3.0.0**: Reescrita em FastAPI (considerando)

### 🎯 Melhorias Planejadas
- [ ] Cache inteligente de resultados
- [ ] Suporte a mais idiomas
- [ ] Interface em tempo real (WebSocket)
- [ ] Integração com serviços de nuvem
- [ ] Docker oficial
- [ ] Métricas e analytics

---

**📅 Última atualização**: Junho 2025
**👥 Mantenedores**: Equipe Whisper-Insights
