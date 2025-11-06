import tkinter as tk
from tkinter import messagebox
import random
import os

# Band name generation logic
adjectives = ["Amazing", "Electric", "Funky", "Majestic", "Thunderous", "Mellow", "Cosmic", "Groovy", "Radiant", "Lunar", "Epic"]
genre_suffixes = {
    "rock": ["Band", "Experience", "Squad"],
    "pop": ["Vibes", "Divas", "Stars"],
    "jazz": ["Quartet", "Collective", "Groove"],
    "metal": ["Force", "Storm", "Rage"],
    "indie": ["Project", "Sound", "Scene"],
    "default": ["Ensemble", "Crew"]
}
history_file = "band_names.txt"

def generate_names():
    city = city_entry.get().strip()
    pet = pet_entry.get().strip()
    genre = genre_entry.get().lower().strip()
    try:
        num = int(num_entry.get())
        if num < 1 or num > 5:
            num = 3
    except ValueError:
        num = 3

    if not city or not pet:
        messagebox.showerror("Error", "City and pet fields cannot be blank.")
        return

    if genre not in genre_suffixes:
        suffixes = genre_suffixes["default"]
    else:
        suffixes = genre_suffixes[genre]

    if city.lower() == "paris" or pet.lower() == "dragon":
        messagebox.showinfo("Bonus", "You have a truly legendary band setup!")

    names = set()
    used_names = set()
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            used_names = set(line.strip() for line in f)

    attempts = 0
    while len(names) < num and attempts < 12:
        adj = random.choice(adjectives)
        suf = random.choice(suffixes)
        name = f"{adj} {city} {pet} {suf}"
        if name not in used_names and name not in names:
            names.add(name)
        attempts += 1

    result_box.delete(0, tk.END)
    for n in names:
        result_box.insert(tk.END, n)

    with open(history_file, "a") as f:
        for n in names:
            f.write(f"{n}\n")

def show_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            all_names = [line.strip() for line in f]
        history_text = "\n".join(all_names)
        messagebox.showinfo("Band Name History", history_text if history_text else "No band names yet.")
    else:
        messagebox.showinfo("Band Name History", "No band names yet.")

# Tkinter UI setup
root = tk.Tk()
root.title("Band Name Generator")

tk.Label(root, text="City you grew up in:").grid(row=0, column=0, sticky="e")
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1)

tk.Label(root, text="Your pet's name:").grid(row=1, column=0, sticky="e")
pet_entry = tk.Entry(root)
pet_entry.grid(row=1, column=1)

tk.Label(root, text="Favorite genre (rock/pop/jazz/metal/indie):").grid(row=2, column=0, sticky="e")
genre_entry = tk.Entry(root)
genre_entry.grid(row=2, column=1)

tk.Label(root, text="How many suggestions? (1-5):").grid(row=3, column=0, sticky="e")
num_entry = tk.Entry(root)
num_entry.grid(row=3, column=1)
num_entry.insert(0, "3")

tk.Button(root, text="Generate Band Names", command=generate_names).grid(row=4, column=0, columnspan=2, pady=8)
tk.Button(root, text="Show History", command=show_history).grid(row=5, column=0, columnspan=2, pady=3)

result_box = tk.Listbox(root, width=45, height=6)
result_box.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
