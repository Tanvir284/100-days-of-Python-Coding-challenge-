import tkinter as tk
import random
import string

# For password scoring
def score(password):
    length = len(password)
    types = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in "@#$%!?^&*()_-~" for c in password)
    ])
    entropy = length * (types * 2.5)
    if length >= 16 and types == 4:
        label, color = "Excellent", "#88cc44"
    elif length >= 12 and types >= 3:
        label, color = "Strong", "#33aaff"
    elif length >= 8 and types >= 2:
        label, color = "Medium", "#ffaa22"
    else:
        label, color = "Weak", "#ee4433"
    return label, color, entropy

# Secure password generator that ensures all types if selected
def secure_password(length, lower, upper, digit, symbol, ambiguous):
    # Define allowed chars
    l = string.ascii_lowercase
    u = string.ascii_uppercase
    d = string.digits
    s = "@#$%!?^&*()_-~"
    # Remove ambiguous chars if requested
    if ambiguous:
        l = ''.join(c for c in l if c not in "ilo")
        u = ''.join(c for c in u if c not in "O")
        d = ''.join(c for c in d if c not in "01")
    charsets = []
    if lower: charsets.append(l)
    if upper: charsets.append(u)
    if digit: charsets.append(d)
    if symbol: charsets.append(s)
    if not charsets: return ""
    chars = ''.join(charsets)
    # Guarantee at least one from each type
    password = [random.choice(cs) for cs in charsets]
    while len(password) < length:
        password.append(random.choice(chars))
    random.shuffle(password)
    return ''.join(password[:length])

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.theme = 0
        self.root.title("🔑 Ultra Password Generator")
        self.root.configure(bg="#eaf6f6")
        self.font_main = ("Comic Sans MS",14,"bold")
        self.font_label = ("Helvetica",12)
        self.font_btn = ("Helvetica",12,"bold")
        self.colors = [ # Light, Dark
            {"bg": "#eaf6f6", "btn": "#f7cac9", "list": "#d0f4de", "fg": "#112", "meterbg":"#eaf6f6"},
            {"bg": "#21243d", "btn": "#6c47be", "list": "#222844", "fg": "#f6fbff", "meterbg":"#21243d"}
        ]

        tk.Label(root, text="Password Length:", font=self.font_main, bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=0, column=0, sticky="e", padx=9, pady=8)
        self.length_entry = tk.Entry(root, width=7, font=self.font_label, bg=self.colors[self.theme]["list"])
        self.length_entry.grid(row=0, column=1, pady=9)
        self.length_entry.insert(0, "16")

        self.opt_lower = tk.BooleanVar(value=True)
        self.opt_upper = tk.BooleanVar(value=True)
        self.opt_digit = tk.BooleanVar(value=True)
        self.opt_symbol = tk.BooleanVar(value=True)
        self.opt_ambig = tk.BooleanVar(value=True)

        tk.Checkbutton(root, text="a-z", variable=self.opt_lower, font=self.font_label,
                       bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=1, column=0, padx=8)
        tk.Checkbutton(root, text="A-Z", variable=self.opt_upper, font=self.font_label,
                       bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=1, column=1)
        tk.Checkbutton(root, text="0-9", variable=self.opt_digit, font=self.font_label,
                       bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=2, column=0, padx=8)
        tk.Checkbutton(root, text="@#$", variable=self.opt_symbol, font=self.font_label,
                       bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=2, column=1)
        tk.Checkbutton(root, text="No ambiguous chars", variable=self.opt_ambig, font=self.font_label,
                       bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=3, column=0,
                                                                                                columnspan=2)

        tk.Label(root, text="How many suggestions?", font=self.font_label, bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=4, column=0, pady=7)
        self.amount_entry = tk.Entry(root, width=7, font=self.font_label, bg=self.colors[self.theme]["list"])
        self.amount_entry.grid(row=4, column=1)
        self.amount_entry.insert(0, "3")

        self.gen_btn = tk.Button(root, text="Generate", command=self.generate, font=self.font_btn, bg=self.colors[self.theme]["btn"])
        self.gen_btn.grid(row=5, column=0, columnspan=2, pady=10)
        self.theme_btn = tk.Button(root, text="Switch Theme 🌓", command=self.switch_theme, font=self.font_label, bg="#d0f4de")
        self.theme_btn.grid(row=5, column=1, padx=3)

        self.result_box = tk.Listbox(root, width=38, height=5, font=("Consolas",13), bg=self.colors[self.theme]["list"], fg="#21209c", selectbackground="#88cc44")
        self.result_box.grid(row=6, column=0, columnspan=2, padx=8, pady=2)

        self.copy_btn = tk.Button(root, text="Copy Selected", command=self.copy_password, font=self.font_label, bg="#aee1f9")
        self.copy_btn.grid(row=7, column=0, columnspan=2, pady=5)

        # Show/hide toggle
        self.show_var = tk.BooleanVar(value=True)
        self.show_btn = tk.Checkbutton(root, text="Show Passwords", variable=self.show_var, command=self.toggle_show, font=self.font_label, bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"])
        self.show_btn.grid(row=8, column=0, columnspan=2, pady=2)

        # Strength meter bar
        self.str_label = tk.Label(root, text="Strength: ", font=self.font_label, bg=self.colors[self.theme]["meterbg"], fg=self.colors[self.theme]["fg"])
        self.str_label.grid(row=9, column=0, padx=8)
        self.meter_canvas = tk.Canvas(root, width=160, height=15, bg=self.colors[self.theme]["meterbg"], highlightthickness=0)
        self.meter_canvas.grid(row=9, column=1)

        # Entropy
        self.entropy_label = tk.Label(root, text="Entropy: ", font=self.font_label, bg=self.colors[self.theme]["meterbg"], fg=self.colors[self.theme]["fg"])
        self.entropy_label.grid(row=10, column=0, columnspan=2, pady=2)

    def switch_theme(self):
        self.theme = 1 - self.theme
        c = self.colors[self.theme]
        self.root.configure(bg=c["bg"])
        for w in [self.length_entry, self.amount_entry, self.result_box, self.meter_canvas]:
            w.config(bg=c["list"])
        for w in [self.gen_btn, self.theme_btn, self.copy_btn]:
            w.config(bg=c["btn"])
        for w in [self.str_label, self.entropy_label, self.show_btn]:
            w.config(bg=c["meterbg"], fg=c["fg"])
        for row in self.root.grid_slaves():
            if isinstance(row, tk.Checkbutton) or isinstance(row, tk.Label):
                row.config(bg=c["bg"], fg=c["fg"])

    def generate(self):
        try:
            length = int(self.length_entry.get())
            amount = int(self.amount_entry.get())
        except:
            tk.messagebox.showerror("Invalid Input", "Length and amount must be integers.")
            return
        if length < 6 or amount < 1:
            tk.messagebox.showerror("Invalid Input", "Length must be ≥6, amount ≥1.")
            return

        lower = self.opt_lower.get()
        upper = self.opt_upper.get()
        digit = self.opt_digit.get()
        symbol = self.opt_symbol.get()
        ambiguous = self.opt_ambig.get()

        self.result_box.delete(0, tk.END)
        passwords = []
        for _ in range(amount):
            password = secure_password(length, lower, upper, digit, symbol, ambiguous)
            passwords.append(password)
            display_pw = password if self.show_var.get() else '*' * len(password)
            self.result_box.insert(tk.END, display_pw)
        # Score for first password
        if passwords:
            label, color, entropy = score(passwords[0])
            self.str_label.config(text=f"Strength: {label}")
            self.entropy_label.config(text=f"Entropy: {round(entropy,2)} bits")
            self.meter_canvas.delete("all")
            meter_len = int(entropy)
            self.meter_canvas.create_rectangle(5, 5, min(155,meter_len*2), 14, fill=color, outline="")
        else:
            self.str_label.config(text="Strength: ")
            self.entropy_label.config(text="Entropy: ")
            self.meter_canvas.delete("all")

    def copy_password(self):
        sel = self.result_box.curselection()
        if not sel:
            tk.messagebox.showinfo("Copy", "Select a password to copy.")
            return
        pw = self.result_box.get(sel)
        # Copy actual password not hidden (if hidden, index matches passwords list)
        if not self.show_var.get():
            length = int(self.length_entry.get())
            lower = self.opt_lower.get()
            upper = self.opt_upper.get()
            digit = self.opt_digit.get()
            symbol = self.opt_symbol.get()
            ambiguous = self.opt_ambig.get()
            password = secure_password(length, lower, upper, digit, symbol, ambiguous)
            pw = password
        self.root.clipboard_clear()
        self.root.clipboard_append(pw)
        self.root.update()
        tk.messagebox.showinfo("Copy", "Password copied to clipboard.")

    def toggle_show(self):
        self.generate()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
