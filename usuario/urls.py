from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_usuario, name='inicio_usuario'),
    path('metodo1/', views.usuario_metodo1, name='metodo1_usuario'),
    path('metodo2/', views.usuario_metodo2, name='metodo2_usuario'),
    path('documentacion/', views.usuario_documentacion, name='documentacion_usuario'),
    path('perfil/', views.usuario_perfil, name='perfil'),
]