import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

from sympy import integrate

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



def IntegralNumerica(f, deci, valores, valoresH, a, b, tama):
    
    ff = sp.sympify(f)
    
    fff = sp.Lambda(x, ff)
    
    fa = fff(a)
    fb = fff(b)
    
    AreaT = np.round((b-a)*((fa + fb)/2), deci)#Trapecio Simple
    
    broaaaa = float(integrate(fff, (x, a, b) ).evalf())
    
    AreaI = np.round(broaaaa, deci)#Evaluar integral
    
    h = (b - a)/tama

    valores = np.zeros(tama+1)
    valoresH = np.zeros(tama+1)
    
    for i in range(tama+1):
        valores[i] = fff(a+(h*i))
        valoresH[i] = a+(h*i)
        
    if valores.size > 2:
        resto = np.sum(valores[np.arange(1,tama)])
    
    AreaTC = np.round((b-a)*((fa+fb+2*resto)/(2*tama)), deci)#Area trapecio compuesta
    
    errorT = Error(AreaT, AreaI, deci)
    errorTC = Error(AreaTC, AreaI, deci)
    
    GraficarITC(a, b, valores, tama)
    
    return AreaI, AreaT, AreaTC

def GraficarITC(a, b, valores, tama):
    fig, ax = plt.subplots()

    arr = np.linspace(a,b,tama+1)

    plt.plot(arr, valores)

    plt.savefig("static/metodos/grafica_integral_numerica.svg", format='svg')
