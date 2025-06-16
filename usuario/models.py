from django.db import models
from accounts.models import MiUsuario

class HistorialPuntoFijo(models.Model):
    usuario = models.ForeignKey(MiUsuario, on_delete=models.CASCADE, db_column='usuario_id')
    funcion = models.CharField(max_length=255)
    x0 = models.FloatField()
    n_iteraciones = models.IntegerField()
    decimales = models.IntegerField()
    error_final = models.FloatField()
    resultado_final = models.FloatField()  # este es el correcto
    error_Calculado = models.FloatField(default=0.0)
    fecha = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'tblHistorialPuntoFijo'

    def __str__(self):
        return f"{self.usuario.user} - {self.funcion} ({self.fecha})"
    
class Iteracion(models.Model):
    ejercicio = models.ForeignKey(HistorialPuntoFijo, on_delete=models.CASCADE, related_name='iteraciones')
    numero_iteracion = models.IntegerField()
    x_anterior = models.FloatField()
    x_nueva = models.FloatField()
    error = models.FloatField()

    class Meta:
        db_table = 'tblIteracionesPuntoFijo'

