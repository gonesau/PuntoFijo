import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sympy

class PuntoFijoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Método de Punto Fijo")

        self.label_ecuacion = ttk.Label(master, text="Ecuación:")
        self.label_ecuacion.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_ecuacion = ttk.Entry(master, width=30)
        self.entry_ecuacion.grid(row=0, column=1, padx=10, pady=5)

        self.label_valor_inicial = ttk.Label(master, text="Valor Inicial:")
        self.label_valor_inicial.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_valor_inicial = ttk.Entry(master)
        self.entry_valor_inicial.grid(row=1, column=1, padx=10, pady=5)

        self.label_tolerancia = ttk.Label(master, text="Tolerancia:")
        self.label_tolerancia.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry_tolerancia = ttk.Entry(master)
        self.entry_tolerancia.grid(row=2, column=1, padx=10, pady=5)

        self.btn_calcular = ttk.Button(master, text="Calcular", command=self.calcular_punto_fijo)
        self.btn_calcular.grid(row=3, column=0, columnspan=2, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.table_frame = ttk.Frame(master)
        self.table_frame.grid(row=5, column=0, columnspan=2, pady=10)
        self.tree = ttk.Treeview(self.table_frame, columns=('Iteración', 'Valor'), show='headings')
        self.tree.heading('Iteración', text='Iteración')
        self.tree.heading('Valor', text='Valor')
        self.tree.pack(side='left', fill='both')

    def calcular_punto_fijo(self):
        ecuacion_texto = self.entry_ecuacion.get()
        valor_inicial = float(self.entry_valor_inicial.get())
        tolerancia = float(self.entry_tolerancia.get())

        x = sympy.symbols('x')
        ecuacion = sympy.sympify(ecuacion_texto)

        iteraciones, valores = self.punto_fijo(ecuacion, valor_inicial, tolerancia)

        self.actualizar_grafico(ecuacion, valores)
        self.actualizar_tabla(iteraciones, valores)

    def punto_fijo(self, ecuacion, x0, tolerancia, max_iter=100):
        iteraciones = []
        valores = []

        x = sympy.symbols('x')

        # Convertir ecuacion a función lambda para evaluarla en x0
        ecuacion_lambda = sympy.lambdify(x, ecuacion, 'numpy')
        for i in range(max_iter):
            x1 = ecuacion_lambda(x0)
            iteraciones.append(i + 1)
            valores.append(x1)

            if abs(x1 - x0) < tolerancia:
                break

            x0 = x1

        return iteraciones, valores

    def actualizar_grafico(self, ecuacion, valores):
        self.ax.clear()
        x_vals = np.linspace(min(valores) - 1, max(valores) + 1, 100)
        y_vals = [ecuacion.evalf(subs={'x': val}) for val in x_vals]
        self.ax.plot(x_vals, y_vals, label="Ecuación")
        self.ax.scatter(valores[-1], ecuacion.evalf(subs={'x': valores[-1]}), color='red', label="Raíz")

        self.ax.legend()
        self.canvas.draw()

    def actualizar_tabla(self, iteraciones, valores):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for i, valor in zip(iteraciones, valores):
            self.tree.insert('', 'end', values=(i, valor))

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoFijoApp(root)
    root.mainloop()
