import re
from django.shortcuts import render, redirect
from accounts.models import MiUsuario
from metodos import puntoFijo, IntegralNumerica
from usuario.models import HistorialPuntoFijo, Iteracion, HistorialMetodo2, ValoresMetodo2
import sympy as sp

def inicio_usuario(request):
    nombre = request.session.get('usuario_nombre', None, )
    

    if not nombre:
        return redirect('inicio_landing')

    return render(request, 'usuario/index.html', {
    'modo': 'usuario',
    'nombre': nombre})

def usuario_metodo1(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')

    resultado = None
    iteraciones = []
    funcion = ''
    x0 = 0
    decimales = 6
    error_final = 0.1
    nIteraciones = 10
    porcentajeError = 0
    error_Calculado = 0
    errores = []

    if request.method == 'POST':
        funcion = request.POST.get('funcion')
        x0_str = request.POST.get('x0')
        nIteraciones_str = request.POST.get('nIteraciones')
        decimales_str = request.POST.get('decimales')
        error_final_str = request.POST.get('error_final')

        # Validar que solo contenga caracteres matemáticos
        if not funcion or funcion.strip() == "":
            errores.append("La función g(x) no puede estar vacía.")
        else:
            try:
                sp.sympify(funcion)
            except (sp.SympifyError, SyntaxError):
                errores.append("La función ingresada no es válida. Usa notación válida como: exp(x), sin(x), x**2, etc.")

        # Validaciones numéricas
        try:
            x0 = float(x0_str)
        except (ValueError, TypeError):
            errores.append("x₀ debe ser un número válido.")

        try:
            nIteraciones = int(nIteraciones_str)
            if not (2 <= nIteraciones <= 25):
                errores.append("Las iteraciones deben estar entre 2 y 25.")
        except (ValueError, TypeError):
            errores.append("Iteraciones debe ser un número entero.")

        try:
            decimales = int(decimales_str)
            if not (2 <= decimales <= 10):
                errores.append("Los decimales deben estar entre 2 y 10.")
        except (ValueError, TypeError):
            errores.append("Decimales debe ser un número entero.")

        try:
            error_final = float(error_final_str.replace(",", "."))
            if error_final <= 0:
                errores.append("El error final debe ser mayor a 0.")
        except (ValueError, TypeError):
            errores.append("Error final debe ser un número válido.")

        # Si no hay errores, ejecutar el método
        if not errores:
            try:
                resultado, iteraciones, error_Calculado = puntoFijo(funcion, x0, decimales, error_final, nIteraciones)

                usuario = MiUsuario.objects.get(id=request.session['usuario_id'])

                historial = HistorialPuntoFijo.objects.create(
                    usuario=usuario,
                    funcion=funcion,
                    x0=x0,
                    n_iteraciones=nIteraciones,
                    decimales=decimales,
                    error_final=error_final,
                    resultado_final=resultado,
                    error_Calculado=error_Calculado
                )

                for i, it in enumerate(iteraciones, start=1):
                    Iteracion.objects.create(
                        ejercicio=historial,
                        numero_iteracion=i,
                        x_anterior=iteraciones[i - 1][0] if i > 1 else x0,
                        x_nueva=it[0],
                        error=it[1]
                    )

                if iteraciones:
                    porcentajeError = iteraciones[-1][1]

            except Exception as e:
                errores.append(f"Error en el cálculo: {str(e)}")

    return render(request, 'usuario/punto-fijo.html', {
        'modo': 'usuario',
        'resultado': resultado,
        'iteraciones': iteraciones,
        'funcion': funcion,
        'x0': x0,
        'decimales': decimales,
        'error_final': error_final,
        'error': porcentajeError,
        'nIteraciones': nIteraciones,
        'error_Calculado': error_Calculado,
        'errores': errores
    })

def usuario_metodo2(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')
    
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
    valor_t = 0
    errores = []
    
    if request.method == 'POST':
        funcion = request.POST.get('funcion')

        if not funcion or funcion.strip() == "":
            errores.append("La función g(x) no puede estar vacía.")
        else:
            try:
                sp.sympify(funcion)
            except (sp.SympifyError, SyntaxError):
                errores.append("La función ingresada no es válida. Usa notación válida como: exp(x), sin(x), x**2, etc.")
        
        try:
            limite_a = float(request.POST.get('limite_a'))
        except (ValueError, TypeError):
            errores.append("el limite inferior no es valido.")
            
        try:
            limite_b = float(request.POST.get('limite_b'))
        except (ValueError, TypeError):
            errores.append("el limite superior no es valido.")
        
        try:
            valor_t = int(request.POST.get('valor_t'))
            if not (2 <= valor_t <= 25):
                errores.append("Las los segmentos no pueden ser mayores a 25 ni menores de 2.")
        except (ValueError, TypeError):
            errores.append("Los segmentos deben ser un número entero.")
        
        try:
            decimales = int(request.POST.get('deci_v'))
            if not (2 <= decimales <= 10):
                errores.append("Los decimales deben estar entre 2 y 10.")
        except (ValueError, TypeError):
            errores.append("Decimales debe ser un número entero.")
        
        if not errores:
            try:
                limite_a = float(request.POST.get('limite_a'))
                limite_b = float(request.POST.get('limite_b'))
                valor_t = int(request.POST.get('valor_t'))

                AreaI, AreaT, AreaTC, valores, errorT, errorTC, valor_t = IntegralNumerica(funcion, decimales, limite_a, limite_b, valor_t)

                usuario = MiUsuario.objects.get(id=request.session['usuario_id'])
                
                historial = HistorialMetodo2.objects.create(
                    usuario=usuario,
                    funcion=funcion,
                    AreaI=AreaI,
                    AreaT=AreaT,
                    AreaTC=AreaTC,
                    errorT = errorT,
                    errorTC=errorTC,
                    n_espacios=valor_t,
                    decimales= decimales
                )
                
                for i, it in enumerate(valores, start=1):
                    ValoresMetodo2.objects.create(
                        ejercicio=historial,
                        valorF=valores[i],
                        valorH=valoresH[i]
                    )

            except Exception as e:
                errores.append(f"Error en el cálculo: {str(e)}")

    return render(request, 'landing/metodo2.html', {
        'modo': 'usuario',
        'AreaI': AreaI,
        'AreaT': AreaT,
        'AreaTC': AreaTC,
        'errorT': errorT,
        'errorTC': errorTC,
        'funcion': funcion,
        'limite_a': limite_a,
        'limite_b': limite_b,
        'valor_t': valor_t,
        'valores': valores,
        'errores': errores
    })

def usuario_documentacion(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')
    return render(request, 'usuario/documentacion.html', {'modo': 'usuario'})

def usuario_perfil(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')

    usuario = MiUsuario.objects.get(id=request.session['usuario_id'])
    historial = HistorialPuntoFijo.objects.filter(usuario=usuario).prefetch_related('iteraciones').order_by('-fecha')
    histoM = HistorialMetodo2.objects.filter(usuario=usuario).prefetch_related('valores').order_by('-fecha')

    return render(request, 'usuario/perfil.html', {
        'modo': 'usuario',
        'usuario': usuario,
        'historial': historial,
        'histoM': histoM
    })


def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de sesión
    return redirect('inicio_landing')  

