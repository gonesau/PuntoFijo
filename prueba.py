import math
import sympy as sp

def punto_fijo(g, x0, tol, max_iter=100):
    """
    g: función de iteración
    x0: valor inicial
    tol: tolerancia
    max_iter: número máximo de iteraciones
    """
    x = x0
    for i in range(max_iter):
        x_nuevo = g(x)
        if abs(x_nuevo - x) < tol:
            return x_nuevo, i
        x = x_nuevo
    return None, max_iter

# Solicitar al usuario que ingrese la ecuación, el valor inicial y la tolerancia
ecuacion = input("Por favor, ingrese la ecuación de iteración (use 'x' como la variable): ")
x0 = float(input("Por favor, ingrese el valor inicial: "))
tol = float(input("Por favor, ingrese la tolerancia: "))

# Convertir la ecuación del usuario en una función de Python
x = sp.symbols('x')
g = sp.lambdify(x, sp.sympify(ecuacion), "math")

# Ejecutar el método de punto fijo
raiz, num_iter = punto_fijo(g, x0, tol)

# Imprimir el resultado
if raiz is not None:
    print(f"La raíz es {raiz} y se encontró en {num_iter} iteraciones.")
else:
    print(f"No se encontró una raíz después de {num_iter} iteraciones.")