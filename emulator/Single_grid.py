import tkinter as tk
import pyttsx3
from googletrans import Translator

# Complete Braille to English Alphabet Mapping
BRAILLE_MAP = {
    "100000": "A", "110000": "B", "100100": "C", "100110": "D", "100010": "E",
    "110100": "F", "110110": "G", "110010": "H", "010100": "I", "010110": "J",
    "101000": "K", "111000": "L", "101100": "M", "101110": "N", "101010": "O",
    "111100": "P", "111110": "Q", "111010": "R", "011100": "S", "011110": "T",
    "101001": "U", "111001": "V", "010111": "W", "101101": "X", "101111": "Y",
    "101011": "Z", "000000": " "
}

class BrailleEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Braille Slate Emulator")
        self.root.geometry("500x750")

        self.dots = [0] * 6
        self.buttons = []
        self.current_text = ""

        # Initialize Translation and Audio Engines
        self.translator = Translator()
        self.engine = pyttsx3.init()
        
        # Adjust speech rate to be slightly slower and clearer
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)

        self.create_ui()

    def create_ui(self):
        # 1. The Braille Cell Input Area
        cell_frame = tk.Frame(self.root)
        cell_frame.pack(pady=15)

        grid_mapping = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1)]

        for i in range(6):
            row, col = grid_mapping[i]
            btn = tk.Button(cell_frame, text=f"Dot {i+1}", width=8, height=3,
                            bg="lightgray", command=lambda idx=i: self.toggle_dot(idx))
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons.append(btn)

        # 2. Live Character Translation Labels
        self.output_label = tk.Label(self.root, text="Bitmask: 000000", font=("Arial", 12))
        self.output_label.pack(pady=2)
        
        self.translation_label = tk.Label(self.root, text="Character:  ", font=("Arial", 16, "bold"), fg="blue")
        self.translation_label.pack(pady=5)

        # 3. Control Buttons for Navigation
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        save_btn = tk.Button(control_frame, text="Next Cell", width=12, command=self.save_character)
        save_btn.grid(row=0, column=0, padx=5)

        space_btn = tk.Button(control_frame, text="Space", width=10, command=self.add_space)
        space_btn.grid(row=0, column=1, padx=5)

        clear_btn = tk.Button(control_frame, text="Clear Page", width=10, command=self.clear_page)
        clear_btn.grid(row=0, column=2, padx=5)

        # 4. Document Display Area
        self.document_text = tk.Text(self.root, height=4, width=45, font=("Arial", 14))
        self.document_text.pack(pady=10)
        self.document_text.config(state=tk.DISABLED)

        # 5. Translation and Audio Engine UI
        engine_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        engine_frame.pack(pady=15, padx=20, fill="x")
        
        engine_title = tk.Label(engine_frame, text="Translation & Audio Engine", font=("Arial", 12, "bold"))
        engine_title.pack(pady=5)

        # Language Selection Dropdown
        self.lang_var = tk.StringVar(self.root)
        self.lang_var.set("English (en)") 
        languages = ["English (en)", "Hindi (hi)", "Tamil (ta)"]
        
        lang_menu = tk.OptionMenu(engine_frame, self.lang_var, *languages)
        lang_menu.pack(pady=5)

        # Output Translated Text Label
        self.translated_text_label = tk.Label(engine_frame, text="", font=("Arial", 14), fg="green", wraplength=400)
        self.translated_text_label.pack(pady=10)

        speak_btn = tk.Button(engine_frame, text="Translate & Speak", width=20, bg="lightgreen", command=self.translate_and_speak)
        speak_btn.pack(pady=10)

    def toggle_dot(self, index):
        self.dots[index] = 1 if self.dots[index] == 0 else 0
        self.update_buttons()
        self.update_output()

    def update_buttons(self):
        for i in range(6):
            if self.dots[i] == 1:
                self.buttons[i].config(bg="lightblue")
            else:
                self.buttons[i].config(bg="lightgray")

    def update_output(self):
        bitmask_str = "".join(map(str, self.dots))
        self.output_label.config(text=f"Bitmask: {bitmask_str}")
        character = BRAILLE_MAP.get(bitmask_str, "?")
        self.translation_label.config(text=f"Character: {character}")

    def save_character(self):
        bitmask_str = "".join(map(str, self.dots))
        character = BRAILLE_MAP.get(bitmask_str, "?")
        if character != "?":
            self.current_text += character
            self.update_document_view()
        self.reset_cell()

    def add_space(self):
        self.current_text += " "
        self.update_document_view()
        self.reset_cell()

    def clear_page(self):
        self.current_text = ""
        self.update_document_view()
        self.translated_text_label.config(text="")
        self.reset_cell()

    def reset_cell(self):
        self.dots = [0] * 6
        self.update_buttons()
        self.update_output()

    def update_document_view(self):
        self.document_text.config(state=tk.NORMAL)
        self.document_text.delete(1.0, tk.END)
        self.document_text.insert(tk.END, self.current_text)
        self.document_text.config(state=tk.DISABLED)

    def translate_and_speak(self):
        # Prevent engine from crashing if there is no text
        if not self.current_text.strip():
            return

        selected_lang = self.lang_var.get()
        target_code = "en"
        
        if "hi" in selected_lang:
            target_code = "hi"
        elif "ta" in selected_lang:
            target_code = "ta"

        try:
            # 1. Translate the text
            if target_code != "en":
                translated = self.translator.translate(self.current_text, dest=target_code)
                final_text = translated.text
            else:
                final_text = self.current_text
            
            # Display the translated text
            self.translated_text_label.config(text=f"Translation: {final_text}")
            
            # 2. Speak the text aloud
            self.engine.say(final_text)
            self.engine.runAndWait()
            
        except Exception as e:
            self.translated_text_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BrailleEmulator(root)
    root.mainloop()