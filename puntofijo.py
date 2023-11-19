import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sympy

def punto_fijo(g, x0, tol, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_nuevo = g(x)
        if abs(x_nuevo - x) < tol:
            return x_nuevo, i
        x = x_nuevo
    return None, max_iter

class PuntoFijoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Método de Punto Fijo")

        # Cambios en el nombre de las etiquetas y las entradas

        self.label_ecuacion_f = ttk.Label(master, text="F(x):")
        self.label_ecuacion_f.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_ecuacion_f = ttk.Entry(master, width=30)
        self.entry_ecuacion_f.grid(row=0, column=1, padx=10, pady=5)

        self.label_ecuacion_g = ttk.Label(master, text="Ecuación G(x):")
        self.label_ecuacion_g.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_ecuacion_g = ttk.Entry(master, width=30)
        self.entry_ecuacion_g.grid(row=1, column=1, padx=10, pady=5)


        self.label_valor_inicial = ttk.Label(master, text="Valor Inicial:")
        self.label_valor_inicial.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_valor_inicial = ttk.Entry(master)
        self.entry_valor_inicial.grid(row=2, column=1, padx=10, pady=5)

        self.label_tolerancia = ttk.Label(master, text="Tolerancia:")
        self.label_tolerancia.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_tolerancia = ttk.Entry(master)
        self.entry_tolerancia.grid(row=3, column=1, padx=10, pady=5)

        self.btn_calcular = ttk.Button(master, text="Calcular", command=self.calcular_punto_fijo)
        self.btn_calcular.grid(row=4, column=0, padx=5, pady=10, sticky=tk.E)

        self.btn_limpiar = ttk.Button(master, text="Limpiar", command=self.limpiar)
        self.btn_limpiar.grid(row=4, column=1, padx=5, pady=10, sticky=tk.W)

        self.label_resultado = ttk.Label(master, text="La raíz de la ecuación es:")
        self.label_resultado.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_resultado = ttk.Entry(master, state='readonly')
        self.entry_resultado.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

        self.table_frame = ttk.Frame(master)
        self.table_frame.grid(row=6, column=0, columnspan=2, pady=10)
        self.tree = ttk.Treeview(self.table_frame, columns=('Iteración', 'Xi', 'G(x)', 'Tolerancia'), show='headings')
        self.tree.heading('Iteración', text='Iteración')
        self.tree.heading('Xi', text='Xi')
        self.tree.heading('G(x)', text='G(x)')
        self.tree.heading('Tolerancia', text='Tolerancia')
        self.tree.pack(side='left', fill='both')

        self.fig, self.ax = plt.subplots(figsize=(6, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def calcular_punto_fijo(self):
        ecuacion_g_texto = self.entry_ecuacion_g.get()
        ecuacion_f_texto = self.entry_ecuacion_f.get()
        valor_inicial = float(self.entry_valor_inicial.get())
        tolerancia = float(self.entry_tolerancia.get())

        x = sympy.symbols('x')
        ecuacion_g = sympy.sympify(ecuacion_g_texto)
        ecuacion_f = sympy.sympify(ecuacion_f_texto)

        g_lambda = sympy.lambdify(x, ecuacion_g, 'numpy')
        g = lambda x: g_lambda(x)

        raiz, niter = punto_fijo(g, valor_inicial, tolerancia)

        iteraciones, valores, tolerancias = self.punto_fijo(g_lambda, valor_inicial, tolerancia)

        self.entry_resultado.config(state='normal')
        self.entry_resultado.delete(0, tk.END)
        if raiz is not None:
            self.entry_resultado.insert(0, f"{raiz:.6f}")
        else:
            self.entry_resultado.insert(0, "No convergió")
        self.entry_resultado.config(state='readonly')

        self.actualizar_grafico(ecuacion_f, valores)
        self.actualizar_tabla(iteraciones, valores, tolerancias)

    def punto_fijo(self, g, x0, tol, max_iter=100):
        iteraciones = []
        valores = []
        tolerancias = []

        for i in range(max_iter):
            x1 = g(x0)
            iteraciones.append(i + 1)
            valores.append(x0)
            tolerancias.append(abs(x1 - x0))

            if abs(x1 - x0) < tol:
                break

            x0 = x1
        else:
            iteraciones.extend(range(len(iteraciones) + 1, max_iter + 1))
            valores.extend([None] * (max_iter - len(iteraciones) + 1))
            tolerancias.extend([None] * (max_iter - len(iteraciones) + 1))

        return iteraciones, valores, tolerancias

    def actualizar_grafico(self, ecuacion_f, valores):
        self.ax.clear()
        x_vals = np.linspace(min(valores) - 1, max(valores) + 1, 100)
        y_vals = [ecuacion_f.evalf(subs={'x': val}) for val in x_vals]
        self.ax.plot(x_vals, y_vals, label="Ecuación F(x)")
        self.ax.scatter(valores[-1], 0, color='red', label="Raíz")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def actualizar_tabla(self, iteraciones, valores, tolerancias):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for i, (valor, tolerancia) in enumerate(zip(valores, tolerancias), 1):
            self.tree.insert('', 'end', values=(i, valor, valores[i] if i < len(valores) else None, tolerancia))

    def limpiar(self):
        self.entry_ecuacion_g.delete(0, tk.END)
        self.entry_ecuacion_f.delete(0, tk.END)
        self.entry_valor_inicial.delete(0, tk.END)
        self.entry_tolerancia.delete(0, tk.END)
        self.entry_resultado.config(state='normal')
        self.entry_resultado.delete(0, tk.END)
        self.entry_resultado.config(state='readonly')

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.ax.clear()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoFijoApp(root)
    root.mainloop()
