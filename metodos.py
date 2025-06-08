import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.symbols('x')

def evaluarFuncion(ecuacion, x0, decimales):
    fx = sp.lambdify(x, ecuacion, modules='numpy')
    return np.round(fx(x0), decimales)

def Error(X_nueva, X_Vieja, decimales):
    if X_nueva == 0:
        return np.inf
    error = np.abs((X_nueva - X_Vieja) / X_nueva) * 100
    return np.round(error, decimales)
def puntoFijo(ecuacion_str, x_Vieja, decimales, error_final, nIteraciones):
    lista = []
    ecuacion = sp.sympify(ecuacion_str)

    for i in range(nIteraciones):
        x_Nueva = evaluarFuncion(ecuacion, x_Vieja, decimales)
        error = Error(x_Nueva, x_Vieja, decimales)

        lista.append([round(x_Vieja, decimales), error])

        if error <= error_final:
            break  # solo sal del bucle, no grafiques aún

        x_Vieja = x_Nueva

    puntoFijoGrafica(ecuacion, lista, decimales)
    return x_Nueva, lista

def puntoFijoGrafica(ecuacion, lista, decimales):
    X0 = lista[0][0]  # Valor inicial
    x_ultimo = lista[-1][0]  # Última x evaluada
    
    y_ultimo = evaluarFuncion(ecuacion, x_ultimo, decimales)

    fig, ax = plt.subplots(figsize=(18,8))

    valoresX = np.linspace(X0 - 10, X0 + 10, 500)
    valoresY = evaluarFuncion(ecuacion, valoresX, decimales)

    # Graficar F(x)
    ax.plot(valoresX, valoresY, label="F(x)")

    # Punto rojo en la última aproximación
    ax.plot(x_ultimo, y_ultimo, 'ro', label=f'Último punto ({x_ultimo}, {y_ultimo})')

    ax.set_title("Gráfica de f(x)")
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.grid(True)
    ax.axhline(y=0, color='black', linestyle='--')
    ax.axvline(x=0, color='black', linestyle='--')

    # Leyenda en la esquina superior derecha
    ax.legend(loc='upper right')

    # Guardar como archivo SVG
    plt.tight_layout()
    plt.savefig("static/metodos/grafica_punto_fijo.svg", format='svg')





