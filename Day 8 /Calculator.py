import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, sympify, diff, integrate, solve, lambdify, pretty
from scipy import stats

class SciCalcPro:
    def __init__(self, root):
        self.root = root
        root.title("🔬 Ultimate SciCalc Pro")
        self.functions = {}
        self.sym_x = symbols('x')
        self.display = tk.Entry(root, font=("Consolas", 20), borderwidth=2, relief="sunken", bg="#fcf6bd", fg="#222", justify="right", width=30)
        self.display.grid(row=0, column=0, columnspan=8, pady=12, padx=2)

        self.history = tk.Listbox(root, height=4, width=50, font=("Consolas",12), bg="#dde7f0", fg="#5e6472")
        self.history.grid(row=1, column=0, columnspan=8, padx=7, pady=2)
        self.history.insert(tk.END, "Calculator History:")

        # Calculator keypad
        btns = [
            ["7", "8", "9", "/", "sin", "f(x)", "C", "diff"],
            ["4", "5", "6", "*", "cos", "store", "(", "intg"],
            ["1", "2", "3", "-", "tan", "plot2D", ")", "roots"],
            ["0", ".", "%", "+", "ln", "plot3D", "regress", "="],
        ]
        for r, row in enumerate(btns):
            for c, val in enumerate(row):
                b = tk.Button(root, text=val, font=("Helvetica",15,"bold"), width=5, height=2, bg="#bce6eb" if c < 4 else "#fae3d9", fg="#222",
                              command=lambda v=val: self.on_press(v))
                b.grid(row=2+r, column=c, padx=1, pady=1)
        # The plot/figure pane
        self.fig = plt.Figure(figsize=(4.2,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=8, padx=8, pady=7)
        # Export button
        self.export_btn = tk.Button(root, text="Export Graph", command=self.export_graph, font=("Helvetica",12), bg="#4b9cd3", fg="#fff")
        self.export_btn.grid(row=7, column=7, pady=6, sticky="e")

        # Bindings
        self.root.bind("<Return>", lambda e: self.on_press("="))
        self.root.bind("<BackSpace>", lambda e: self.on_press("←"))
        self.root.bind("<Key>", self.key_input)

    def on_press(self, val):
        # Calculator logic and symbolic/graphical enhancements
        if val == "C":
            self.display.delete(0, tk.END)
        elif val == "=":
            expr = self.display.get()
            try:
                result = eval(expr.replace("^","**"), {"__builtins__": None}, math.__dict__)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.history.insert(tk.END, f"{expr} = {result}")
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif val == "store":
            funcdef = simpledialog.askstring("Function", "Define function (e.g., f(x) = x**3+x):")
            try:
                if funcdef and "=" in funcdef:
                    lhs, rhs = map(str.strip, funcdef.split("="))
                    if lhs.startswith("f(") and lhs.endswith(")"):
                        self.functions["f"] = sympify(rhs)
                        self.history.insert(tk.END, f"Stored: f(x) = {rhs}")
            except Exception as e:
                messagebox.showerror("Invalid Function", str(e))
        elif val == "f(x)":
            if "f" in self.functions:
                xval = simpledialog.askfloat("f(x)", "x = ?")
                if xval is not None:
                    try:
                        result = self.functions["f"].subs(self.sym_x, xval)
                        self.display.delete(0, tk.END)
                        self.display.insert(tk.END, str(result))
                        self.history.insert(tk.END, f"f({xval}) = {result}")
                    except Exception:
                        self.display.delete(0, tk.END)
                        self.display.insert(tk.END, "Error")
        elif val == "plot2D":
            if "f" in self.functions:
                self.plot2d()
        elif val == "plot3D":
            if "f" in self.functions:
                self.plot3d()
        elif val == "regress":
            data = simpledialog.askstring("Regression Data", "x1,x2,... (comma); y1,y2,... (semicolon,2nd field):")
            try:
                if data and ";" in data:
                    xlist, ylist = data.split(";")
                    x = np.array(list(map(float,xlist.split(","))))
                    y = np.array(list(map(float,ylist.split(","))))
                    poly = np.polyfit(x, y, 2 if len(x) >=3 else 1)
                    fx = np.poly1d(poly)
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, f"y = {np.array2string(poly, precision=3)}")
                    self.plot_regression(x, y, fx)
                    self.history.insert(tk.END, f"Regression: {poly}")
            except Exception as e:
                messagebox.showerror("Regression error", str(e))
        elif val == "stats":
            lst = simpledialog.askstring("Stats Data", "Provide numbers comma-separated:")
            if lst:
                try:
                    nums = list(map(float, lst.split(",")))
                    out = f"Mean: {np.mean(nums):.3f} | Median: {np.median(nums):.3f} | Std: {np.std(nums):.3f}"
                    mode = stats.mode(nums, keepdims=True).mode[0]
                    out += f" | Mode: {mode:.3f}"
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, out)
                    self.history.insert(tk.END, f"Stats: {out}")
                except Exception:
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, "Error")
        elif val == "diff":
            expr = self.display.get()
            try:
                syme = sympify(expr)
                result = diff(syme, self.sym_x)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.history.insert(tk.END, f"d/dx({expr}) = {result}")
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif val == "intg":
            expr = self.display.get()
            try:
                syme = sympify(expr)
                result = integrate(syme, self.sym_x)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.history.insert(tk.END, f"∫({expr}) dx = {result}")
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif val == "roots":
            expr = self.display.get()
            try:
                syme = sympify(expr)
                result = solve(syme, self.sym_x)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.history.insert(tk.END, f"Roots({expr}) = {result}")
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, val)

    def plot2d(self):
        try:
            self.ax.clear()
            f = self.functions["f"]
            x = np.linspace(-10, 10, 400)
            fx = lambdify(self.sym_x, f, "numpy")
            y = fx(x)
            self.ax.plot(x, y, color="#fa4659")
            self.ax.set_title(f"f(x) = {f}")
            self.ax.grid(True)
            self.canvas.draw()
            self.history.insert(tk.END, f"Plotted 2D: f(x) = {f}")
        except Exception as e:
            messagebox.showerror("2D Plot error", str(e))

    def plot3d(self):
        try:
            self.canvas.get_tk_widget().grid_forget()
            fig_3d = plt.Figure(figsize=(4,3), dpi=100)
            ax3d = fig_3d.add_subplot(111, projection='3d')
            f = self.functions["f"]
            x = y = np.linspace(-5, 5, 60)
            xx, yy = np.meshgrid(x, y)
            zz = np.zeros_like(xx)
            func = lambdify((self.sym_x, symbols('y')), f, "numpy")
            for i in range(xx.shape[0]):
                for j in range(xx.shape[1]):
                    zz[i, j] = func(xx[i, j], yy[i, j])
            surf = ax3d.plot_surface(xx, yy, zz, cmap="coolwarm")
            ax3d.set_title(f"z = {f}")
            self.canvas = FigureCanvasTkAgg(fig_3d, master=self.root)
            self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=8, padx=8, pady=7)
            self.canvas.draw()
            self.history.insert(tk.END, f"Plotted 3D: f(x,y) = {f}")
        except Exception as e:
            messagebox.showerror("3D Plot error", str(e))

    def plot_regression(self, x, y, fx):
        self.ax.clear()
        self.ax.scatter(x, y, color="#fa4659", label="Data")
        xx = np.linspace(min(x), max(x), 250)
        self.ax.plot(xx, fx(xx), color="#4b9cd3", label="Fit")
        self.ax.set_title("Polynomial Regression")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def export_graph(self):
        fname = filedialog.asksaveasfilename(title="Save Graph", defaultextension=".png", filetypes=[("PNG Images", "*.png")])
        if fname:
            self.fig.savefig(fname)
            messagebox.showinfo("Saved", f"Graph saved as {fname}")

    def key_input(self, event):
        if event.char in "0123456789.+-*/()":
            self.display.insert(tk.END, event.char)
        if event.char == "^":
            self.display.insert(tk.END, "^")
        if event.char.lower() == "p":
            self.display.insert(tk.END, str(math.pi))
        if event.char.lower() == "e":
            self.display.insert(tk.END, str(math.e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SciCalcPro(root)
    root.mainloop()
