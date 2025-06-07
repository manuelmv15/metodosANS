from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from accounts import views
from django.db import connection
from accounts.models import MiUsuario
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password
from accounts.models import MiUsuario

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

    return render(request, 'accounts/registro.html')


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

    return render(request, 'accounts/login.html')