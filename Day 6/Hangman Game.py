import tkinter as tk
import random

WORDS = [
    "python", "developer", "algorithm", "variable",
    "function", "machine", "learning", "project",
    "security", "hangman", "keyboard", "optimize",
    "challenge", "scripting", "virtual", "network"
]

HANGMANPICS = [
    "",
    "O",
    "O\n|",
    "O\n/|",
    "O\n/|\\",
    "O\n/|\\\n/",
    "O\n/|\\\n/ \\"
]


class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🪢 Hangman Game Deluxe")
        self.root.configure(bg="#f8efd4")
        self.font_title = ("Comic Sans MS", 18, "bold")
        self.font_word = ("Consolas", 23, "bold")
        self.font_normal = ("Helvetica", 13)
        self.font_lives = ("Helvetica", 13, "bold")

        self.word_label = tk.Label(root, text="", font=self.font_word, bg="#d0f4de", fg="#3b2e5a", width=14)
        self.word_label.pack(pady=15)

        self.hangman_display = tk.Label(root, text="", font=("Consolas", 24, "bold"), bg="#ffd6e0", fg="#ae378b",
                                        width=10, height=3)
        self.hangman_display.pack()

        self.lives_label = tk.Label(root, text="", font=self.font_lives, bg="#f8efd4", fg="#bf1e2e")
        self.lives_label.pack(pady=5)

        # on-screen keyboard
        self.kb_frame = tk.Frame(root, bg="#f8efd4")
        self.kb_frame.pack(pady=10)
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            b = tk.Button(self.kb_frame, text=letter, width=4, font=("Helvetica", 11, "bold"), bg="#aee1f9",
                          command=lambda l=letter: self.make_guess(l.lower()))
            b.grid(row=i // 9, column=i % 9, padx=2, pady=2)

        self.msg_label = tk.Label(root, text="", font=self.font_normal, bg="#dde7c7", fg="#394a51", width=36)
        self.msg_label.pack(pady=10)

        self.reset_btn = tk.Button(root, text="New Game", command=self.reset, font=("Helvetica", 12), bg="#ffedc2")
        self.reset_btn.pack()

        self.root.bind('<Key>', self.key_guess)
        self.reset()

    def reset(self):
        self.secret_word = random.choice(WORDS)
        self.display_word = ["_" for _ in self.secret_word]
        self.guessed = set()
        self.missed = 0
        self.update_display()
        self.lives_label.config(text=f"Lives: {6 - self.missed}   ")
        self.msg_label.config(text="Guess a letter!")
        for btn in self.kb_frame.winfo_children():
            btn.config(state=tk.NORMAL, relief=tk.RAISED, bg="#aee1f9")
        self.over = False
        self.hangman_display.config(text=HANGMANPICS[self.missed])

    def make_guess(self, char):
        if self.over or char in self.guessed:
            return
        self.guessed.add(char)
        for btn in self.kb_frame.winfo_children():
            if btn['text'].lower() == char:
                btn.config(state=tk.DISABLED, relief=tk.SUNKEN, bg="#ffd6e0")
        if char in self.secret_word:
            for idx, c in enumerate(self.secret_word):
                if c == char:
                    self.display_word[idx] = c
            self.msg_label.config(text="Good guess!")
        else:
            self.missed += 1
            self.msg_label.config(text=f"Nope! {6 - self.missed} lives left.")
        self.update_display()
        self.hangman_display.config(text=HANGMANPICS[self.missed])
        if "_" not in self.display_word:
            self.msg_label.config(text=f"🎉 YOU WIN! The word was: {self.secret_word}")
            self.over = True
        elif self.missed >= 6:
            self.msg_label.config(text=f"💀 GAME OVER! The word was: {self.secret_word}")
            self.over = True
            # Reveal the word
            for i, c in enumerate(self.secret_word):
                self.display_word[i] = c
            self.update_display()

    def update_display(self):
        self.word_label.config(text=" ".join(self.display_word))
        self.lives_label.config(text=f"Lives: {6 - self.missed}   ")

    def key_guess(self, event):
        if event.char.isalpha():
            self.make_guess(event.char.lower())


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()
