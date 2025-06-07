from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_index, name='inicio_landing'),
    path('metodo1/', views.landing_metodo1, name='metodo1_landing'),
    path('metodo2/', views.landing_metodo2, name='metodo2_landing'),
    path('documentacion/', views.landing_documentacion, name='documentacion_landing'),
]

