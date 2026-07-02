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
        self.root.title("Smart Braille Slate - Full Grid")
        self.root.geometry("850x850")

        self.num_rows = 4
        self.num_cols = 5
        self.total_cells = self.num_rows * self.num_cols

        # State for 20 cells, each containing 6 dots
        self.cells_data = [[0] * 6 for _ in range(self.total_cells)]
        self.cell_buttons = [[] for _ in range(self.total_cells)]

        # Initialize Engines
        self.translator = Translator()
        self.engine = pyttsx3.init()
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)

        self.create_ui()

    def create_ui(self):
        # 1. Container for the grid
        grid_container = tk.Frame(self.root)
        grid_container.pack(pady=20)

        grid_mapping = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1)]

        # Generate the 20 Braille cells
        for cell_idx in range(self.total_cells):
            r = cell_idx // self.num_cols
            c = cell_idx % self.num_cols

            # Frame with a border for a single 6-dot cell
            cell_frame = tk.Frame(grid_container, bd=1, relief=tk.SOLID)
            cell_frame.grid(row=r, column=c, padx=8, pady=8)

            for dot_idx in range(6):
                dr, dc = grid_mapping[dot_idx]
                btn = tk.Button(cell_frame, width=3, height=1, bg="lightgray",
                                command=lambda ci=cell_idx, di=dot_idx: self.toggle_dot(ci, di))
                btn.grid(row=dr, column=dc, padx=2, pady=2)
                self.cell_buttons[cell_idx].append(btn)

        # 2. Document Display Area
        self.document_text = tk.Text(self.root, height=4, width=65, font=("Arial", 14))
        self.document_text.pack(pady=10)
        self.document_text.config(state=tk.DISABLED)

        # 3. Clear Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        clear_btn = tk.Button(control_frame, text="Clear Grid", width=15, command=self.clear_grid)
        clear_btn.pack()

        # 4. Translation and Audio Engine UI
        engine_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        engine_frame.pack(pady=15, padx=20, fill="x")
        
        engine_title = tk.Label(engine_frame, text="Translation & Audio Engine", font=("Arial", 12, "bold"))
        engine_title.pack(pady=5)

        self.lang_var = tk.StringVar(self.root)
        self.lang_var.set("English (en)") 
        languages = ["English (en)", "Hindi (hi)", "Tamil (ta)"]
        
        lang_menu = tk.OptionMenu(engine_frame, self.lang_var, *languages)
        lang_menu.pack(pady=5)

        self.translated_text_label = tk.Label(engine_frame, text="", font=("Arial", 14), fg="green", wraplength=700)
        self.translated_text_label.pack(pady=10)

        speak_btn = tk.Button(engine_frame, text="Translate & Speak", width=20, bg="lightgreen", command=self.translate_and_speak)
        speak_btn.pack(pady=10)

    def toggle_dot(self, cell_idx, dot_idx):
        # Toggle state
        current_state = self.cells_data[cell_idx][dot_idx]
        self.cells_data[cell_idx][dot_idx] = 1 if current_state == 0 else 0
        
        # Update specific button color
        btn = self.cell_buttons[cell_idx][dot_idx]
        if self.cells_data[cell_idx][dot_idx] == 1:
            btn.config(bg="lightblue")
        else:
            btn.config(bg="lightgray")
            
        self.update_document()

    def update_document(self):
        parsed_text = ""
        for cell in self.cells_data:
            bitmask_str = "".join(map(str, cell))
            character = BRAILLE_MAP.get(bitmask_str, "?")
            # Blank cell translates to a space
            if bitmask_str == "000000":
                parsed_text += " "
            else:
                parsed_text += character
        
        # Remove empty trailing spaces for cleaner output processing
        final_text = parsed_text.rstrip()

        self.document_text.config(state=tk.NORMAL)
        self.document_text.delete(1.0, tk.END)
        self.document_text.insert(tk.END, final_text)
        self.document_text.config(state=tk.DISABLED)

    def clear_grid(self):
        # Reset data arrays and button colors
        self.cells_data = [[0] * 6 for _ in range(self.total_cells)]
        for cell_idx in range(self.total_cells):
            for dot_idx in range(6):
                self.cell_buttons[cell_idx][dot_idx].config(bg="lightgray")
        
        self.translated_text_label.config(text="")
        self.update_document()

    def translate_and_speak(self):
        current_text = self.document_text.get(1.0, tk.END).strip()
        if not current_text:
            return

        selected_lang = self.lang_var.get()
        target_code = "en"
        
        if "hi" in selected_lang:
            target_code = "hi"
        elif "ta" in selected_lang:
            target_code = "ta"

        try:
            if target_code != "en":
                translated = self.translator.translate(current_text, dest=target_code)
                final_text = translated.text
            else:
                final_text = current_text
            
            self.translated_text_label.config(text=f"Translation: {final_text}")
            
            self.engine.say(final_text)
            self.engine.runAndWait()
            
        except Exception as e:
            self.translated_text_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BrailleEmulator(root)
    root.mainloop()