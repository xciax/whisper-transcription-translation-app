from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import customtkinter as ctk
import threading
import whisper
import pyaudio
import tempfile
import wave

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.recorder = Recorder()
        self.main_window()
        self.file_path = None
        self.dictLang = {'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Azerbaijani': 'az', 'Bashkir': 'ba', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs', 'Breton': 'br', 'Bulgarian': 'bg', 'Burmese': 'my', 'Castilian': 'es', 'Catalan': 'ca', 'Chinese': 'zh', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Estonian': 'et', 'Faroese': 'fo', 'Finnish': 'fi', 'Flemish': 'nl', 'French': 'fr', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu', 'Haitian': 'ht', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'he', 'Hindi': 'hi', 'Hungarian': 'hu', 'Icelandic': 'is', 'Indonesian': 'id', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Letzeburgesch': 'lb', 'Lingala': 'ln', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Moldavian': 'mo', 'Moldovan': 'mo', 'Mongolian': 'mn', 'Myanmar': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Nynorsk': 'nn', 'Occitan': 'oc', 'Panjabi': 'pa', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Pushto': 'ps', 'Romanian': 'ro', 'Russian': 'ru','Sindhi': 'sd','Sinhala': 'si', 'Sinhalese': 'si','Slovak': 'sk','Slovenian': 'sl','Somali': 'so','Spanish': 'es','Sundanese': 'su','Swahili': 'sw','Swedish': 'sv','Tagalog': 'tl','Tajik': 'tg','Tamil': 'ta','Tatar': 'tt','Telugu': 'te','Thai': 'th','Tibetan': 'bo','Turkish': 'tr','Turkmen': 'tk','Ukrainian': 'uk','Urdu': 'ur','Uzbek': 'uz','Valencian': 'ca','Vietnamese': 'vi','Welsh': 'cy','Yiddish': 'yi','Yoruba': 'yo','Zulu': 'zu'}
        self.dictModels = {"Tiny (~1GB)":"tiny", "Base (~1GB)":"base", "Small (~2GB)":"small", "Medium (~5GB)":"medium", "Large (~10GB)":"large"}


    def main_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.title("Audio Translation & Transcriber")
        self.geometry("1100x580")
        self.minsize(1100,580)
        self.maxsize(1100,580)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(12, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Options", font=("", 28, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.model_label = ctk.CTkLabel(self.sidebar_frame, text="Model: (VRAM required)")
        self.model_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.model_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Tiny (~1GB)", "Base (~1GB)", "Small (~2GB)", "Medium (~5GB)", "Large (~10GB)"])
        self.model_option.grid(row=2, column=0, padx=20, pady=0)

        self.from_lang_label = ctk.CTkLabel(self.sidebar_frame, text="From Language:")
        self.from_lang_label.grid(row=3, column=0, padx=20, pady=(5, 0))
        self.language_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani", "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian", "Breton", "Bulgarian", "Burmese", "Castilian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Faroese", "Finnish", "Flemish", "French", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin", "Latvian", "Letzeburgesch", "Lingala", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Moldavian", "Moldovan", "Mongolian", "Myanmar", "Nepali", "Norwegian", "Nynorsk", "Occitan", "Panjabi", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Pushto", "Romanian", "Russian", "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Sinhalese", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uzbek", "Valencian", "Vietnamese", "Welsh", "Yiddish", "Yoruba"])
        self.language_option.grid(row=4, column=0, padx=20, pady=0)

        self.task_label = ctk.CTkLabel(self.sidebar_frame, text="Task:")
        self.task_label.grid(row=5, column=0, padx=20, pady=(5, 0))
        self.task_option = ctk.CTkOptionMenu(self.sidebar_frame, values=["transcribe", "translate"])
        self.task_option.grid(row=6, column=0, padx=20, pady=0)

        self.to_lang_label = ctk.CTkLabel(self.sidebar_frame, text="To Language:")
        self.to_lang_label.grid(row=7, column=0, padx=20, pady=(5, 0))
        self.language_option_to = ctk.CTkOptionMenu(self.sidebar_frame, values=["None", "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani", "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian", "Breton", "Bulgarian", "Burmese", "Castilian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Faroese", "Finnish", "Flemish", "French", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin", "Latvian", "Letzeburgesch", "Lingala", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Moldavian", "Moldovan", "Mongolian", "Myanmar", "Nepali", "Norwegian", "Nynorsk", "Occitan", "Panjabi", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Pushto", "Romanian", "Russian", "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Sinhalese", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uzbek", "Valencian", "Vietnamese", "Welsh", "Yiddish", "Yoruba"])
        self.language_option_to.grid(row=8, column=0, padx=20, pady=0)

        self.open_file_button = ctk.CTkButton(self.sidebar_frame, text="Choose only an\nAudio File", command=self.open_file, font=("", 12, "bold"))
        self.open_file_button.grid(row=9, column=0, padx=20, pady=(50,5))

        self.record_button = ctk.CTkButton(self.sidebar_frame, text="Record", command=self.run_recording, font=("", 12, "bold"))
        self.record_button.grid(row=10, column=0, padx=20, pady=(5, 50))

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:")
        self.appearance_mode_label.grid(row=11, column=0, padx=20, pady=(20,0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=12, column=0, padx=20, pady=(0, 20))
        self.appearance_mode_optionemenu.set("System")

        self.textbox = ctk.CTkTextbox(self, width=250, wrap="word")
        self.textbox.grid(row=0, column=1, rowspan=2, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.textbox.insert("0.0", "Ouput:\n\n")
        self.textbox.configure(state="disabled")

        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.grid(row=2, column=1, padx=0, pady=0)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.run_task, font=("", 14, "bold"), width=256)
        self.start_button.grid(row=3, column=1, padx=20, pady=20)
        self.start_button.configure(state="disabled")

        self.export_button = ctk.CTkButton(self, text="Save Text", command=self.export_text, font=("", 14, "bold"), width=256)
        self.export_button.grid(row=3, column=2, padx=20, pady=20)

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def export_text(self):
        text = self.textbox.get("0.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile="output.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        messagebox.showinfo("Export Successful", f"The file has been saved to {file_path}")

    def close_app(self):
        self.destroy()
        self.quit()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.start_button.configure(state="normal")
            self.message_label.configure(text=f"Selected File: {file_path}")
            self.file_path = file_path
        else:
            self.start_button.configure(state="disabled")
            self.message_label.configure(text="Note: No File Selected, Click (Choose File) Button to Select a File.")

    def run_transcribe(self):
        model_type = self.model_option.get()
        path = self.file_path
        language = self.language_option.get()
        lang_to = self.language_option_to.get()
        task = self.task_option.get()
        self.message_label.configure(text=f"Task Started, Please Wait...\nModel: {model_type}\nLanguage: {language}\nTask: {task}\nLanguage to Translate to: {lang_to}")

        model = whisper.load_model(self.dictModels[model_type])

        self.model_option.configure(state="disabled")
        self.language_option.configure(state="disabled")
        self.task_option.configure(state="disabled")
        self.language_option_to.configure(state="disabled")
        self.open_file_button.configure(state="disabled")
        self.record_button.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.export_button.configure(state="disabled")
        self.textbox.configure(state="normal")

        if task == "transcribe" and lang_to == "None":
            result_text = self.audio_chuncking(path, model, task, language)
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", result_text)
        elif task == "translate" and lang_to != "None":
            if lang_to == "English":
                result_text = self.audio_chuncking(path, model, task, language)
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", result_text)
            elif lang_to == language:
                result_text = self.audio_chuncking(path, model, "transcribe", language)
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", result_text)
            else: 
                result_text = self.audio_chuncking(path, model, task, language)
                tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-" + self.dictLang[lang_to])
                modelT = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-" + self.dictLang[lang_to])
                translator = pipeline("translation",model=modelT, tokenizer=tokenizer)
                res = translator(result_text)
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", res[0]["translation_text"])
        else:
            error_message = "Please select a valid task and language combination."
            self.message_label.configure(text=error_message)
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", "Output:\n\n")
            self.textbox.configure(state="disabled")
            self.model_option.configure(state="normal")
            self.language_option.configure(state="normal")
            self.task_option.configure(state="normal")
            self.language_option_to.configure(state="normal")
            self.open_file_button.configure(state="normal")
            self.record_button.configure(state="normal")
            self.start_button.configure(state="disabled")            
            self.export_button.configure(state="disabled")
            return
        
        self.textbox.configure(state="disabled")
        self.model_option.configure(state="normal")
        self.language_option.configure(state="normal")
        self.task_option.configure(state="normal")
        self.language_option_to.configure(state="normal")
        self.open_file_button.configure(state="normal")
        self.record_button.configure(state="normal")
        self.start_button.configure(state="disabled")
        self.export_button.configure(state="normal")
        self.message_label.configure(text="Task Completed.")

    def audio_chuncking(self, path, model, task, language):
        audio_file = AudioSegment.from_file(path)
        segment_duration = 30000
        segments = [audio_file[start:start+segment_duration] for start in range(0, len(audio_file), segment_duration)]
        transcriptions = ""

        with tempfile.TemporaryDirectory() as temp_dir:
            for i, segment in enumerate(segments):
                temp_path = f"{temp_dir}/segment_{i}.wav"
                segment.export(temp_path, format="wav")
                audio = whisper.load_audio(temp_path)
                audio = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio).to(model.device)
                options = whisper.DecodingOptions(task=task, language=language, fp16=False)
                result = whisper.decode(model, mel, options)
                transcriptions = transcriptions + " " + result.text
        return transcriptions

    def run_task(self):
        try:
            threading.Thread(target=self.run_transcribe).start()
        except Exception:
            error_message = "An error has occurred:\nThe program encountered an unexpected error and was unable to complete the requested action.\nPlease try again."
            self.message_label.configure(text=error_message)

    def run_recording(self):
        try: 
            if not self.recorder.is_recording:
                self.record_button.configure(text="Stop Recording")
                threading.Thread(target=self.recorder.start_recording).start()
            else:
                self.record_button.configure(text="Record")
                self.recorder.is_recording = False
        except Exception:
            error_message = "An error has occurred:\nThe program encountered an unexpected error and was unable to complete the requested action.\nPlease try again."
            self.message_label.configure(text=error_message)

class Recorder():
    def __init__(self):
        self.frames = []
        self.is_recording = False
        self.stream = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

    def start_recording(self):
        app.message_label.configure(text="Recording...")
        app.model_option.configure(state="disabled")
        app.language_option.configure(state="disabled")
        app.task_option.configure(state="disabled")
        app.language_option_to.configure(state="disabled")
        app.open_file_button.configure(state="disabled")
        app.export_button.configure(state="disabled")

        model_type = app.model_option.get()
        language = app.language_option.get()
        lang_to = app.language_option_to.get()
        task = app.task_option.get()

        self.is_recording = not self.is_recording
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)

        while self.is_recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        app.message_label.configure(text=f"Task Started, Please Wait...\nModel: {model_type}\nLanguage: {language}\nTask: {task}\nLanguage to Translate to: {lang_to}")

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        wf = wave.open("output.wav", "wb")
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b"".join(self.frames))
        wf.close()

        model = whisper.load_model(app.dictModels[model_type])
        path = "output.wav"
        
        app.textbox.configure(state="normal")
        
        if task == "transcribe" and lang_to == "None":
            result_text = app.audio_chuncking(path, model, task, language)
            app.textbox.delete("0.0", "end")
            app.textbox.insert("0.0", result_text)
        elif task == "translate" and lang_to != "None":
            if lang_to == "English":
                result_text = app.audio_chuncking(path, model, task, language)
                app.textbox.delete("0.0", "end")
                app.textbox.insert("0.0", result_text)
            elif lang_to == language:
                result_text = app.audio_chuncking(path, model, "transcribe", language)
                app.textbox.delete("0.0", "end")
                app.textbox.insert("0.0", result_text)
            else: 
                tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-" + app.dictLang[lang_to])
                modelT = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-" + app.dictLang[lang_to])
                translator = pipeline("translation",model=modelT, tokenizer=tokenizer)
                res = translator(result_text)
                app.textbox.delete("0.0", "end")
                app.textbox.insert("0.0", res[0]["translation_text"])
        else:
            error_message = "Please select a valid task and language combination."
            app.message_label.configure(text=error_message)
            app.textbox.delete("0.0", "end")
            app.textbox.insert("0.0", "Output:\n\n")
            app.textbox.configure(state="disabled")
            app.model_option.configure(state="normal")
            app.language_option.configure(state="normal")
            app.task_option.configure(state="normal")
            app.language_option_to.configure(state="normal")
            app.open_file_button.configure(state="normal")
            return
        
        app.textbox.configure(state="disabled")

        app.model_option.configure(state="normal")
        app.language_option.configure(state="normal")
        app.task_option.configure(state="normal")
        app.language_option_to.configure(state="normal")
        app.open_file_button.configure(state="normal")
        app.export_button.configure(state="normal")
        app.message_label.configure(text="Task Completed.")

if __name__ == "__main__":
    app = App()
    app.mainloop()