from django.db import models

class MiUsuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Longitud suficiente para hash
    
    class Meta:
        db_table = 'tblUsuarios'




