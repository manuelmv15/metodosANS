from django.db import models
from accounts.models import MiUsuario


class HistorialPuntoFijo(models.Model):
    usuario = models.ForeignKey(MiUsuario, on_delete=models.CASCADE, db_column='usuario_id')
    funcion = models.CharField(max_length=255)
    x0 = models.FloatField()
    n_iteraciones = models.IntegerField()
    decimales = models.IntegerField()
    error_final = models.FloatField(null=True)
    resultado_final = models.FloatField(null=True)
    error_Calculado = models.FloatField(default=0.0)
    fecha = models.DateTimeField(auto_now_add=True)

    imagen = models.ImageField(upload_to='imagenes_punto_fijo/', null=True, blank=True)  

    class Meta:
        db_table = 'tblHistorialPuntoFijo'

    def __str__(self):
        return f"{self.usuario.user} - {self.funcion} ({self.fecha})"

    
class Iteracion(models.Model):
    ejercicio = models.ForeignKey(HistorialPuntoFijo, on_delete=models.CASCADE, related_name='iteraciones')
    numero_iteracion = models.IntegerField()
    x_anterior = models.FloatField()
    x_nueva = models.FloatField()
    error = models.FloatField(null=True)  # ✅ Esto permite guardar None


    class Meta:
        db_table = 'tblIteracionesPuntoFijo'

class HistorialMetodo2(models.Model):
    usuario = models.ForeignKey(MiUsuario, on_delete=models.CASCADE, db_column='usuario_id')
    funcion = models.CharField(max_length=255)
    AreaI = models.FloatField()
    AreaT = models.FloatField()
    AreaTC = models.FloatField()
    errorT = models.FloatField()
    errorTC = models.FloatField()
    n_espacios = models.IntegerField()
    decimales = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tblHistorialMetodo2'

    def __str__(self):
        return f"{self.usuario.user} - {self.funcion} ({self.fecha})"

class ValoresMetodo2(models.Model):
    ejercicio = models.ForeignKey(HistorialMetodo2, on_delete=models.CASCADE, related_name='valores')
    valorF = models.FloatField()
    valorH = models.FloatField()

    class Meta:
        db_table = 'tblValoresMetodo2'
