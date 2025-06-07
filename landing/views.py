from django.shortcuts import render
from django.shortcuts import render, redirect



def landing_index(request):
    return render(request, 'landing/index.html', {'modo': 'landing'})

def landing_metodo1(request):
    return render(request, 'landing/punto-fijo.html', {'modo': 'landing'})

def landing_metodo2(request):
    return render(request, 'landing/metodo2.html', {'modo': 'landing'})

def landing_documentacion(request):
    return render(request, 'landing/documentacion.html', {'modo': 'landing'})

