import tkinter as tk
import random
from tkinter import messagebox
import time

try:
    from playsound import playsound
    HAVE_SOUND = True
except ImportError:
    HAVE_SOUND = False

CHOICES = [('✊', 'Rock'), ('🖐', 'Paper'), ('✌', 'Scissors')]
THEMES = [
    {"bg": "#f0f4f8", "fg": "#222", "btn": "#aee1f9", "active": "#83e9f8", "result": "#f7cac9"},
    {"bg": "#1a1a2e", "fg": "#f4dfa2", "btn": "#16213e", "active": "#0f3460", "result": "#e94560"},
]

def clamp(val):
    return max(0, min(val, 255))

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 40
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, bg="#ffeebb", fg="#333", font=("Helvetica", 10), relief=tk.SOLID, borderwidth=1, padx=8, pady=3)
        label.pack()

    def hide(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.theme = 0
        self.root.title("🌟 Rock-Paper-Scissors Deluxe 🌟")
        self.root.geometry("480x500")
        self.root.configure(bg=THEMES[self.theme]['bg'])
        self.choices = CHOICES
        self.score = {"User": 0, "Computer": 0}
        self.streak = 0
        self.best_streak = 0
        self.history = []

        # Gradient header -- now fully safe!
        self.header_canvas = tk.Canvas(root, width=470, height=60, highlightthickness=0)
        self.header_canvas.pack()
        for i in range(470):
            r = clamp(255 - i//2)
            g = clamp(202 - i//4)
            b = clamp(169 - i//2)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.header_canvas.create_line(i, 0, i, 65, fill=color)
        self.header_text = self.header_canvas.create_text(235, 30, text="Rock-Paper-Scissors Deluxe", font=("Comic Sans MS", 22, "bold"), fill="#21209c")

        # Main label
        self.main_label = tk.Label(root, text="✊ Choose your move!", font=("Comic Sans MS", 15, "bold"),
                                   bg=THEMES[self.theme]['bg'], fg=THEMES[self.theme]['fg'])
        self.main_label.pack(pady=10)

        # Button frame
        btn_frame = tk.Frame(root, bg=THEMES[self.theme]['bg'])
        btn_frame.pack(pady=5)
        self.icon_buttons = []
        for i, (icon, label) in enumerate(self.choices):
            btn = tk.Button(btn_frame, text=f"{icon}\n{label}", width=8, height=3,
                            font=("Arial", 15, "bold"), bg=THEMES[self.theme]['btn'],
                            fg=THEMES[self.theme]['fg'],
                            activebackground=THEMES[self.theme]['active'],
                            command=lambda choice=label: self.play(choice))
            btn.grid(row=0, column=i, padx=14)
            Tooltip(btn, f"Beat {label}'s weakness!")
            self.icon_buttons.append(btn)

        theme_btn = tk.Button(root, text="Change Theme 🌓", command=self.change_theme,
                              font=("Arial",11,"bold"), bg="#eaf6f6")
        theme_btn.pack()

        self.streak_label = tk.Label(root, text=f"Streak: {self.streak} | Best: {self.best_streak}",
                                     font=("Helvetica", 12, "bold"), bg=THEMES[self.theme]['bg'], fg="#900")
        self.streak_label.pack(pady=2)

        self.result_label = tk.Label(root, text="", font=("Comic Sans MS", 13, "bold"),
                                    bg=THEMES[self.theme]['result'], fg="#222")
        self.result_label.pack(pady=10, fill="x")

        self.score_label = tk.Label(root, text="Score: User 0 - Computer 0",
                                   font=("Helvetica", 12, "bold"), bg=THEMES[self.theme]['bg'], fg="#3498db")
        self.score_label.pack(pady=5)

        log_frame = tk.Frame(root, bg=THEMES[self.theme]['bg'])
        log_frame.pack(pady=7)
        tk.Label(log_frame, text="History:", font=("Helvetica",11,"bold"), bg=THEMES[self.theme]['bg']).pack()
        self.history_box = tk.Listbox(log_frame, width=33, height=6, font=("Helvetica", 10), fg="#605c5c", bg="#f0f4f8")
        self.history_box.pack()

        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset, font=("Helvetica",11), bg="#f7cac9")
        self.reset_button.pack(pady=7)

    def change_theme(self):
        self.theme = 1 - self.theme
        colors = THEMES[self.theme]
        self.root.configure(bg=colors['bg'])
        self.main_label.config(bg=colors['bg'], fg=colors['fg'])
        self.score_label.config(bg=colors['bg'])
        self.streak_label.config(bg=colors['bg'])
        self.result_label.config(bg=colors['result'])
        for btn in self.icon_buttons:
            btn.config(bg=colors['btn'], fg=colors['fg'], activebackground=colors['active'])
        self.history_box.config(bg=colors['bg'] if self.theme else "#f0f4f8")
        self.reset_button.config(bg="#e94560" if self.theme else "#f7cac9")

    def play(self, user_choice):
        computer_choice = random.choice([c[1] for c in self.choices])
        result = ""
        if user_choice == computer_choice:
            result = f"{user_choice} vs {computer_choice}: It's a Tie!"
            self.streak = 0
            if HAVE_SOUND: self.playsound('tie.wav')
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Paper" and computer_choice == "Rock") or \
             (user_choice == "Scissors" and computer_choice == "Paper"):
            result = f"{user_choice} beats {computer_choice}: You Win!"
            self.score["User"] += 1
            self.streak += 1
            self.best_streak = max(self.streak, self.best_streak)
            if HAVE_SOUND: self.playsound('win.wav')
        else:
            result = f"{computer_choice} beats {user_choice}: Computer Wins!"
            self.score["Computer"] += 1
            self.streak = 0
            if HAVE_SOUND: self.playsound('lose.wav')

        self.result_label.config(text=result)
        self.score_label.config(text=f"Score: User {self.score['User']} - Computer {self.score['Computer']}")
        self.streak_label.config(text=f"Streak: {self.streak} | Best: {self.best_streak}")
        self.history.append(result)
        self.history_box.insert(tk.END, result)
        if len(self.history) > 15:
            self.history_box.delete(0, tk.END)
            self.history = self.history[-10:]
            for item in self.history: self.history_box.insert(tk.END, item)

    def reset(self):
        self.score = {"User": 0, "Computer": 0}
        self.streak = 0
        self.result_label.config(text="")
        self.score_label.config(text="Score: User 0 - Computer 0")
        self.streak_label.config(text=f"Streak: 0 | Best: {self.best_streak}")
        self.history = []
        self.history_box.delete(0, tk.END)
        if HAVE_SOUND: self.playsound('reset.wav')

    def playsound(self, filename):
        try:
            playsound(filename, block=False)
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGame(root)
    root.mainloop()
