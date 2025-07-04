from django.shortcuts import render
from django.shortcuts import render, redirect
from metodos import puntoFijo, IntegralNumerica
import numpy as np
from accounts.models import MiUsuario
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import connection


def landing_index(request):
    return render(request, 'landing/index.html', {'modo': 'landing'})

def landing_metodo1(request):
    resultado = None
    iteraciones = []
    funcion = ''
    x0 = 0
    decimales = 4
    error_final = 0.01
    nIteraciones = 15
    porcentajeError = 0
    errores = []
    no_converge = False  # NUEVA BANDERA

    if request.method == 'POST':
        funcion = request.POST.get('funcion')
        x0_str = request.POST.get('x0')
        error_final_str = request.POST.get('error_final')

        # Validaciones
        if not funcion or funcion.strip() == "":
            errores.append("Debe ingresar una función g(x).")

        try:
            x0 = float(x0_str)
        except (ValueError, TypeError):
            errores.append("x₀ debe ser un número válido.")

        try:
            error_final = float(error_final_str.replace(",", "."))
            if error_final <= 0:
                errores.append("El error final debe ser mayor a 0.")
        except (ValueError, TypeError):
            errores.append("El error final debe ser un número válido.")

        if not errores:
            try:
                resultado, iteraciones = puntoFijo(funcion, x0, decimales, error_final, nIteraciones)

                if not np.isfinite(resultado):
                    errores.append("El método no converge con el valor inicial dado.")
                elif iteraciones and (iteraciones[-1][1] is None or not np.isfinite(iteraciones[-1][1])):
                    errores.append("El método no converge o el error calculado es inválido.")
                else:
                    porcentajeError = iteraciones[-1][1]

            except Exception as e:
                errores.append(f"Error durante el cálculo: {str(e)}")


    return render(request, 'landing/punto-fijo.html', {
        'modo': 'landing',
        'resultado': None if no_converge else resultado,
        'iteraciones': iteraciones,
        'funcion': funcion,
        'x0': x0,
        'decimales': decimales,
        'error_final': error_final,
        'error': porcentajeError,
        'nIteraciones': nIteraciones,
        'errores': errores,
        'no_converge': no_converge  
    })

def landing_metodo2(request):
    AreaI = 0.0
    AreaT = 0.0
    AreaTC = 0.0
    valores = []
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
        if not errores:
            try:
                limite_a = float(request.POST.get('limite_a'))
                limite_b = float(request.POST.get('limite_b'))
                valor_t = int(request.POST.get('valor_t'))

                AreaI, AreaT, AreaTC, valores, errorT, errorTC, valor_t = IntegralNumerica(funcion, decimales, limite_a, limite_b, valor_t)

            except Exception as e:
                errores.append(f"Error durante el cálculo: {str(e)}")

    return render(request, 'landing/metodo2.html', {
        'modo': 'landing',
        'AreaI': AreaI,
        'AreaT': AreaT,
        'AreaTC': AreaTC,
        'errorT': errorT,
        'errorTC': errorTC,
        'funcion': funcion,
        'limite_a': limite_a,
        'limite_b': limite_b,
        'valor_t': valor_t,
        'valores':valores
    })

def landing_documentacion(request):
    return render(request, 'landing/documentacion.html', {'modo': 'landing'})

def login(request): 
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')

        try:
            usuario = MiUsuario.objects.get(user=username)

            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                return redirect('inicio_usuario')
            else:
                raise MiUsuario.DoesNotExist()

        except MiUsuario.DoesNotExist:
            return render(request, 'accounts/login.html', {
                'error': 'Credenciales inválidas'
            })

    return render(request, 'accounts/login.html', {'modo': 'landing'})

def registro(request): 
    if request.method == 'POST':
        nombre = request.POST['nombre']
        user = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']

        # Verificar si ya existe el usuario o email
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM tblUsuarios WHERE user = %s OR email = %s", [user, email])
            count = cursor.fetchone()[0]
        
        if count > 0:
            return render(request, 'accounts/registro.html', {
                'error': 'Ya existe un usuario con ese correo o nombre de usuario.'
            })

        # Encriptar la contraseña
        hashed_password = make_password(password)

        # Insertar en la base de datos
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tblUsuarios (nombre, email, user, password)
                VALUES (%s, %s, %s, %s)
            """, [nombre, email, user, hashed_password])

        # Obtener al usuario y guardar en sesión
        usuario = MiUsuario.objects.get(user=user)
        request.session['usuario_id'] = usuario.id
        request.session['usuario_nombre'] = usuario.nombre

        return redirect('inicio_usuario')

    return render(request, 'accounts/registro.html',{'modo': 'landing'})
