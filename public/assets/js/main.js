let currentTaskId = null;
let statusCheckInterval = null;
const defaultInsightsPrompt = "Analise a seguinte transcrição e forneça um resumo dos principais pontos, identifique os principais tópicos discutidos e quaisquer ações ou decisões mencionadas. Considere o tom geral da conversa e quaisquer sentimentos expressos. O texto é: {{text}}";

// Verificar modelo na inicialização
window.onload = function () {
  checkModel();
  checkOllama();
  checkDiarizationAvailability();
  setupDragAndDrop();
  setupFileInput();
};

function checkModel() {
  const indicator = document.getElementById('whisper-indicator');
  if (!indicator) {
    console.warn('Elemento whisper-indicator não encontrado');
    return;
  }
  indicator.className = 'status-indicator loading';
  fetch('http://localhost:5001/check_model')
  .then(response => response.json())
  .then(data => {
      const modelStatus = document.getElementById('whisper-status');

      if (!modelStatus || !indicator) {
        console.warn('Elementos de status do Whisper não encontrados');
        return;
      }

      if (data.success) {
        modelStatus.textContent = data.message;
        indicator.className = 'status-indicator online';
      } else {
        modelStatus.textContent = data.message;
        indicator.className = 'status-indicator error';
      }
    })
    .catch(error => {
      const modelStatus = document.getElementById('whisper-status');
      const indicator = document.getElementById('whisper-indicator');

      if (modelStatus) {
        modelStatus.textContent = 'Erro ao verificar modelo: ' + error;
      }
      if (indicator) {
        indicator.className = 'status-indicator error';
      }
    });
}

function checkOllama() {
  const indicator = document.getElementById('ollama-indicator');
  if (!indicator) {
    console.warn('Elemento ollama-indicator não encontrado');
    return;
  }
  indicator.className = 'status-indicator loading';
  fetch('http://localhost:5001/check_ollama')
    .then(response => response.json())
    .then(data => {
      const ollamaStatus = document.getElementById('ollama-status');

      if (!ollamaStatus || !indicator) {
        console.warn('Elementos de status do Ollama não encontrados');
        return;
      }

      if (data.connected && data.count > 0) {
        ollamaStatus.textContent = `Conectado - ${data.count} modelo(s): ${data.models.join(', ')}`;
        indicator.className = 'status-indicator online';
      } else if (data.connected && data.count === 0) {
        ollamaStatus.textContent = 'Conectado mas sem modelos instalados';
        indicator.className = 'status-indicator warning';
      } else {
        ollamaStatus.textContent = 'Não está disponível (insights desabilitados)';
        indicator.className = 'status-indicator error';
      }
    })
    .catch(error => {
      const ollamaStatus = document.getElementById('ollama-status');
      const indicator = document.getElementById('ollama-indicator');

      if (ollamaStatus) {
        ollamaStatus.textContent = 'Erro ao verificar Ollama: ' + error;
      }
      if (indicator) {
        indicator.className = 'status-indicator error';
      }
    });
}

function checkDiarizationAvailability() {
  const indicator = document.getElementById('diarization-indicator');
  if (!indicator) {
    console.warn('Elemento diarization-indicator não encontrado');
    return;
  }
  indicator.className = 'status-indicator loading';
  fetch('http://localhost:5001/check_diarization_availability')
    .then(response => response.json())
    .then(data => {
      const diarizationStatus = document.getElementById('diarization-status');
      const diarizationToggle = document.getElementById('use-diarization');

      if (!diarizationStatus || !indicator) {
        console.warn('Elementos de status da diarização não encontrados');
        return;
      }

      if (data.available) {
        diarizationStatus.textContent = 'Disponível';
        indicator.className = 'status-indicator online';
        if (diarizationToggle) {
          diarizationToggle.disabled = false;
        }
      } else {
        diarizationStatus.textContent = 'Indisponível - configure token Hugging Face';
        indicator.className = 'status-indicator error';
        if (diarizationToggle) {
          diarizationToggle.disabled = true;
          diarizationToggle.checked = false;
        }
      }
    })
    .catch(error => {
      const diarizationStatus = document.getElementById('diarization-status');
      const indicator = document.getElementById('diarization-indicator');
      const diarizationToggle = document.getElementById('use-diarization');

      if (diarizationStatus) {
        diarizationStatus.textContent = 'Erro ao verificar: ' + error;
      }
      if (indicator) {
        indicator.className = 'status-indicator error';
      }
      if (diarizationToggle) {
        diarizationToggle.disabled = true;
      }
    });
}

function setupDragAndDrop() {
  const uploadSection = document.getElementById('upload-area');

  if (!uploadSection) {
    console.warn('Elemento upload-area não encontrado');
    return;
  }

  uploadSection.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadSection.classList.add('dragover');
  });

  uploadSection.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragover');
  });

  uploadSection.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  });
}

function setupFileInput() {
  const fileInput = document.getElementById('file-input');

  if (!fileInput) {
    console.warn('Elemento file-input não encontrado');
    return;
  }

  fileInput.addEventListener('change', function (e) {
    if (e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  });
}

function handleFileSelection(file) {
  const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/flac', 'video/mp4', 'video/avi', 'audio/kwf', 'application/octet-stream']; // Adicionado 'audio/kwf' e um genérico
  const allowedExtensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.mp4', '.avi', '.kwf'];

  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

  if (!allowedExtensions.includes(fileExtension)) {
    showStatus('Formato de arquivo não suportado. Use: mp3, wav, m4a, ogg, flac, mp4, avi, kwf', 'error');
    return;
  }

  // Atualiza a exibição do arquivo selecionado
  const fileName = document.getElementById('file-name');
  const fileSize = document.getElementById('file-size');
  const fileInfo = document.getElementById('file-info');
  const transcriptionOptions = document.getElementById('transcription-options');

  if (fileName) {
    fileName.textContent = file.name;
  }

  if (fileSize) {
    fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
  }

  if (fileInfo) {
    fileInfo.style.display = 'block';
  }

  if (transcriptionOptions) {
    transcriptionOptions.style.display = 'block';
  }

  // Atualiza o input de arquivo
  const fileInput = document.getElementById('file-input');
  if (fileInput) {
    fileInput.files = createFileList(file);
  }
}

function createFileList(file) {
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  return dataTransfer.files;
}

function startTranscription() {
  const fileInput = document.getElementById('file-input');
  if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
    showStatus('Por favor, selecione um arquivo primeiro.', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  // Adiciona opção de diarização
  const diarizationEnabled = document.getElementById('use-diarization');
  if (diarizationEnabled) {
    formData.append('enable_diarization', diarizationEnabled.checked);
  }

  showStatus('Enviando arquivo...', 'loading');
  showProgress(true);

  fetch('http://localhost:5001/upload', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        currentTaskId = data.task_id;
        showStatus(data.message, 'loading');
        startStatusCheck();
      } else {
        showStatus(data.message, 'error');
        showProgress(false);
      }
    })
    .catch(error => {
      showStatus('Erro no upload: ' + error, 'error');
      showProgress(false);
    });
}

function startStatusCheck() {
  if (statusCheckInterval) {
    clearInterval(statusCheckInterval);
  }

  statusCheckInterval = setInterval(() => {
    if (currentTaskId) {
      checkTranscriptionStatus();
    }
  }, 2000);
}

function checkTranscriptionStatus() {
  fetch(`http://localhost:5001/status/${currentTaskId}`)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'processing') {
        showStatus(data.progress || 'Processando transcrição...', 'loading');
      } else if (data.status === 'transcription_completed') {
        showStatus(data.message || 'Transcrição Concluída!', 'success');

        // Atualiza o resultado da transcrição
        displayTranscriptionResult(data);

        // Mostra a seção de resultados
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
          resultsSection.style.display = 'block';
        }

        // Prepara para geração de Insights
        populateOllamaModels(data.available_ollama_models || []);
        fetchAndDisplayPrompt(currentTaskId, data.current_prompt);

        const generateBtn = document.getElementById('generate-insights-btn');
        if (generateBtn) {
          generateBtn.textContent = '💡 Gerar Insights';
        }

        showProgress(false);
        clearInterval(statusCheckInterval);

      } else if (data.status === 'generating_insights') {
        showStatus(data.progress || 'Gerando insights...', 'loading');

      } else if (data.status === 'completed_with_insights') {
        showStatus(data.message || 'Insights gerados com sucesso!', 'success');

        const insightsResult = document.getElementById('insights-result');
        if (insightsResult) {
          insightsResult.textContent = data.insights;
        }

        const insightsContainer = document.getElementById('insights-result-container');
        if (insightsContainer) {
          insightsContainer.style.display = 'block';
        }

        fetchAndDisplayPrompt(currentTaskId, data.current_prompt, data.selected_model);

        const generateBtn = document.getElementById('generate-insights-btn');
        if (generateBtn) {
          generateBtn.textContent = '🔁 Regerar Insights';
        }

        showProgress(false);
        clearInterval(statusCheckInterval);

      } else if (data.status === 'error_insights') {
        showStatus(data.message || 'Erro ao gerar insights.', 'error');

        const insightsResult = document.getElementById('insights-result');
        if (insightsResult) {
          insightsResult.textContent = data.message || 'Falha ao gerar insights.';
        }

        const insightsContainer = document.getElementById('insights-result-container');
        if (insightsContainer) {
          insightsContainer.style.display = 'block';
        }

        fetchAndDisplayPrompt(currentTaskId, data.current_prompt, data.selected_model);

        const generateBtn = document.getElementById('generate-insights-btn');
        if (generateBtn) {
          generateBtn.textContent = '🔁 Tentar Novamente Insights';
        }

        showProgress(false);
        clearInterval(statusCheckInterval);

      } else if (data.status === 'error') {
        showStatus(data.message, 'error');
        showProgress(false);
        clearInterval(statusCheckInterval);
      } else if (data.status === 'not_found') {
        showStatus('Tarefa não encontrada.', 'error');
        showProgress(false);
        clearInterval(statusCheckInterval);
      }
    })
    .catch(error => {
      showStatus('Erro ao verificar status: ' + error, 'error');
      showProgress(false);
      clearInterval(statusCheckInterval);
    });
}

function populateOllamaModels(models) {
  const selectElement = document.getElementById('ollama-model');

  if (!selectElement) {
    console.warn('Elemento ollama-model não encontrado');
    return;
  }

  selectElement.innerHTML = ''; // Limpa opções existentes
  if (models && models.length > 0) {
    models.forEach(modelName => {
      const option = document.createElement('option');
      option.value = modelName;
      option.textContent = modelName;
      selectElement.appendChild(option);
    });
    selectElement.disabled = false;
    const generateBtn = document.getElementById('generate-insights-btn');
    if (generateBtn) {
      generateBtn.disabled = false;
    }
  } else {
    const option = document.createElement('option');
    option.value = "";
    option.textContent = "Nenhum modelo Ollama disponível";
    selectElement.appendChild(option);
    selectElement.disabled = true;
    const generateBtn = document.getElementById('generate-insights-btn');
    if (generateBtn) {
      generateBtn.disabled = true;
    }
  }
}

function fetchAndDisplayPrompt(taskId, promptFromServer, selectedModel) {
  const promptTextarea = document.getElementById('insights-prompt');

  if (!promptTextarea) {
    console.warn('Elemento insights-prompt não encontrado');
    return;
  }

  if (promptFromServer) {
    promptTextarea.value = promptFromServer;
  } else {
    // Usa o defaultInsightsPrompt injetado pelo Flask se nenhum prompt específico da tarefa for encontrado
    const defaultPrompt = window.defaultInsightsPrompt || defaultInsightsPrompt;
    promptTextarea.value = defaultPrompt !== "{{DEFAULT_INSIGHTS_PROMPT_PLACEHOLDER}}" ? defaultPrompt : "Gere insights sobre o seguinte texto: {{text}}";
  }

  if (selectedModel) {
    const modelSelect = document.getElementById('ollama-model');
    if (modelSelect) {
      modelSelect.value = selectedModel;
    }
  }
}

function generateOrRetryInsights() { // Renomeada de retryInsightsGeneration
  if (!currentTaskId) {
    showStatus('Nenhuma tarefa ativa para gerar insights.', 'error');
    return;
  }

  const customPrompt = document.getElementById('insights-prompt');
  if (!customPrompt || !customPrompt.value.trim()) {
    showStatus('O prompt para insights não pode estar vazio.', 'error');
    return;
  }

  const selectedModel = document.getElementById('ollama-model');
  if (!selectedModel || !selectedModel.value) {
    showStatus('Por favor, selecione um modelo Ollama.', 'error');
    return;
  }

  showStatus('Solicitando insights...', 'loading');

  const insightsResult = document.getElementById('insights-result');
  const insightsLoading = document.getElementById('insights-loading');
  const generateBtn = document.getElementById('generate-insights-btn');

  if (insightsResult) {
    insightsResult.textContent = 'Gerando insights com o modelo ' + selectedModel.value + '...';
  }

  if (insightsLoading) {
    insightsLoading.style.display = 'block';
  }

  if (generateBtn) {
    generateBtn.disabled = true;
  }

  fetch(`http://localhost:5001/retry_insights/${currentTaskId}`, // Endpoint pode ser renomeado no backend para /generate_insights
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt: customPrompt.value,
        model_name: selectedModel.value // Envia o modelo selecionado
      })
    })
    .then(response => response.json())
    .then(data => {
      if (generateBtn) {
        generateBtn.disabled = false;
      }

      if (insightsLoading) {
        insightsLoading.style.display = 'none';
      }

      if (data.success) {
        showStatus(data.message || 'Insights gerados com sucesso!', 'success');

        if (insightsResult) {
          insightsResult.textContent = data.insights;
        }

        const insightsContainer = document.getElementById('insights-result-container');
        if (insightsContainer) {
          insightsContainer.style.display = 'block';
        }

        if (data.current_prompt && customPrompt) {
          customPrompt.value = data.current_prompt;
        }
        if (data.selected_model && selectedModel) {
          selectedModel.value = data.selected_model;
        }

        if (generateBtn) {
          generateBtn.textContent = '🔁 Regerar Insights';
        }
      } else {
        showStatus(data.message || 'Erro ao gerar insights.', 'error');

        if (insightsResult) {
          insightsResult.textContent = data.message || 'Falha ao gerar insights.';
        }

        const insightsContainer = document.getElementById('insights-result-container');
        if (insightsContainer) {
          insightsContainer.style.display = 'block';
        }

        if (generateBtn) {
          generateBtn.textContent = '🔁 Tentar Novamente Insights';
        }
      }
    })
    .catch(error => {
      if (generateBtn) {
        generateBtn.disabled = false;
      }

      if (insightsLoading) {
        insightsLoading.style.display = 'none';
      }

      showStatus('Erro na requisição para gerar insights: ' + error, 'error');

      if (insightsResult) {
        insightsResult.textContent = 'Erro na comunicação com o servidor.';
      }

      const insightsContainer = document.getElementById('insights-result-container');
      if (insightsContainer) {
        insightsContainer.style.display = 'block';
      }

      if (generateBtn) {
        generateBtn.textContent = '🔁 Tentar Novamente Insights';
      }
    });
}

function displayTranscriptionResult(data) {
  // Armazena os dados da transcrição globalmente
  window.transcriptionData = data;

  console.log('Dados de transcrição recebidos:', data);

  // Exibe o resultado da transcrição
  const transcriptionResult = document.getElementById('transcription-result');
  if (transcriptionResult) {
    transcriptionResult.textContent = data.text;
  }

  // Verifica se há dados de diarização para mostrar o tab de diálogo
  // Verifica múltiplas fontes de dados de diarização
  const hasSpeakersText = !!data.speakers_text;
  const hasSpeakersSummary = !!(data.transcription_data && data.transcription_data.speakers_summary);
  const hasDiarizationData = !!(data.transcription_data && data.transcription_data.diarization);
  const hasWhisperSegmentsWithSpeakers = data.transcription_data &&
    data.transcription_data.segments &&
    data.transcription_data.segments.some(segment => segment.speaker);

  const hasSpeakers = hasSpeakersText || hasSpeakersSummary || hasDiarizationData || hasWhisperSegmentsWithSpeakers;
  const dialogueTab = document.getElementById('dialogue-tab-btn');

  console.log('🔍 VERIFICAÇÃO DETALHADA DE SPEAKERS:');
  console.log('  - speakers_text exists:', !!data.speakers_text);
  console.log('  - transcription_data exists:', !!data.transcription_data);
  console.log('  - segments exists:', !!(data.transcription_data && data.transcription_data.segments));
  console.log('  - segments count:', data.transcription_data?.segments?.length || 0);
  console.log('  - speakers_summary exists:', !!data.transcription_data?.speakers_summary);
  console.log('  - diarization data exists:', !!data.transcription_data?.diarization);

  if (data.transcription_data?.segments) {
    const segmentsWithSpeaker = data.transcription_data.segments.filter(s => s.speaker);
    console.log('  - whisper segments with speaker:', segmentsWithSpeaker.length);
    console.log('  - first few whisper segments speaker check:',
      data.transcription_data.segments.slice(0, 3).map(s => ({
        hasSpeaker: !!s.speaker,
        speaker: s.speaker
      }))
    );
  }

  if (data.transcription_data?.diarization) {
    console.log('  - diarization segments count:', data.transcription_data.diarization.length);
    console.log('  - first few diarization segments:',
      data.transcription_data.diarization.slice(0, 3).map(s => ({
        speaker: s.speaker,
        duration: s.duration
      }))
    );
  }

  console.log('  - hasSpeakersText:', hasSpeakersText);
  console.log('  - hasSpeakersSummary:', hasSpeakersSummary);
  console.log('  - hasDiarizationData:', hasDiarizationData);
  console.log('  - hasWhisperSegmentsWithSpeakers:', hasWhisperSegmentsWithSpeakers);
  console.log('  - hasSpeakers (final):', hasSpeakers);
  console.log('  - dialogue tab found:', !!dialogueTab);

  if (hasSpeakers && dialogueTab) {
    dialogueTab.style.display = 'inline-block';
    displayDialogueResult(data);
    console.log('✅ Tab de diálogo habilitado');
  } else {
    if (dialogueTab) {
      dialogueTab.style.display = 'none';
      console.log('❌ Tab de diálogo OCULTADO - dados insuficientes');
    } else {
      console.log('❌ Tab de diálogo não encontrado no DOM');
    }
  }

  // Mostra o botão "Nova Transcrição"
  const newSection = document.getElementById('new-section');
  if (newSection) {
    newSection.style.display = 'block';
  }
}

function displayDialogueResult(data) {
  const dialogueResult = document.getElementById('dialogue-result');
  if (!dialogueResult) {
    console.warn('Elemento dialogue-result não encontrado');
    return;
  }

  console.log('Exibindo resultado do diálogo com dados:', data);

  // Verifica se temos dados de diarização (relaxa a verificação)
  if (!data.speakers_text && !data.transcription_data) {
    dialogueResult.innerHTML = '<p>Dados de diarização não disponíveis.</p>';
    return;
  }

  // Processa os dados de diarização
  const dialogueData = parseDialogueData(data);
  if (!dialogueData || dialogueData.length === 0) {
    dialogueResult.innerHTML = '<p>Não foi possível processar os dados de diarização.</p>';
    return;
  }

  console.log('Dados de diálogo processados:', dialogueData);

  // Renderiza as mensagens do diálogo
  renderDialogueMessages(dialogueResult, dialogueData);
}

function parseDialogueData(data) {
  const messages = [];

  try {
    console.log('Parsing dialogue data:', {
      hasTranscriptionData: !!data.transcription_data,
      hasSpeakersText: !!data.speakers_text,
      hasCombinedText: !!(data.transcription_data && data.transcription_data.combined_text),
      hasDiarization: !!(data.transcription_data && data.transcription_data.diarization)
    });

    // PRIORITÁRIO: Usa combined_text se disponível (formato já processado com speakers e timestamps)
    if (data.transcription_data && data.transcription_data.combined_text) {
      console.log('Processando combined_text (formato já processado)');
      const combinedText = data.transcription_data.combined_text;
      const lines = combinedText.split('\n');

      lines.forEach((line, index) => {
        line = line.trim();
        if (line) {
          // Formato: [00:00 - 00:07] SPEAKER_01: texto
          const match = line.match(/^\[(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})\]\s+(SPEAKER_\d+):\s*(.+)$/);
          if (match) {
            const startTime = match[1];
            const endTime = match[2];
            const speaker = match[3];
            const text = match[4].trim();

            if (text) {
              messages.push({
                speaker: speaker,
                text: text,
                start: timeToSeconds(startTime),
                end: timeToSeconds(endTime),
                timestamp: startTime
              });
              console.log(`Linha ${index} processada: ${speaker} -> "${text.substring(0, 30)}..."`);
            }
          }
        }
      });
    }
    // FALLBACK 1: Tenta extrair dados dos segmentos de whisper com speakers se disponível
    else if (data.transcription_data && data.transcription_data.segments) {
      console.log('Processando segmentos de transcrição:', data.transcription_data.segments.length);

      // Debug: vamos ver alguns segmentos de exemplo
      console.log('Primeiros 3 segmentos:', data.transcription_data.segments.slice(0, 3));

      data.transcription_data.segments.forEach((segment, index) => {
        console.log(`Segmento ${index}:`, {
          hasText: !!segment.text,
          hasSpeaker: !!segment.speaker,
          textLength: segment.text ? segment.text.length : 0,
          speaker: segment.speaker,
          text: segment.text ? segment.text.substring(0, 50) + '...' : 'sem texto'
        });

        if (segment.speaker && segment.text && segment.text.trim()) {
          messages.push({
            speaker: segment.speaker,
            text: segment.text.trim(),
            start: segment.start || 0,
            end: segment.end || 0,
            timestamp: formatTime(segment.start || 0)
          });
        }
      });
    }
    // FALLBACK 2: parse do speakers_text básico
    else if (data.speakers_text) {
      console.log('Processando speakers_text como fallback');
      const speakersText = data.speakers_text;
      const lines = speakersText.split('\n');

      lines.forEach(line => {
        line = line.trim();
        if (line) {
          // Formato: SPEAKER_XX: texto
          const match = line.match(/^(SPEAKER_\d+):\s*(.+)$/);
          if (match) {
            const speaker = match[1];
            const text = match[2].trim();

            if (text) {
              messages.push({
                speaker: speaker,
                text: text,
                start: 0,
                end: 0,
                timestamp: '--:--'
              });
            }
          }
        }
      });
    } else {
      console.warn('Nenhum dado de diarização encontrado');
    }

    console.log('Mensagens processadas:', messages.length);
  } catch (error) {
    console.error('Erro ao processar dados de diálogo:', error);
    return [];
  }

  return messages;
}

function renderDialogueMessages(container, messages) {
  console.log('Renderizando mensagens de diálogo:', messages.length);

  let html = '';
  const speakerColors = ['speaker-0', 'speaker-1', 'speaker-2', 'speaker-3', 'speaker-4'];
  const speakerMap = new Map();
  let speakerIndex = 0;

  messages.forEach((message, index) => {
    // Atribui uma cor consistente para cada locutor
    if (!speakerMap.has(message.speaker)) {
      speakerMap.set(message.speaker, speakerColors[speakerIndex % speakerColors.length]);
      speakerIndex++;
    }

    const colorClass = speakerMap.get(message.speaker);
    const speakerLabel = getSpeakerLabel(message.speaker);

    console.log(`Renderizando mensagem ${index + 1}:`, {
      speaker: message.speaker,
      speakerLabel,
      colorClass,
      text: message.text.substring(0, 50) + '...'
    });

    html += `
      <div class="dialogue-message ${colorClass}">
        <div class="message-header">
          <div class="speaker-icon ${colorClass}"></div>
          <span class="speaker-name">${speakerLabel}</span>
          <span class="message-timestamp">${message.timestamp}</span>
        </div>
        <div class="message-text">${escapeHtml(message.text)}</div>
      </div>
    `;
  });

  console.log('HTML gerado para diálogo:', html.length, 'caracteres');
  container.innerHTML = html;

  // Verifica se o HTML foi inserido corretamente
  const insertedMessages = container.querySelectorAll('.dialogue-message');
  console.log('Mensagens inseridas no DOM:', insertedMessages.length);
}

function getSpeakerLabel(speaker) {
  // Converte SPEAKER_00 para "Locutor 1", etc.
  const match = speaker.match(/SPEAKER_(\d+)/);
  if (match) {
    const num = parseInt(match[1]) + 1;
    return `Locutor ${num}`;
  }
  return speaker;
}

function formatTime(seconds) {
  if (!seconds || seconds === 0) return '--:--';

  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Funções auxiliares
function timeToSeconds(timeStr) {
  // Converte formato MM:SS para segundos
  const parts = timeStr.split(':');
  if (parts.length === 2) {
    const minutes = parseInt(parts[0]) || 0;
    const seconds = parseInt(parts[1]) || 0;
    return minutes * 60 + seconds;
  }
  return 0;
}

// Funções de Status e Progress
function showStatus(message, type) {
  // Primeiro tenta usar um elemento de status específico se existir
  let status = document.getElementById('status');

  // Se não encontrar, cria um ou usa o progress-text
  if (!status) {
    status = document.getElementById('progress-text');
  }

  if (status) {
    status.textContent = message;
    // Remove classes anteriores
    status.className = status.className.replace(/\b(success|error|loading|warning)\b/g, '');
    // Adiciona nova classe
    if (type) {
      status.classList.add(type);
    }
  } else {
    // Fallback: exibe no console se não encontrar elementos
    console.log(`Status [${type}]: ${message}`);
  }
}

function showProgress(show) {
  const progressSection = document.getElementById('progress-section');
  const progressBar = document.getElementById('progressBar');

  if (progressSection) {
    if (show) {
      progressSection.style.display = 'block';
    } else {
      progressSection.style.display = 'none';
    }
  }

  if (progressBar) {
    if (show) {
      progressBar.classList.add('show');
    } else {
      progressBar.classList.remove('show');
    }
  }
}

// Funções adicionais de compatibilidade para o novo template
function showTab(tabName) {
  // Remove classe active de todos os botões de tab
  document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

  // Ativa o tab selecionado
  const tabButton = document.querySelector(`[onclick="showTab('${tabName}')"]`);
  const tabContent = document.getElementById(`${tabName}-tab`);

  if (tabButton) {
    tabButton.classList.add('active');
  }

  if (tabContent) {
    tabContent.classList.add('active');
  }
}

function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    const text = element.textContent || element.value;
    navigator.clipboard.writeText(text).then(() => {
      showStatus('Texto copiado para a área de transferência!', 'success');
    }).catch(err => {
      showStatus('Erro ao copiar texto: ' + err, 'error');
    });
  }
}

function downloadText(elementId, filename) {
  const element = document.getElementById(elementId);
  if (element) {
    const text = element.textContent || element.value;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }
}

function copyInsights() {
  copyToClipboard('insights-result');
}

function downloadInsights() {
  downloadText('insights-result', 'insights.txt');
}

function startNew() {
  // Reset da aplicação
  currentTaskId = null;

  // Esconde seções de resultado
  const resultSection = document.getElementById('results-section');
  const newSection = document.getElementById('new-section');
  const fileInfo = document.getElementById('file-info');
  const transcriptionOptions = document.getElementById('transcription-options');
  const progressSection = document.getElementById('progress-section');

  if (resultSection) resultSection.style.display = 'none';
  if (newSection) newSection.style.display = 'none';
  if (fileInfo) fileInfo.style.display = 'none';
  if (transcriptionOptions) transcriptionOptions.style.display = 'none';
  if (progressSection) progressSection.style.display = 'none';

  // Limpa o input de arquivo
  const fileInput = document.getElementById('file-input');
  if (fileInput) {
    fileInput.value = '';
  }

  // Volta para o tab de transcrição
  showTab('transcription');

  showStatus('Pronto para nova transcrição', 'success');
}

// Test function to validate dialogue functionality
function testDialogueView() {
  console.log('🧪 Testing dialogue view functionality...');

  // Simulate test data
  const testData = {
    text: 'Olá, como você está? Estou bem, obrigado.',
    speakers_text: 'SPEAKER_00: Olá, como você está?\nSPEAKER_01: Estou bem, obrigado.',
    transcription_data: {
      segments: [
        {
          speaker: 'SPEAKER_00',
          text: 'Olá, como você está?',
          start: 0.0,
          end: 2.5
        },
        {
          speaker: 'SPEAKER_01',
          text: 'Estou bem, obrigado.',
          start: 2.8,
          end: 5.2
        }
      ]
    }
  };

  console.log('Test data:', testData);

  // Test the dialogue tab button finding
  const dialogueTabBtn = document.getElementById('dialogue-tab-btn');
  console.log('Dialogue tab button found:', !!dialogueTabBtn);

  // Test the dialogue result element
  const dialogueResult = document.getElementById('dialogue-result');
  console.log('Dialogue result element found:', !!dialogueResult);

  // Test data parsing
  const parsedData = parseDialogueData(testData);
  console.log('Parsed dialogue data:', parsedData);

  // Test rendering if elements exist
  if (dialogueResult && parsedData.length > 0) {
    renderDialogueMessages(dialogueResult, parsedData);
    console.log('✅ Dialogue view test completed successfully');
  } else {
    console.log('❌ Dialogue view test failed - missing elements or data');
  }
}