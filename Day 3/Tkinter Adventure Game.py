import tkinter as tk
from tkinter import messagebox, font
import random


class AdventureGame:
    def __init__(self, root):
        self.root = root
        self.root.title('🌴 Treasure Island Adventure 🌴')
        self.root.configure(bg='#f7cac9')
        self.boldfont = font.Font(family="Helvetica", size=12, weight="bold")
        self.headfont = font.Font(family="Comic Sans MS", size=15, weight="bold")

        # --- Widget setup ---
        self.result_box = tk.Text(root, width=54, height=7, state=tk.DISABLED, bg="#fff0f5", font=self.headfont)
        self.result_box.pack(pady=10)
        self.inventory_box = tk.Text(root, width=54, height=1, state=tk.DISABLED, bg="#ffeebb", font=self.boldfont)
        self.inventory_box.pack(pady=5)

        btn_kwargs = dict(font=self.boldfont, bg="#deeaee", fg="#333", activebackground="#c1c8e4",
                          activeforeground="#333")
        self.entry_box = tk.Entry(root, width=30, font=self.boldfont, bg="#eaf6f6")
        self.ok_button = tk.Button(root, text="OK", command=self.start_next, **btn_kwargs)
        self.left_button = tk.Button(root, text="Go Left ➔", width=14, command=self.left_path, **btn_kwargs)
        self.right_button = tk.Button(root, text="Go Right ➔", width=14, command=self.right_path, **btn_kwargs)
        self.swim_button = tk.Button(root, text="Swim 🏊", width=14, command=self.swim_path, **btn_kwargs)
        self.wait_button = tk.Button(root, text="Wait ⏳", width=14, command=self.wait_path, **btn_kwargs)
        self.red_button = tk.Button(root, text="Red Door 🚪", width=14, command=self.red_door, **btn_kwargs)
        self.blue_button = tk.Button(root, text="Blue Door 🔵", width=14, command=self.blue_door, **btn_kwargs)
        self.yellow_button = tk.Button(root, text="Yellow Door 🟡", width=14, command=self.yellow_door, **btn_kwargs)
        self.hint_button = tk.Button(root, text="🔍 Hint", width=14, command=self.show_hint, **btn_kwargs)
        self.get_key_button = tk.Button(root, text="🔑 Pick Up Key", width=14, command=self.pick_key, **btn_kwargs)
        self.use_key_button = tk.Button(root, text="🔓 Use Key", width=14, command=self.use_key, **btn_kwargs)
        self.restart_button = tk.Button(root, text="Restart 🔄", width=14, command=self.restart, **btn_kwargs)

        # --- Start the game ---
        self.reset_game()

    def reset_game(self):
        self.name = ''
        self.stage = 'start'
        self.inventory = []
        self.history = []
        self.result("🌟 Welcome to Treasure Island! 🌟\n\nWhat is your name?")
        self.hide_all()
        self.entry_box.pack(pady=8)
        self.entry_box.delete(0, tk.END)
        self.entry_box.focus_set()
        self.ok_button.pack(pady=4)

    def hide_all(self):
        widgets = [
            self.entry_box, self.ok_button, self.left_button, self.right_button, self.swim_button,
            self.wait_button, self.red_button, self.blue_button, self.yellow_button,
            self.hint_button, self.get_key_button, self.use_key_button, self.restart_button
        ]
        for widget in widgets:
            widget.pack_forget()
        self.inventory_box.config(state=tk.NORMAL)
        self.inventory_box.delete(1.0, tk.END)
        self.inventory_box.config(state=tk.DISABLED)

    def result(self, text):
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, text)
        self.result_box.config(state=tk.DISABLED)
        self.root.update()

    def start_next(self):
        self.name = self.entry_box.get().strip()
        if not self.name:
            messagebox.showerror('Input Error', 'Please enter a name!')
            return
        self.stage = 'lake'
        self.history = [f'Player name: {self.name}']
        self.result(f"Hello, {self.name}! Your mission: find the treasure.\nDo you go 'left' or 'right'?")
        self.hide_all()
        self.left_button.pack(side=tk.LEFT, padx=6)
        self.right_button.pack(side=tk.LEFT, padx=6)
        self.hint_button.pack(side=tk.LEFT, padx=6)
        self.update_inventory()

    def left_path(self):
        self.stage = 'lake_choice'
        self.history.append('Chose: left')
        self.result("You come to a lake. Would you 'swim' or 'wait'?")
        self.hide_all()
        self.swim_button.pack(side=tk.LEFT, padx=6)
        self.wait_button.pack(side=tk.LEFT, padx=6)
        self.hint_button.pack(side=tk.LEFT, padx=6)
        if "Key" not in self.inventory and random.choice([True, False]):
            self.result_box.config(state=tk.NORMAL)
            self.result_box.insert(tk.END, "\n🔑 You see something shiny by the lake. Pick it up?")
            self.result_box.config(state=tk.DISABLED)
            self.get_key_button.pack(side=tk.LEFT, padx=6)
        self.update_inventory()

    def right_path(self):
        self.stage = 'hole'
        self.history.append('Chose: right')
        self.result(f"💀 Oops, {self.name} fell into a hole. Game Over!\nCheck history for your choices.")
        self.hide_all()
        self.restart_button.pack()
        self.show_history()

    def swim_path(self):
        self.stage = 'swim'
        self.history.append('Chose: swim')
        self.result("🐟 You try to swim but are attacked by trout. Game Over!\nCheck history for your choices.")
        self.hide_all()
        self.restart_button.pack()
        self.show_history()

    def wait_path(self):
        self.stage = 'doors'
        self.history.append('Chose: wait')
        text = ("🛖 You safely arrive on the island. There's a house with three doors:\n"
                "🚪 Red, 🔵 Blue, and 🟡 Yellow. Which will you choose?")
        if "Key" in self.inventory:
            text += "\nYou feel the key could fit one of the doors."
        self.result(text)
        self.hide_all()
        self.red_button.pack(side=tk.LEFT, padx=6)
        self.blue_button.pack(side=tk.LEFT, padx=6)
        self.yellow_button.pack(side=tk.LEFT, padx=6)
        if "Key" in self.inventory:
            self.use_key_button.pack(side=tk.LEFT, padx=6)
        self.hint_button.pack(side=tk.LEFT, padx=6)
        self.update_inventory()

    def red_door(self):
        self.stage = 'red'
        self.history.append('Chose: red door')
        self.result("🔥 You open the red door... burned by fire. Game Over!\nCheck history for your choices.")
        self.hide_all()
        self.restart_button.pack()
        self.show_history()

    def blue_door(self):
        self.stage = 'blue'
        self.history.append('Chose: blue door')
        self.result("🦁 You open the blue door... beasts inside! Game Over!\nCheck history for your choices.")
        self.hide_all()
        self.restart_button.pack()
        self.show_history()

    def yellow_door(self):
        self.stage = 'yellow'
        self.history.append('Chose: yellow door')
        self.result(f"💰 {self.name}, you found the treasure! You Win!\nCheck history for your choices.")
        self.hide_all()
        self.restart_button.pack()
        self.show_history()

    def show_hint(self):
        hints = {
            "start": "Think carefully about your path.",
            "lake": "Sometimes patience pays off.",
            "lake_choice": "Check the area for useful items.",
            "doors": "The key might help you unlock something special.",
        }
        hint = hints.get(self.stage, "No hints available for this stage.")
        messagebox.showinfo("Hint", hint)

    def pick_key(self):
        self.inventory.append("Key")
        self.get_key_button.pack_forget()
        messagebox.showinfo("Item Acquired", "You picked up a key!")
        self.update_inventory()

    def use_key(self):
        if "Key" in self.inventory and self.stage == "doors":
            self.history.append('Used: key')
            self.result(f"💎 {self.name}, you unlock a secret door and find a diamond! You Win with bonus loot!")
            self.inventory.remove("Key")
            self.hide_all()
            self.restart_button.pack()
            self.show_history()
        else:
            messagebox.showinfo("Invalid", "There's nowhere to use your key right now.")

    def update_inventory(self):
        self.inventory_box.config(state=tk.NORMAL)
        self.inventory_box.delete(1.0, tk.END)
        self.inventory_box.insert(tk.END, f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        self.inventory_box.config(state=tk.DISABLED)

    def show_history(self):
        log = "\n".join(self.history)
        messagebox.showinfo("Your Path History", f"Choices & events so far:\n\n{log}")

    def restart(self):
        self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = AdventureGame(root)
    root.mainloop()
