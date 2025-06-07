from django.shortcuts import render, redirect

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
    return render(request, 'usuario/punto-fijo.html', {'modo': 'usuario'})  # o cambia si el archivo se llama diferente

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

