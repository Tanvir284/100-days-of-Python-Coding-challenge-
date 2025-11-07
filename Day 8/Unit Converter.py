import tkinter as tk
from tkinter import messagebox
import math

THEMES = [
    {"bg": "#f9fde7", "btn": "#bae1ff", "result": "#ffeebb", "fg": "#253456", "highlight": "#4b9cd3"},
    {"bg": "#212c3d", "btn": "#6c7b95", "result": "#29335c", "fg": "#fff1eb", "highlight": "#ffc857"},
]

UNIT_CATEGORIES = {
    "Length": {
        "meter": 1.0,
        "kilometer": 1000.0,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
        "cm": 0.01,
        "mm": 0.001,
    },
    "Mass": {
        "gram": 1.0,
        "kilogram": 1000.0,
        "pound": 453.592,
        "ounce": 28.3495,
        "tonne": 1e6,
        "milligram": 0.001,
    },
    "Temperature": {
        "celsius": (1, 0),
        "fahrenheit": (5/9, -32),
        "kelvin": (1, -273.15),
    },
    "Time": {
        "second": 1.0,
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400.0,
        "week": 604800.0,
    },
    "Speed": {
        "m/s": 1.0,
        "km/h": 0.277778,
        "mph": 0.44704,
        "knot": 0.514444,
    }
}

class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.theme = 0
        self.root.title("🧮 Day 9: Ultimate Unit Converter")
        self.root.configure(bg=THEMES[self.theme]["bg"])

        self.history = []

        self.cat_var = tk.StringVar(value="Length")
        self.unit1_var = tk.StringVar(value="meter")
        self.unit2_var = tk.StringVar(value="kilometer")
        self.amount_var = tk.StringVar()

        tk.Label(root, text="Category:", font=("Helvetica",14,"bold"), bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).grid(row=0, column=0, pady=7, sticky="e")
        self.cat_menu = tk.OptionMenu(root, self.cat_var, *UNIT_CATEGORIES.keys(), command=self.update_units)
        self.cat_menu.config(font=("Helvetica",14), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"])
        self.cat_menu.grid(row=0, column=1, padx=6, sticky="w")

        tk.Label(root, text="From:", font=("Helvetica",13), bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).grid(row=1, column=0, sticky="e")
        self.unit1_menu = tk.OptionMenu(root, self.unit1_var, *UNIT_CATEGORIES["Length"].keys())
        self.unit1_menu.config(font=("Helvetica",13), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"])
        self.unit1_menu.grid(row=1, column=1, padx=6, sticky="w")

        tk.Label(root, text="To:", font=("Helvetica",13), bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).grid(row=2, column=0, sticky="e")
        self.unit2_menu = tk.OptionMenu(root, self.unit2_var, *UNIT_CATEGORIES["Length"].keys())
        self.unit2_menu.config(font=("Helvetica",13), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"])
        self.unit2_menu.grid(row=2, column=1, padx=6, sticky="w")

        tk.Label(root, text="Value:", font=("Helvetica",13), bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["fg"]).grid(row=3, column=0, sticky="e")
        self.amount_entry = tk.Entry(root, textvariable=self.amount_var, font=("Consolas",14), bg="#eaf6f6", fg=THEMES[self.theme]["fg"])
        self.amount_entry.grid(row=3, column=1, padx=10, sticky="w")

        self.convert_btn = tk.Button(root, text="Convert", command=self.convert, font=("Helvetica",14,"bold"), bg=THEMES[self.theme]["highlight"], fg="#fff")
        self.convert_btn.grid(row=4, column=0, columnspan=2, pady=10)
        self.theme_btn = tk.Button(root, text="Switch Theme 🌓", command=self.switch_theme, font=("Helvetica",12), bg=THEMES[self.theme]["highlight"], fg="#fff")
        self.theme_btn.grid(row=4, column=2, padx=7)

        self.result_box = tk.Entry(root, font=("Consolas",16), bg=THEMES[self.theme]["result"], fg=THEMES[self.theme]["fg"], width=32)
        self.result_box.grid(row=5, column=0, columnspan=3, pady=8, padx=5)

        self.history_box = tk.Listbox(root, width=47, height=6, font=("Consolas",11), bg="#eaf6f6", fg="#294d61")
        self.history_box.grid(row=6, column=0, columnspan=3, padx=6, pady=3)
        self.copy_btn = tk.Button(root, text="Copy Result", command=self.copy_result, font=("Helvetica",12), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"])
        self.copy_btn.grid(row=7, column=1, pady=7)
        self.update_units("Length")

    def switch_theme(self):
        self.theme = 1 - self.theme
        th = THEMES[self.theme]
        self.root.configure(bg=th["bg"])
        for w in self.root.winfo_children():
            if isinstance(w, tk.Label):
                w.config(bg=th["bg"], fg=th["fg"])
            elif isinstance(w, tk.OptionMenu):
                w.config(bg=th["btn"], fg=th["fg"])
            elif isinstance(w, tk.Entry):
                w.config(bg="#eaf6f6", fg=th["fg"])
            elif isinstance(w, tk.Button):
                w.config(bg=th["highlight"], fg="#fff")
            elif isinstance(w, tk.Listbox):
                w.config(bg="#eaf6f6", fg="#294d61")
        self.result_box.config(bg=th["result"], fg=th["fg"])
        self.amount_entry.config(bg="#eaf6f6", fg=th["fg"])
        self.copy_btn.config(bg=th["btn"], fg=th["fg"])

    def update_units(self, cat):
        # Update 'from' and 'to' menus
        units = UNIT_CATEGORIES[self.cat_var.get()]
        menu1 = self.unit1_menu["menu"]
        menu2 = self.unit2_menu["menu"]
        menu1.delete(0, "end")
        menu2.delete(0, "end")
        for u in units.keys():
            menu1.add_command(label=u, command=tk._setit(self.unit1_var, u))
            menu2.add_command(label=u, command=tk._setit(self.unit2_var, u))
        self.unit1_var.set(list(units.keys())[0])
        self.unit2_var.set(list(units.keys())[1])

    def convert(self):
        cat = self.cat_var.get()
        try:
            value = float(self.amount_var.get())
        except:
            self.result_box.delete(0, tk.END)
            self.result_box.insert(0, "Invalid value")
            return
        from_u = self.unit1_var.get()
        to_u = self.unit2_var.get()
        if cat != "Temperature":
            units = UNIT_CATEGORIES[cat]
            val_si = value * units[from_u]
            result = val_si / units[to_u]
        else:
            # Handle temperature conversions
            temp = value
            if from_u == "fahrenheit":
                temp = (value - 32) * 5/9
            elif from_u == "kelvin":
                temp = value - 273.15
            if to_u == "celsius":
                result = temp
            elif to_u == "fahrenheit":
                result = temp * 9/5 + 32
            elif to_u == "kelvin":
                result = temp + 273.15
        out_str = f"{value} {from_u} = {result:.4f} {to_u}"
        self.result_box.delete(0, tk.END)
        self.result_box.insert(0, out_str)
        self.history_box.insert(tk.END, out_str)

    def copy_result(self):
        res = self.result_box.get()
        if res and "Invalid" not in res:
            self.root.clipboard_clear()
            self.root.clipboard_append(res)
            self.root.update()
            messagebox.showinfo("Copied", f"Result copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()
