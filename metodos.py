from sympy import integrate, Abs
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.symbols('x')

def evaluarFuncion(ecuacion, x0, decimales):
    fx = sp.lambdify(x, ecuacion, modules='numpy')
    return np.round(fx(x0), decimales)

def Error(X_nueva, X_Vieja, decimales):
    
    if np.isclose(X_nueva, 0.0, atol=1e-12):
        return float('inf')  # o un valor alto, para no detener el método prematuramente
    error = np.abs((X_nueva - X_Vieja) / X_nueva) * 100
    return np.round(error, decimales)




def puntoFijo(ecuacion_str, x_Vieja, decimales, error_final, nIteraciones):
    lista = []
    ecuacion = sp.sympify(ecuacion_str)
    error = 0.0

    for i in range(nIteraciones):
        x_Nueva = evaluarFuncion(ecuacion, x_Vieja, decimales)

        error = Error(x_Nueva, x_Vieja, decimales)

        if not np.isfinite(error):
            error = None

        if not np.isfinite(x_Nueva) or abs(x_Nueva) > 1e6:
            lista.append([None, None])
            break  # salimos si x_Nueva es inválido

        lista.append([round(x_Vieja, decimales), error])

        if error is not None and error <= error_final:
            break

        x_Vieja = x_Nueva

    print("ITERACIONES:")
    for fila in lista:
        print(fila)

    puntoFijoGrafica(ecuacion, lista, decimales)
    return x_Vieja, lista


def puntoFijoGrafica(ecuacion, lista, decimales):
    if not lista or lista[0][0] is None or lista[-1][0] is None:
        return
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







def IntegralNumerica(f, deci, a, b, tama):
    
    fff = sp.sympify(f)
    
    AreaI = round(integrate(fff, (x, a, b) ).evalf(), deci)
    
    fa = fff.subs(x, a)
    fb = fff.subs(x, b)
    
    AreaT = round((b-a)*((fa + fb)/2), deci)
    
    h = (b - a)/tama

    valores = [tama+1]
    
    for i in range(tama+1):
        valores.append([fff.subs(x, a+(h*i)), a+(h*i)])
        
    if valores.size > 2:
        resto = np.sum(valores[np.arange(1,tama)][0])
    
    AreaTC = round((b-a)*((fa+fb+2*resto)/(2*tama)), deci)#Area trapecio compuesta
    
    errorT = round(Abs((AreaI - AreaT) / AreaI) * 100, deci)
    errorTC = round(Abs((AreaI - AreaTC) / AreaI) * 100, deci)
    
    GraficarITC(a, b, valores, tama)
    
    return AreaI, AreaT, AreaTC, valores, errorT, errorTC, tama

def GraficarITC(a, b, valores, tama):
    plt.rcParams.update({'font.size': 20})
    
    fig, ax = plt.subplots(figsize=(18,8))
    
    vH, vF = [tama+1], [tama+1]
    
    for i in range(tama+1):
        vH.append(valores[1][i])
        vF.append(valores[i][0])

    ax.fill_between(vH, vF, label="F(x)")
    ax.grid(True)

    ax.set_title("Gráfica de f(x)", fontsize=24)
    ax.set_xlabel("x", fontsize=20)
    ax.set_ylabel("F(x)")
    
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig("static/metodos/grafica_integral_numerica.svg", format='svg')
