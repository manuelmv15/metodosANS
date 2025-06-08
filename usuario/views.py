from django.shortcuts import render, redirect
from accounts.models import MiUsuario
from metodos import puntoFijo
from usuario.models import HistorialPuntoFijo,Iteracion

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

    if request.method == 'POST':
        funcion = request.POST.get('funcion')

        if not funcion or funcion.strip() == "":
            resultado = "Por favor, ingresa una ecuación válida en g(x)."
        else:
            try:
                x0 = float(request.POST.get('x0'))
                nIteraciones = int(request.POST.get('nIteraciones'))
                decimales = int(request.POST.get('decimales'))
                error_final = float(request.POST.get('error_final'))

                resultado, iteraciones = puntoFijo(funcion, x0, decimales, error_final, nIteraciones)
                
                usuario = MiUsuario.objects.get(id=request.session['usuario_id'])

                historial = HistorialPuntoFijo.objects.create(
                    usuario=usuario,
                    funcion=funcion,
                    x0=x0,
                    n_iteraciones=nIteraciones,
                    decimales=decimales,
                    error_final=error_final,
                    resultado_final=resultado
                )

                for i, it in enumerate(iteraciones, start=1):
                    Iteracion.objects.create(
                    ejercicio=historial,
                    numero_iteracion=i,
                    x_anterior=iteraciones[i - 1][0] if i > 1 else x0,  # x anterior
                    x_nueva=it[0],  # x nueva
                    error=it[1]
                    )
                
                if iteraciones:
                    porcentajeError = iteraciones[-1][1]
            except Exception as e:
                resultado = f"Error: {str(e)}"
    
    return render(request, 'usuario/punto-fijo.html', {
        'modo': 'usuario',
        'resultado': resultado,
        'iteraciones': iteraciones,
        'funcion': funcion,
        'x0': x0,
        'decimales': decimales,
        'error_final': error_final,
        'error': porcentajeError,
        'nIteraciones': nIteraciones
    })

    
    
    # o cambia si el archivo se llama diferente

def usuario_metodo2(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')
    return render(request, 'usuario/metodo2.html', {'modo': 'usuario'})

def usuario_documentacion(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')
    return render(request, 'usuario/documentacion.html', {'modo': 'usuario'})

def usuario_perfil(request):
    if 'usuario_id' not in request.session:
        return redirect('vista_invitado')
    nombre = request.session['usuario_nombre']
    return render(request, 'usuario/perfil.html', {'nombre': nombre,'modo': 'usuario'})

def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de sesión
    return redirect('inicio_landing')  

