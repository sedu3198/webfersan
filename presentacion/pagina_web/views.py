from django.shortcuts import render, redirect
from django import forms
from .models import CitaServicio    
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def menu_hamburguesa(request):
    return render(request, 'components\menu_hamburguesa.html')

def pie_de_pagina(request):
    return render(request, 'components\pie_de_pagina.html')

def interfaz_modificar(request):
    return render(request, 'components\interfaz_modificar.html')

def marcas(request):
    return render(request, 'pagina\marcas.html')

def home(request):
    contenido_path = "static/data/contenido.json"  # Ruta del archivo contenido.json
    notas_path = "static/data/notes.json"  # Ruta del archivo notes.json

    try:
        # Leer contenido.json
        with open(contenido_path, "r", encoding="utf-8") as contenido_file:
            contenido_data = json.load(contenido_file)
        
        # Leer notes.json
        with open(notas_path, "r", encoding="utf-8") as notas_file:
            notas_data = json.load(notas_file)
        
        # Enviar ambos conjuntos de datos a la plantilla
        print(f"Datos enviados a la plantilla: contenido={contenido_data}, notas={notas_data}")  # Depuración
        return render(request, "pagina/home.html", {"contenido": contenido_data, "notas": notas_data})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/home.html", {"contenido": {"tarjetas": []}, "notas": {"notas": []}})

@login_required
def inicio_usuario(request):
    return render(request, 'pagina/inicio_usuario.html')

@login_required
def registro(request):
    return render(request, 'pagina/inicio_usuario.html')  # Muestra el formulario de login 

def salir(request):
    logout(request)
    return redirect('/')


def marcas(request):
    return render(request, 'pagina/marcas.html')

def acerca_empresa(request):
    return render(request, 'pagina/acerca_empresa.html')

def atencion_al_cliente(request):
    return render(request, 'pagina/atencion_al_cliente.html')

def localizador_agencias(request):
    return render(request, 'pagina/localizador_agencias.html')

def volkswagen(request):
    vw_path = "static/data/vw.json"  # Ruta del archivo vw.json

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(vw_path, "r", encoding="utf-8") as vw_file:
            vw_data = json.load(vw_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: vw_volkswagen={vw_data}")  # Depuración
        return render(request, "pagina/volkswagen.html", {"vw": vw_data})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/volkswagen.html", {"vw": {"vw_info": []}})

def suzuki(request):
    suzuki_path = "static/data/suzuki.json"  # Ruta del archivo vw.json

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(suzuki_path, "r", encoding="utf-8") as suzuki_file:
            suzuki_info = json.load(suzuki_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: suzuki={suzuki_info}")  # Depuración
        return render(request, "pagina/suzuki.html", {"suzuki": suzuki_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/suzuki.html", {"suzuki": {"suzuki_info": []}})

def harley(request):
    harley_path = "static/data/harley.json"  # Ruta del archivo vw.json

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(harley_path, "r", encoding="utf-8") as harley_file:
            harley_data = json.load(harley_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: vw_volkswagen={harley_data}")  # Depuración
        return render(request, "pagina/harley.html", {"harley": harley_data})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/harley.html", {"harley": {"harley_info": []}})

def seat(request):
    seat_path = "static/data/seat.json" 

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(seat_path, "r", encoding="utf-8") as seat_file:
            seat_info = json.load(seat_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: seat={seat_info}")  # Depuración
        return render(request, "pagina/seat.html", {"seat": seat_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/seat.html", {"seat": {"seat_info": []}})

def omoda(request):
    omoda_path = "static/data/omoda.json" 

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(omoda_path, "r", encoding="utf-8") as omoda_file:
            omoda_info = json.load(omoda_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: omoda={omoda_info}")  # Depuración
        return render(request, "pagina/omoda.html", {"omoda": omoda_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/omoda.html", {"omoda": {"omoda_info": []}})

def sev(request):
    sev_path = "static/data/sev.json" 

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(sev_path, "r", encoding="utf-8") as sev_file:
            sev_info = json.load(sev_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: sev={sev_info}")  # Depuración
        return render(request, "pagina/sev.html", {"sev": sev_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/sev.html", {"sev": {"sev_info": []}})

def zeekr(request):
    zeekr_path = "static/data/zeekr.json" 

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(zeekr_path, "r", encoding="utf-8") as zeekr_file:
            zeekr_info = json.load(zeekr_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: zeekr={zeekr_info}")  # Depuración
        return render(request, "pagina/zeekr.html", {"zeekr": zeekr_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/zeekr.html", {"zeekr": {"zeekr_info": []}})

def chirey(request):
    chirey_path = "static/data/chirey.json" 

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(chirey_path, "r", encoding="utf-8") as chirey_file:
            chirey_info = json.load(chirey_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: chirey={chirey_info}")  # Depuración
        return render(request, "pagina/chirey.html", {"chirey": chirey_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/chirey.html", {"chirey": {"chirey_info": []}})
    
def motornation(request):
    motor_path = "static/data/motor.json" 

    try:
        # Leer el archivo JSON con codificación UTF-8 para asegurar la correcta lectura de caracteres especiales
        with open(motor_path, "r", encoding="utf-8") as motor_file:
            motor_info = json.load(motor_file)
        
        # Enviar los datos a la plantilla
        print(f"Datos enviados a la plantilla: motor={motor_info}")  # Depuración
        return render(request, "pagina/motornation.html", {"motor": motor_info})

    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        # Enviar datos vacíos en caso de error
        return render(request, "pagina/motornation.html", {"motor": {"motor_info": []}})

