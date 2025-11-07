import tkinter as tk
import pyttsx3
import importlib.util
import os
from tkinter import messagebox, filedialog
from datetime import datetime
import string

# START DRAG-DROP SUPPORT (IF AVAILABLE)
try:
    import tkinterdnd2 as tkdnd
    HAS_DND = True
except ImportError:
    HAS_DND = False

# Speech engine setup
_speech_engine = pyttsx3.init()

def speak(text):
    _speech_engine.say(text)
    _speech_engine.runAndWait()

# ----------- BASIC CIPHER ENGINES (as before) --------
def caesar_cipher(text, key, alphabet=None, encode=True):
    if alphabet is None:
        alphabet = string.ascii_lowercase
    result = []
    key %= len(alphabet)
    letter_map = {c: i for i, c in enumerate(alphabet)}
    for c in text:
        low = c.lower()
        if low in letter_map:
            orig_idx = letter_map[low]
            shift = key if encode else -key
            new_idx = (orig_idx + shift) % len(alphabet)
            rep = alphabet[new_idx]
            if c.isupper():
                rep = rep.upper()
            result.append(rep)
        else:
            result.append(c)
    return ''.join(result)

def atbash_cipher(text, alphabet=None):
    if alphabet is None:
        alphabet = string.ascii_lowercase
    result = []
    indices = {c: i for i, c in enumerate(alphabet)}
    la = len(alphabet)
    for c in text:
        low = c.lower()
        if low in indices:
            new_c = alphabet[la - 1 - indices[low]]
            if c.isupper():
                new_c = new_c.upper()
            result.append(new_c)
        else:
            result.append(c)
    return ''.join(result)

def vigenere_cipher(text, keyword, alphabet=None, encode=True):
    if alphabet is None:
        alphabet = string.ascii_lowercase
    result = []
    alpha_set = set(alphabet)
    key_len = len(keyword)
    letter_map = {c: i for i, c in enumerate(alphabet)}
    key_indices = [letter_map[c.lower()] for c in keyword.lower() if c.lower() in alpha_set]
    key_index = 0
    for c in text:
        low = c.lower()
        if low in alpha_set and key_indices:
            shift = key_indices[key_index % len(key_indices)]
            shift = shift if encode else -shift
            orig_idx = letter_map[low]
            new_idx = (orig_idx + shift) % len(alphabet)
            rep = alphabet[new_idx]
            if c.isupper():
                rep = rep.upper()
            result.append(rep)
            key_index += 1
        else:
            result.append(c)
    return ''.join(result)

# ----------- PLUGIN SYSTEM -----------
def load_plugins():
    ciphers = []
    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
    for fname in os.listdir(plugin_dir):
        if fname.endswith('.py'):
            plugin_path = os.path.join(plugin_dir, fname)
            spec = importlib.util.spec_from_file_location(fname[:-3], plugin_path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                cipher_name = getattr(mod, "CIPHER_NAME", fname[:-3].capitalize())
                encode_fun = getattr(mod, "encode", None)
                decode_fun = getattr(mod, "decode", None)
                if callable(encode_fun) and callable(decode_fun):
                    ciphers.append((cipher_name, encode_fun, decode_fun))
            except Exception as e:
                print(f"Failed loading plugin {fname}: {e}")
    return ciphers

class CipherSuiteProApp:
    def __init__(self, root):
        self.root = root
        self.theme = 0
        self.favorites = []
        self.plugin_ciphers = load_plugins()
        self.root.title("🔐 Cipher Suite Ultra Pro X")
        self.font_label = ("Helvetica",13)
        self.font_btn = ("Helvetica",13,"bold")

        self.title_label = tk.Label(root, text="Cipher Suite Ultra Pro X", font=("Comic Sans MS",17,"bold"), bg="#ededed", fg="#2d4356")
        self.title_label.grid(row=0, column=0, columnspan=8, pady=12)

        self.theme_btn = tk.Button(root, text="Switch Theme 🌓", command=self.switch_theme, font=("Helvetica",11,"bold"), bg="#ecc5fb")
        self.theme_btn.grid(row=0, column=7, sticky="e", padx=8)
        self.text_entry = tk.Entry(root, width=32, font=self.font_label, bg="#EEE")
        self.text_entry.grid(row=1, column=1, columnspan=6, padx=5, sticky="w")
        self.text_entry.bind("<KeyRelease>", lambda e: self.live_preview())
        tk.Label(root, text="Text:", font=self.font_label, bg="#ededed", fg="#2d4356").grid(row=1, column=0, sticky="e", pady=4)

        # Drag/drop
        if HAS_DND:
            self.dnd = tk.Label(root, text="⬇️ Drag a .txt file here to load", bg="#f6eac2", fg="#444", font=self.font_btn, relief='ridge', width=34)
            self.dnd.grid(row=2, column=1, columnspan=6, padx=5, pady=2)
            self.dnd.drop_target_register(tkdnd.DND_FILES)
            self.dnd.dnd_bind('<<Drop>>', self.file_drop)
        else:
            self.dnd = tk.Button(root, text="Clipboard Paste", command=self.paste_clip, bg="#ffedc2", font=self.font_btn)
            self.dnd.grid(row=2, column=1, columnspan=6, padx=5, pady=2)

        # Cipher selection, including plugins!
        tk.Label(root, text="Cipher:", font=self.font_label, bg="#ededed", fg="#2d4356").grid(row=3, column=0, sticky="e", pady=4)
        self.cipher_var = tk.StringVar(value="Caesar")
        base_ciphers = ["Caesar", "ROT13", "Atbash", "Vigenère"] + [p[0] for p in self.plugin_ciphers]
        self.cipher_menu = tk.OptionMenu(root, self.cipher_var, *base_ciphers)
        self.cipher_menu.config(font=self.font_label, bg="#ffd6e0", fg="#2d4356")
        self.cipher_menu.grid(row=3, column=1, sticky="w")

        tk.Label(root, text="Key:", font=self.font_label, bg="#ededed", fg="#2d4356").grid(row=3, column=2, sticky="e")
        self.key_entry = tk.Entry(root, width=8, font=self.font_label, bg="#EEE", fg="#2d4356")
        self.key_entry.grid(row=3, column=3, sticky="w")
        self.key_entry.insert(0, "3")
        self.key_entry.bind("<KeyRelease>", lambda e: self.live_preview())

        tk.Label(root, text="Alphabet:", font=self.font_label, bg="#ededed", fg="#2d4356").grid(row=3, column=4, sticky="e")
        self.alpha_entry = tk.Entry(root, width=16, font=("Consolas",11), bg="#EEE", fg="#2d4356")
        self.alpha_entry.grid(row=3, column=5, sticky="w")
        self.alpha_entry.insert(0, string.ascii_lowercase)
        self.alpha_entry.bind("<KeyRelease>", lambda e: self.live_preview())

        self.mode_var = tk.StringVar(value="encode")
        tk.Radiobutton(root, text="Encode", variable=self.mode_var, value="encode", font=self.font_label, bg="#ededed", fg="#2d4356", command=self.live_preview).grid(row=4, column=0, pady=2, sticky="e")
        tk.Radiobutton(root, text="Decode", variable=self.mode_var, value="decode", font=self.font_label, bg="#ededed", fg="#2d4356", command=self.live_preview).grid(row=4, column=1, sticky="w")

        self.go_btn = tk.Button(root, text="Process", command=self.process, font=self.font_btn, bg="#b7e5dd")
        self.go_btn.grid(row=5, column=0, columnspan=1, pady=7)
        self.brute_btn = tk.Button(root, text="Brute Force", command=self.brute_force, font=self.font_btn, bg="#ffd6e0")
        self.brute_btn.grid(row=5, column=1, columnspan=1, pady=7)
        self.tts_btn = tk.Button(root, text="Speak", command=self.speak_result, font=self.font_btn, bg="#ecc5fb")
        self.tts_btn.grid(row=5, column=2, columnspan=1, pady=7)

        tk.Label(root, text="Result:", font=self.font_label, bg="#ededed", fg="#2d4356").grid(row=6, column=0, sticky="e")
        self.result_box = tk.Entry(root, width=40, font=("Consolas", 15, "bold"), bg="#e5ecf6", fg="#b0413e")
        self.result_box.grid(row=6, column=1, columnspan=5, padx=5, sticky="w")

        self.copy_btn = tk.Button(root, text="Copy", command=self.copy_result, font=self.font_label, bg="#b7e5dd")
        self.copy_btn.grid(row=7, column=5, sticky="e", pady=5)
        self.status_label = tk.Label(root, text="", font=self.font_label, bg="#ededed", fg="#4e944f")
        self.status_label.grid(row=8, column=0, columnspan=8, pady=3)

        tk.Label(root, text="History:", font=self.font_label, bg="#ededed", fg="#2d4356").grid(row=9, column=0, sticky="nw", padx=3)
        self.history_box = tk.Listbox(root, width=80, height=6, font=("Consolas",12), bg="#f0f4f8", fg="#2d4356")
        self.history_box.grid(row=10, column=0, columnspan=8, padx=8, pady=3)
        self.clear_btn = tk.Button(root, text="Clear History", command=self.clear_history, font=self.font_label, bg="#ffd6e0")
        self.clear_btn.grid(row=11, column=7, sticky="e", padx=5)

    def file_drop(self, event):
        fname = event.data.strip('{}')
        if os.path.isfile(fname):
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_entry.delete(0, tk.END)
                self.text_entry.insert(0, content)
                self.status_label.config(text=f"Loaded {os.path.basename(fname)}", fg="#6a994e")
                self.live_preview()

    def paste_clip(self):
        self.text_entry.delete(0, tk.END)
        try:
            data = self.root.clipboard_get()
        except Exception:
            data = ""
        self.text_entry.insert(0, data)
        self.status_label.config(text="Clipboard pasted!", fg="#4e944f")
        self.live_preview()

    def get_alphabet(self):
        s = self.alpha_entry.get().strip()
        return s if s else string.ascii_lowercase

    def live_preview(self):
        text = self.text_entry.get()
        mode = self.mode_var.get()
        cipher = self.cipher_var.get()
        alpha = self.get_alphabet()
        key = self.key_entry.get()
        result = ""
        try:
            if cipher == "Caesar":
                k = int(key) if key else 3
                result = caesar_cipher(text, k, alpha, encode=(mode=="encode"))
            elif cipher == "ROT13":
                result = caesar_cipher(text, 13, alpha, encode=True)
            elif cipher == "Atbash":
                result = atbash_cipher(text, alpha)
            elif cipher == "Vigenère":
                result = vigenere_cipher(text, key, alpha, encode=(mode=="encode"))
            else:  # Plugin ciphers
                for name, encodef, decodef in load_plugins():
                    if cipher == name:
                        result = encodef(text) if mode=="encode" else decodef(text)
                        break
            self.result_box.delete(0, tk.END)
            self.result_box.insert(tk.END, result)
        except Exception:
            self.result_box.delete(0, tk.END)
            self.result_box.insert(tk.END, "[error in parameters]")

    def process(self):
        self.live_preview()
        text = self.text_entry.get()
        mode = self.mode_var.get()
        cipher = self.cipher_var.get()
        key = self.key_entry.get()
        alpha = self.get_alphabet()
        result = self.result_box.get()
        # Log non-empty result
        if result:
            action = f'{mode.capitalize()} ({cipher})'
            self.log_history(action, text, key, result)
            self.status_label.config(text=f'Done! {action}', fg="#4e944f")

    def brute_force(self):
        text = self.text_entry.get()
        alpha = self.get_alphabet()
        if not text.strip():
            self.status_label.config(text="Text is empty!", fg="#e94560")
            return
        cipher = self.cipher_var.get()
        if cipher != "Caesar":
            messagebox.showinfo("Note", "Brute Force is only for Caesar cipher.")
            return
        self.result_box.delete(0, tk.END)
        self.result_box.insert(tk.END, "See history for all shifts.")
        self.status_label.config(text="Brute force below!", fg="#fa4659")
        for k in range(len(alpha)):
            result = caesar_cipher(text, k, alpha, encode=False)
            self.log_history(f"Brute Force (Shift={k})", text, k, result)

    def copy_result(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_box.get())
        self.root.update()
        messagebox.showinfo("Copied", "Text copied!")

    def speak_result(self):
        text = self.result_box.get()
        speak(text)
        self.status_label.config(text="Speaking...", fg="#fa4659")

    def log_history(self, action, text, key, result):
        now = datetime.now().strftime("%H:%M:%S")
        msg = f"[{now}] {action} | Key={key} | {text} -> {result}"
        self.history_box.insert(tk.END, msg)
        if self.history_box.size() > 80:
            self.history_box.delete(0)

    def clear_history(self):
        self.history_box.delete(0, tk.END)

    def switch_theme(self):
        self.theme = 1 - self.theme
        bg = "#2d3250" if self.theme else "#ededed"
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=bg, fg="#fefae0" if self.theme else "#2d4356")
            elif isinstance(widget, tk.Entry):
                widget.config(bg="#232234" if self.theme else "#EEE", fg="#fefae0" if self.theme else "#2d4356")
            elif isinstance(widget, tk.Button):
                widget.config(bg="#7c3aed" if self.theme else "#ecc5fb")
            elif isinstance(widget, tk.Listbox):
                widget.config(bg="#232234" if self.theme else "#f0f4f8", fg="#fefae0" if self.theme else "#2d4356")
        self.result_box.config(bg="#232234" if self.theme else "#e5ecf6", fg="#ffd6e0" if self.theme else "#b0413e")

if __name__ == "__main__":
    root = tk.Tk()
    app = CipherSuiteProApp(root)
    root.mainloop()
