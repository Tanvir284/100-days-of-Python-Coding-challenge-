import tkinter as tk
from tkinter import messagebox

def calculate_tip():
    try:
        total = float(total_entry.get())
        tip_percent = float(tip_entry.get())
        people = int(people_entry.get())
        if total < 0 or tip_percent < 0 or people < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid positive numbers (people > 0).")
        return

    tip_amount = total * (tip_percent / 100)
    grand_total = total + tip_amount
    split = grand_total / people

    result_box.config(state=tk.NORMAL)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"Total bill: ${total:.2f}\n")
    result_box.insert(tk.END, f"Tip ({tip_percent}%): ${tip_amount:.2f}\n")
    result_box.insert(tk.END, f"Grand total: ${grand_total:.2f}\n")
    result_box.insert(tk.END, f"Each person pays: ${split:.2f}\n")
    result_box.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Tip Calculator")

tk.Label(root, text="Total bill ($):").grid(row=0, column=0, sticky="e")
total_entry = tk.Entry(root)
total_entry.grid(row=0, column=1)

tk.Label(root, text="Tip percentage (%):").grid(row=1, column=0, sticky="e")
tip_entry = tk.Entry(root)
tip_entry.grid(row=1, column=1)
tip_entry.insert(0, "15")

tk.Label(root, text="Number of people:").grid(row=2, column=0, sticky="e")
people_entry = tk.Entry(root)
people_entry.grid(row=2, column=1)
people_entry.insert(0, "2")

tk.Button(root, text="Calculate", command=calculate_tip).grid(row=3, column=0, columnspan=2, pady=8)

result_box = tk.Text(root, width=38, height=6, state=tk.DISABLED)
result_box.grid(row=4, column=0, columnspan=2, padx=10, pady=8)

root.mainloop()
