from django.shortcuts import render
from django.shortcuts import render, redirect
from metodos import puntoFijo, IntegralNumerica



def landing_index(request):
    return render(request, 'landing/index.html', {'modo': 'landing'})

def landing_metodo1(request):
    resultado = None
    iteraciones = []
    funcion = ''
    x0 = 0
    decimales = 4
    error_final = 0.01
    nIteraciones = 10
    porcentajeError = 0

    if request.method == 'POST':
        funcion = request.POST.get('funcion')

        if not funcion or funcion.strip() == "":
            resultado = "Por favor, ingresa una ecuación válida en g(x)."
        else:
            try:
                x0 = float(request.POST.get('x0'))
                error_final = float(request.POST.get('error_final'))

                resultado, iteraciones = puntoFijo(funcion, x0, decimales, error_final, nIteraciones)

                if iteraciones:
                    porcentajeError = iteraciones[-1][1]

            except Exception as e:
                resultado = f"Error: {str(e)}"

    return render(request, 'landing/punto-fijo.html', {
        'modo': 'landing',
        'resultado': resultado,
        'iteraciones': iteraciones,
        'funcion': funcion,
        'x0': x0,
        'decimales': decimales,
        'error_final': error_final,
        'error': porcentajeError,
        'nIteraciones': nIteraciones
    })


def landing_metodo2(request):
    AreaI = 0.0
    AreaT = 0.0
    AreaTC = 0.0
    valores = []
    valoresH = []
    funcion = ''
    limite_a = 0.0
    limite_b = 0.0
    decimales = 4
    errorT = 0.0
    errorTC = 0.0
    
    if request.method == 'POST':
        funcion = request.POST.get('funcion')

        if not funcion or funcion.strip() == "":
            AreaI = "Por favor, ingresa una ecuación válida en g(x)."
        else:
            try:
                limite_a = float(request.POST.get('limite_a'))
                limite_b = float(request.POST.get('limite_b'))
                valor_t = int(request.POST.get('valor_t'))

                AreaI, AreaT, AreaTC, valores, valoresH, errorT, errorTC = IntegralNumerica(funcion, decimales, limite_a, limite_b, valor_t)

            except Exception as e:
                AreaI = f"Error: {str(e)}"

    return render(request, 'landing/metodo2.html', {
        'modo': 'landing',
        'AreaI': AreaI,
        'AreaT': AreaT,
        'AreaTC': AreaTC,
        'errorT': errorT,
        'errorTC': errorTC,
        'funcion': funcion,
    })

def landing_documentacion(request):
    return render(request, 'landing/documentacion.html', {'modo': 'landing'})

