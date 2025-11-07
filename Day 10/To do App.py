import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime, timedelta
import json

THEMES = [
    {"bg":"#faf3e3","btn":"#aee1f9","entry":"#ffeebb","fg":"#253456","done":"#bcbcbc","highlight":"#4994bf"},
    {"bg":"#232946","btn":"#eeb1b1","entry":"#232946","fg":"#fff1eb","done":"#5c5b5e","highlight":"#f4d35e"}
]

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.theme = 0
        self.root.title("Day 10: To-Do List/Task Manager Pro")
        self.root.configure(bg=THEMES[self.theme]["bg"])

        self.tasks = []  # Each task is dict: {text, done, priority, due, category}
        self.filter_var = tk.StringVar(value="All")
        self.search_var = tk.StringVar()
        self.stats_var = tk.StringVar()

        self.task_entry = tk.Entry(root, font=("Consolas",13), bg=THEMES[self.theme]["entry"], fg=THEMES[self.theme]["fg"], width=32)
        self.task_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=7)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.add_btn = tk.Button(root, text="Add Task", command=self.add_task, font=("Helvetica",12), bg=THEMES[self.theme]["highlight"], fg="#fff")
        self.add_btn.grid(row=0, column=2, pady=7)
        self.theme_btn = tk.Button(root, text="Switch Theme 🌓", command=self.switch_theme, font=("Helvetica",12), bg=THEMES[self.theme]["highlight"], fg="#fff")
        self.theme_btn.grid(row=0, column=3, padx=5)

        self.search_entry = tk.Entry(root, textvariable=self.search_var, font=("Consolas",12), width=16, bg="#eaf6f6")
        self.search_entry.grid(row=1, column=0, padx=4)
        tk.Button(root, text="Search", command=self.update_view, font=("Helvetica",11), bg=THEMES[self.theme]["highlight"], fg="#fff").grid(row=1, column=1)
        self.filter_menu = tk.OptionMenu(root, self.filter_var, "All", "High", "Medium", "Low", "Today", "Overdue", "Done", "Not done", command=lambda _:self.update_view())
        self.filter_menu.config(font=("Helvetica",11), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"])
        self.filter_menu.grid(row=1, column=2)

        tk.Button(root, text="Save", command=self.save_tasks, font=("Helvetica",11), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"]).grid(row=1, column=3)
        tk.Button(root, text="Load", command=self.load_tasks, font=("Helvetica",11), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"]).grid(row=1, column=4)

        self.listbox = tk.Listbox(root, width=52, height=10, font=("Consolas",12), bg="#eaf6f6", activestyle="none")
        self.listbox.grid(row=2, column=0, columnspan=5, padx=7, pady=4)
        self.listbox.bind("<Double-Button-1>", lambda e: self.toggle_done())
        self.listbox.bind("<Delete>", lambda e: self.delete_task())
        self.listbox.bind("<Return>", lambda e: self.edit_task_dialog())

        tk.Button(root, text="Mark Done", command=self.toggle_done, font=("Helvetica",11), bg="#eeb1b1").grid(row=3, column=0)
        tk.Button(root, text="Edit", command=self.edit_task_dialog, font=("Helvetica",11), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"]).grid(row=3, column=1)
        tk.Button(root, text="Delete", command=self.delete_task, font=("Helvetica",11), bg="#eeb1b1").grid(row=3, column=2)
        tk.Button(root, text="Copy", command=self.copy_task, font=("Helvetica",11), bg=THEMES[self.theme]["btn"], fg=THEMES[self.theme]["fg"]).grid(row=3, column=3)

        self.stats_label = tk.Label(root, textvariable=self.stats_var, font=("Helvetica",12,"bold"), bg=THEMES[self.theme]["bg"], fg=THEMES[self.theme]["highlight"], anchor="w")
        self.stats_label.grid(row=4, column=0, columnspan=5, sticky="w", padx=8)
        self.update_view()
        self.update_stats()

    def switch_theme(self):
        self.theme = 1 - self.theme
        th = THEMES[self.theme]
        self.root.configure(bg=th["bg"])
        for w in self.root.winfo_children():
            if isinstance(w, tk.Label):
                w.config(bg=th["bg"], fg=th["highlight"])
            elif isinstance(w, tk.Entry):
                w.config(bg=th["entry"], fg=th["fg"])
            elif isinstance(w, tk.Button):
                w.config(bg=th["highlight"], fg="#fff")
            elif isinstance(w, tk.Listbox):
                w.config(bg="#eaf6f6")
        self.listbox.config(bg="#eaf6f6")

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        due_str = simpledialog.askstring("Due Date", "Due date (YYYY-MM-DD) or blank for none:")
        try:
            due = datetime.strptime(due_str, "%Y-%m-%d") if due_str else None
        except:
            due = None
        prio = simpledialog.askstring("Priority", "Priority (High/Medium/Low):")
        if prio not in {"High","Medium","Low"}:
            prio = "Medium"
        cat = simpledialog.askstring("Category", "Category/tag (optional):") or ""
        self.tasks.append({"text": text, "done": False, "priority": prio, "due": due, "category": cat})
        self.task_entry.delete(0, tk.END)
        self.update_view()
        self.update_stats()

    def edit_task_dialog(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        task = self.filtered_tasks()[idx]
        newtext = simpledialog.askstring("Edit Task", "Task text:", initialvalue=task["text"])
        due_str = simpledialog.askstring("Edit Due", "Due date (YYYY-MM-DD):", initialvalue=task["due"].strftime("%Y-%m-%d") if task["due"] else "")
        try:
            due = datetime.strptime(due_str, "%Y-%m-%d") if due_str else None
        except:
            due = None
        prio = simpledialog.askstring("Priority", "Edit priority:", initialvalue=task["priority"]) or "Medium"
        cat = simpledialog.askstring("Category", "Edit category/tag:", initialvalue=task["category"]) or ""
        # Find original global task
        for t in self.tasks:
            if t is task:
                t.update({"text": newtext, "due": due, "priority": prio, "category": cat})
        self.update_view()
        self.update_stats()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        task = self.filtered_tasks()[idx]
        for i, t in enumerate(self.tasks):
            if t is task:
                del self.tasks[i]
                break
        self.update_view()
        self.update_stats()

    def toggle_done(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        task = self.filtered_tasks()[idx]
        for t in self.tasks:
            if t is task:
                t["done"] = not t["done"]
        self.update_view()
        self.update_stats()

    def copy_task(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        task = self.filtered_tasks()[idx]
        text = task["text"]
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("Copied", f"Task '{text}' copied!")

    def filtered_tasks(self):
        q = self.search_var.get().strip().lower()
        f = self.filter_var.get()
        now = datetime.now()
        def test(t):
            return (q in t["text"].lower()) and (
                f=="All"
                or (f=="High" and t["priority"]=="High")
                or (f=="Medium" and t["priority"]=="Medium")
                or (f=="Low" and t["priority"]=="Low")
                or (f=="Done" and t["done"])
                or (f=="Not done" and not t["done"])
                or (f=="Today" and t["due"] and t["due"].date()==now.date())
                or (f=="Overdue" and t["due"] and t["due"]<now and not t["done"])
            )
        return [t for t in self.tasks if test(t)]

    def update_view(self):
        self.listbox.delete(0, tk.END)
        for t in self.filtered_tasks():
            tag = "[✓]" if t["done"] else "[ ]"
            prio = f'({t["priority"]})'
            due = f'[{t["due"].strftime("%Y-%m-%d")}]' if t["due"] else ""
            cat = f'#{t["category"]}' if t["category"] else ""
            line = f'{tag} {t["text"]} {prio} {due} {cat}'
            self.listbox.insert(tk.END, line)
            if t["done"]:
                self.listbox.itemconfig(tk.END, {'fg': THEMES[self.theme]["done"]})

    def update_stats(self):
        done = sum(t["done"] for t in self.tasks)
        notdone = len(self.tasks)-done
        overdue = sum(t["due"] and t["due"]<datetime.now() and not t["done"] for t in self.tasks)
        today = sum(t["due"] and t["due"].date()==datetime.now().date() for t in self.tasks)
        self.stats_var.set(f"Done: {done} | Not done: {notdone} | Overdue: {overdue} | Due today: {today}")

    def save_tasks(self):
        fname = filedialog.asksaveasfilename(defaultextension=".json")
        if fname:
            with open(fname,"w") as f:
                data = []
                for t in self.tasks:
                    j = t.copy()
                    j["due"] = j["due"].strftime("%Y-%m-%d") if j["due"] else None
                    data.append(j)
                json.dump(data, f)
            messagebox.showinfo("Saved", f"Tasks saved to {fname}")

    def load_tasks(self):
        fname = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if fname:
            with open(fname,"r") as f:
                data = json.load(f)
                self.tasks = []
                for t in data:
                    t["due"] = datetime.strptime(t["due"], "%Y-%m-%d") if t["due"] else None
                    self.tasks.append(t)
            self.update_view()
            self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
