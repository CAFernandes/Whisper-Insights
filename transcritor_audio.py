import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import whisper
import os

# --- Configurações Iniciais ---
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # "blue", "green", "dark-blue"

# Modelo do Whisper a ser usado (outras opções: "tiny", "small", "medium", "large")
# Modelos maiores são mais precisos, mas mais lentos e consomem mais recursos.
# O modelo "base" é um bom equilíbrio para começar.
MODEL_NAME = "base"
loaded_model = None # Variável global para carregar o modelo apenas uma vez

class AudioTranscriberApp(TkinterDnD.Tk): # Herda de TkinterDnD.Tk para DND
    def __init__(self):
        super().__init__()

        self.title("Transcritor de Áudio com Whisper")
        self.geometry("700x550")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.selected_audio_file = None
        self.is_transcribing = False

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Para a caixa de texto expandir

        # Frame para arrastar e soltar / seleção
        self.file_frame = ctk.CTkFrame(self, height=150)
        self.file_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.file_frame.grid_columnconfigure(0, weight=1)
        self.file_frame.grid_rowconfigure(0, weight=1)

        # Habilitar Drag and Drop para o file_frame
        self.file_frame.drop_target_register(DND_FILES)
        self.file_frame.dnd_bind('<<Drop>>', self.handle_drop)

        self.drop_label = ctk.CTkLabel(self.file_frame,
                                       text="Arraste e solte o arquivo de áudio aqui\nou clique no botão abaixo para selecionar",
                                       font=ctk.CTkFont(size=14))
        self.drop_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.select_button = ctk.CTkButton(self, text="Selecionar Arquivo de Áudio", command=self.select_file)
        self.select_button.grid(row=1, column=0, padx=20, pady=(0,10), sticky="ew")

        self.selected_file_label = ctk.CTkLabel(self, text="Nenhum arquivo selecionado", text_color="gray", wraplength=650)
        self.selected_file_label.grid(row=2, column=0, padx=20, pady=(0,10), sticky="w")

        self.transcribe_button = ctk.CTkButton(self, text="Transcrever Áudio", command=self.start_transcription_thread)
        self.transcribe_button.grid(row=3, column=0, padx=20, pady=(5,10), sticky="ew")
        self.transcribe_button.configure(state="disabled")

        self.result_textbox = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=13))
        self.result_textbox.grid(row=4, column=0, padx=20, pady=(0,10), sticky="nsew")
        self.result_textbox.insert("0.0", "O texto transcrito aparecerá aqui...")
        self.result_textbox.configure(state="disabled") # Começa desabilitado para edição

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=5, column=0, padx=20, pady=(0,10), sticky="w")

        self.load_whisper_model()

    def load_whisper_model(self):
        global loaded_model
        if loaded_model is None:
            self.status_label.configure(text=f"Carregando modelo '{MODEL_NAME}' do Whisper... (pode levar tempo na primeira vez)")
            self.update_idletasks() # Força a atualização da UI
            try:
                loaded_model = whisper.load_model(MODEL_NAME)
                self.status_label.configure(text=f"Modelo '{MODEL_NAME}' carregado.")
            except Exception as e:
                self.status_label.configure(text=f"Erro ao carregar modelo: {e}", text_color="red")
                messagebox.showerror("Erro de Modelo", f"Não foi possível carregar o modelo Whisper '{MODEL_NAME}'. Verifique sua instalação ou conexão.\nDetalhes: {e}")
                self.transcribe_button.configure(state="disabled")
        else:
            self.status_label.configure(text=f"Modelo '{MODEL_NAME}' já está carregado.")


    def handle_drop(self, event):
        # event.data é uma string com os caminhos dos arquivos, separados por espaços e entre chaves
        # Ex: '{/caminho/para/arquivo1.mp3} {/caminho/para/arquivo2.wav}'
        # Precisamos limpar isso.
        files_str = event.data.strip('{}')

        # Se múltiplos arquivos forem soltos, pegamos apenas o primeiro
        # Arquivos com espaços nos nomes podem vir como múltiplos itens se não tratados corretamente
        # Tentativa de lidar com nomes de arquivos com espaços (pode não ser perfeito para todos os casos extremos)
        if '\} \{' in files_str: # Múltiplos arquivos distintos
            file_path = files_str.split('\} \{')[0]
        else: # Um único arquivo, possivelmente com espaços
            file_path = files_str

        if os.path.isfile(file_path):
            self.update_selected_file(file_path)
        else:
            self.status_label.configure(text="Item solto não é um arquivo válido.", text_color="orange")

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo de áudio",
            filetypes=(("Arquivos de Áudio", "*.mp3 *.wav *.m4a *.ogg *.flac"),
                       ("Todos os arquivos", "*.*"))
        )
        if file_path:
            self.update_selected_file(file_path)

    def update_selected_file(self, file_path):
        self.selected_audio_file = file_path
        # Mostra apenas o nome do arquivo para não poluir a interface
        filename = os.path.basename(file_path)
        self.selected_file_label.configure(text=f"Arquivo: {filename}", text_color="white")
        self.transcribe_button.configure(state="normal" if loaded_model else "disabled")
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", "Pronto para transcrever...")
        self.result_textbox.configure(state="disabled")
        self.status_label.configure(text="")


    def start_transcription_thread(self):
        if not self.selected_audio_file:
            messagebox.showwarning("Nenhum Arquivo", "Por favor, selecione um arquivo de áudio primeiro.")
            return
        if self.is_transcribing:
            messagebox.showinfo("Em Progresso", "A transcrição já está em andamento.")
            return
        if not loaded_model:
            messagebox.showerror("Modelo Não Carregado", "O modelo Whisper não pôde ser carregado. Verifique o status.")
            self.load_whisper_model() # Tenta carregar novamente
            if not loaded_model: return # Se ainda não carregou, sai

        self.is_transcribing = True
        self.transcribe_button.configure(state="disabled")
        self.select_button.configure(state="disabled")
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", "Transcrevendo, por favor aguarde...\nIsso pode levar alguns minutos dependendo do tamanho do áudio e do modelo.")
        self.result_textbox.configure(state="disabled")
        self.status_label.configure(text="Processando...")

        # Executa a transcrição em uma thread separada para não bloquear a UI
        thread = threading.Thread(target=self.transcribe_audio_task)
        thread.daemon = True # Permite que a thread feche se o app fechar
        thread.start()

    def transcribe_audio_task(self):
        global loaded_model
        try:
            if not loaded_model:
                # Isso não deveria acontecer se o botão está habilitado, mas é uma checagem extra
                raise Exception("Modelo Whisper não carregado.")

            # Para verificar se o arquivo ainda existe (pouco provável, mas bom ter)
            if not os.path.exists(self.selected_audio_file):
                raise FileNotFoundError("Arquivo de áudio não encontrado no caminho especificado.")

            result = loaded_model.transcribe(self.selected_audio_file, fp16=False) # fp16=False para maior compatibilidade
            transcribed_text = result["text"]

            # Atualiza a UI na thread principal
            self.after(0, self.update_ui_with_result, transcribed_text, None)

        except FileNotFoundError as fnf_err:
            self.after(0, self.update_ui_with_result, None, f"Erro: Arquivo não encontrado. {fnf_err}")
        except Exception as e:
            error_message = f"Ocorreu um erro durante a transcrição: {e}\n"
            if "ffmpeg" in str(e).lower():
                error_message += "Verifique se o ffmpeg está instalado e no PATH do sistema.\n"
            self.after(0, self.update_ui_with_result, None, error_message)
        finally:
            self.is_transcribing = False
            # Reabilita botões na thread principal
            self.after(0, self.finalize_transcription_ui)


    def update_ui_with_result(self, text, error_message):
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        if error_message:
            self.result_textbox.insert("0.0", error_message)
            self.status_label.configure(text="Erro na transcrição.", text_color="red")
        else:
            self.result_textbox.insert("0.0", text)
            self.status_label.configure(text="Transcrição Concluída!", text_color="green")
        self.result_textbox.configure(state="disabled")


    def finalize_transcription_ui(self):
        self.transcribe_button.configure(state="normal" if self.selected_audio_file and loaded_model else "disabled")
        self.select_button.configure(state="normal")


    def on_closing(self):
        if self.is_transcribing:
            if messagebox.askyesno("Sair?", "A transcrição está em andamento. Deseja realmente sair?"):
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    # Verifica se o ffmpeg está acessível (verificação básica)
    if os.system("ffmpeg -version > nul 2>&1" if os.name == 'nt' else "ffmpeg -version > /dev/null 2>&1") != 0:
         print("AVISO: ffmpeg não encontrado no PATH do sistema. A transcrição pode falhar.")
         print("Por favor, instale o ffmpeg e adicione-o ao PATH.")
         # Você pode optar por não iniciar o app se o ffmpeg não for encontrado,
         # ou apenas mostrar o aviso e tentar prosseguir.
         # messagebox.showwarning("ffmpeg não encontrado", "O ffmpeg não foi encontrado no PATH do sistema. A transcrição pode falhar. Por favor, instale-o.")


    app = AudioTranscriberApp()
    app.mainloop()