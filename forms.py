from django import forms
from django.contrib.auth.models import User
from accounts.models import MiUsuario


#QUIERO AGRADECER DESDE LO MÁS PROFUNDO DE MI CORAZÓN A https://www.youtube.com/watch?v=N6jzspc2kds&t=2614s
#POR PERMITIRME ESTE LOGRO

class editarPerfilFM(forms.ModelForm):
    class Meta:
        model = MiUsuario
        fields = ('nombre', 'email', 'user', 'password')
        labels = {
            'nombre': 'Nombre',
            'email': 'Email',
            'user': 'User',
            'password': 'contraseña',
        }
    
    def __init__(self, *args, **kwargs):
        super(editarPerfilFM, self).__init__(*args, **kwargs)
    pass