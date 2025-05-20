from tkinter import *
from tkinter import ttk
import generatenew
import phrase

class SeedXORUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SeedXOR Tool")
        self.root.geometry("1200x900")
        self.root.configure(bg="#2E3440")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11), padding=6)
        self.style.configure('TLabel', background="#2E3440", foreground="#D8DEE9", font=('Segoe UI', 14))
        self.style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'), foreground="#88C0D0")
        self.style.configure('Result.TLabel', font=('Segoe UI', 16), foreground="#A3BE8C")

        self.show_home_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        self.clear_screen()

        frame = Frame(self.root, bg="#2E3440")
        frame.pack(expand=True)

        ttk.Label(frame, text="SeedXOR", style='Header.TLabel').pack(pady=30)

        ttk.Button(frame, text="Create Seed Phrases", width=30, command=self.show_create_screen).pack(pady=15)
        ttk.Button(frame, text="Get Seed from Phrases", width=30, command=self.show_get_seed_screen).pack(pady=15)

    def show_create_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Create Seed Phrases", style='Header.TLabel').pack(pady=15)

        seed_frame = Frame(self.root, bg="#2E3440")
        seed_frame.pack(pady=10)
        ttk.Label(seed_frame, text="Enter Seed:", style='TLabel').pack(side=LEFT)
        self.seed_entry = ttk.Entry(seed_frame, width=40)
        self.seed_entry.pack(side=LEFT, padx=10)

        ttk.Button(seed_frame, text="Generate Phrase", command=self.generate_phrase_from_seed).pack(side=LEFT)

        self.phrase_list_frame = Frame(self.root, bg="#3B4252", bd=2, relief=SOLID)
        self.phrase_list_frame.pack(pady=15, fill=X, padx=20)

        self.generated_phrases = []

        ttk.Button(self.root, text="Back", command=self.show_home_screen).pack(pady=15)

    def generate_phrase_from_seed(self):
        seed = self.seed_entry.get()
        if not seed or not seed.isnumeric():
            return
        seed = int(seed)
        phrase1 = phrase.number_to_mnemonic(seed)
        self.generated_phrases.append(phrase1)
        self.update_phrase_list()

    def update_phrase_list(self):
        for widget in self.phrase_list_frame.winfo_children():
            widget.destroy()

        for idx, phrase_text in enumerate(self.generated_phrases):
            frame = Frame(self.phrase_list_frame, bg="#4C566A")
            frame.pack(pady=5, fill="x", padx=5)

            lbl = Label(frame, text=f"Phrase {idx + 1}: {phrase_text}", bg="#4C566A", fg="#D8DEE9",
                        font=("Segoe UI", 12), anchor="w")
            lbl.pack(side=LEFT, padx=10, pady=5, expand=True, fill="x")

            ttk.Button(frame, text="Split", command=lambda i=idx: self.split_phrase(i)).pack(side=RIGHT, padx=5)
            ttk.Button(frame, text="Copy", command=lambda t=phrase_text: self.copy_to_clipboard(t)).pack(side=RIGHT)

    def split_phrase(self, idx):
        original_phrase = self.generated_phrases[idx]
        phrase1, phrase2 = generatenew.create_new_phrase(original_phrase)
        self.generated_phrases[idx:idx+1] = [phrase1, phrase2]
        self.update_phrase_list()

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def show_get_seed_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Enter Phrases to Derive Seed", style='Header.TLabel').pack(pady=15)

        self.phrase_entries = []
        self.phrase_container = Frame(self.root, bg="#3B4252", bd=2, relief=SOLID)
        self.phrase_container.pack(pady=10, fill=X, padx=20)

        self.add_phrase_input()

        btn_frame = Frame(self.root, bg="#2E3440")
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Add Another Phrase", command=self.add_phrase_input).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Get Seed", command=self.get_seed).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Back", command=self.show_home_screen).pack(side=LEFT, padx=10)

        self.result_label = ttk.Label(self.root, text="", style='Result.TLabel')
        self.result_label.pack(pady=10)

    def add_phrase_input(self):
        entry = ttk.Entry(self.phrase_container, width=80)
        entry.pack(pady=5, padx=5)
        self.phrase_entries.append(entry)

    def get_seed(self):
        phrases = [entry.get() for entry in self.phrase_entries]
        try:
            k = generatenew.reconstruct_num(phrases)
        except Exception:
            k = "Invalid Phrase"
        self.result_label.config(text=f"Seed value: {k}")

root = Tk()
app = SeedXORUI(root)
root.mainloop()
