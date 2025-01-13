from django.contrib import messages
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def editar_contenido(request):
    json_path = "static/data/contenido.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar.html", {"contenido": {}})

    if request.method == "POST":
        try:
            # Eliminar la última tarjeta si se ha solicitado
            eliminar_tarjeta_id = request.POST.get("eliminar_tarjeta")
            if eliminar_tarjeta_id == 'last' and len(data["tarjetas"]) > 0:
                # Eliminar la última tarjeta
                data["tarjetas"].pop()
                messages.success(request, "Última tarjeta eliminada con éxito.")
            elif eliminar_tarjeta_id == 'last':
                messages.error(request, "No hay tarjetas para eliminar.")

            # Actualizar las tarjetas existentes
            tarjetas_existentes = len(data["tarjetas"])
            for idx in range(tarjetas_existentes):
                titulo = request.POST.get(f"titulo_{idx}", data["tarjetas"][idx]["titulo"])
                descripcion = request.POST.get(f"descripcion_{idx}", data["tarjetas"][idx]["descripcion"])

                # Actualizamos el título y la descripción
                data["tarjetas"][idx]["titulo"] = titulo
                data["tarjetas"][idx]["descripcion"] = descripcion

                # Procesamos la imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/INFORMACION_FERSAN/tarjeta_{idx+1}.png"

                    with open(ruta_imagen, "wb") as img_file:
                        for chunk in imagen.chunks():
                            img_file.write(chunk)

                    data["tarjetas"][idx]["imagen"] = ruta_imagen

            # Agregar nuevas tarjetas si hay datos
            nuevas_tarjetas = []
            for key in request.POST.keys():
                if key.startswith("titulo_") and int(key.split("_")[1]) >= tarjetas_existentes:
                    idx = int(key.split("_")[1])
                    titulo = request.POST.get(f"titulo_{idx}", "")
                    descripcion = request.POST.get(f"descripcion_{idx}", "")
                    imagen_key = f"imagen_{idx}"

                    nueva_tarjeta = {
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "imagen": ""
                    }

                    # Manejar imagen de nuevas tarjetas
                    if imagen_key in request.FILES:
                        imagen = request.FILES[imagen_key]
                        ruta_imagen = f"static/images/tarjeta{idx+1}.png"

                        with open(ruta_imagen, "wb") as img_file:
                            for chunk in imagen.chunks():
                                img_file.write(chunk)

                        nueva_tarjeta["imagen"] = ruta_imagen

                    nuevas_tarjetas.append(nueva_tarjeta)

            # Agregar nuevas tarjetas al JSON
            data["tarjetas"].extend(nuevas_tarjetas)

            # Limpiar las rutas de las imágenes (opcional)
            for tarjeta in data["tarjetas"]:
                tarjeta["imagen"] = tarjeta["imagen"].replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            messages.success(request, "Los cambios se realizaron con éxito.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")

        return render(request, "editar.html", {"contenido": data})

    return render(request, "editar.html", {"contenido": data})


@csrf_exempt
def editar_notas(request):
    json_path = "static/data/notes.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_n.html", {"notes": {}})

    if request.method == "POST":
        try:
            # Eliminar la última nota si se solicita
            eliminar_nota_id = request.POST.get("eliminar_nota")
            if eliminar_nota_id == 'last' and len(data["notas"]) > 0:
                # Eliminar la última nota
                data["notas"].pop()
                messages.success(request, "Última nota eliminada con éxito.")
            elif eliminar_nota_id == 'last':
                messages.error(request, "No hay notas para eliminar.")

            # Actualizar las notas existentes
            notas_existentes = len(data["notas"])
            for idx in range(notas_existentes):
                titulo = request.POST.get(f"titulo_{idx}", data["notas"][idx].get("titulo", ""))
                descripcion = request.POST.get(f"descripcion_{idx}", data["notas"][idx].get("descripcion", ""))
                enlace = request.POST.get(f"enlace_{idx}", data["notas"][idx].get("enlace", ""))

                # Actualizamos los campos
                data["notas"][idx]["titulo"] = titulo
                data["notas"][idx]["descripcion"] = descripcion
                data["notas"][idx]["enlace"] = enlace

                # Procesar la imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/Notas/nota_{idx + 1}.png"

                    with open(ruta_imagen, "wb") as img_file:
                        for chunk in imagen.chunks():
                            img_file.write(chunk)

                    data["notas"][idx]["imagen"] = ruta_imagen.replace("static/", "")  # Guardar ruta relativa

            # Agregar nuevas notas si hay datos en los campos
            nuevas_notas = []
            for key in request.POST.keys():
                if key.startswith("titulo_") and int(key.split("_")[1]) >= notas_existentes:
                    idx = int(key.split("_")[1])
                    titulo = request.POST.get(f"titulo_{idx}", "")
                    descripcion = request.POST.get(f"descripcion_{idx}", "")
                    enlace = request.POST.get(f"enlace_{idx}", "")
                    imagen_key = f"imagen_{idx}"

                    nueva_nota = {
                        "titulo": titulo,
                        "descripcion": descripcion,
                        "enlace": enlace,
                        "imagen": ""
                    }

                    # Procesar imagen si se envió una nueva
                    if imagen_key in request.FILES:
                        imagen = request.FILES[imagen_key]
                        ruta_imagen = f"static/images/nota_{idx + 1}.png"

                        with open(ruta_imagen, "wb") as img_file:
                            for chunk in imagen.chunks():
                                img_file.write(chunk)

                        nueva_nota["imagen"] = ruta_imagen.replace("static/", "")  # Guardar ruta relativa

                    nuevas_notas.append(nueva_nota)

            # Agregar nuevas notas al JSON
            data["notas"].extend(nuevas_notas)

            # Limpiar las rutas de las imágenes (opcional)
            for nota in data["notas"]:
                nota["imagen"] = nota["imagen"].replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            # Mensaje de éxito
            messages.success(request, "Los cambios se realizaron con éxito.")
        except Exception as e:
            # Manejo de errores
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")

        return render(request, "editar_n.html", {"notes": data})

    return render(request, "editar_n.html", {"notes": data})

""" Agencias------------------------------------------------------------------------------------------------------------ """

@csrf_exempt
def editar_vw(request):
    json_path = "static/data/vw.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_vw.html", {"vw": {"vw_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["vw_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_vw_{idx + 1}.png"

                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)

                    agencia["logo"] = ruta_logo.replace("static/", "")  # Guardar ruta relativa

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/vw_{idx + 1}.png"

                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)

                    agencia["imagen"] = ruta_imagen.replace("static/", "")  # Guardar ruta relativa

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            # Limpiar las rutas de las imágenes (opcional)
            for nota in data["vw_info"]:
                nota["imagen"] = nota["imagen"].replace("static/", "")

            messages.success(request, "Los cambios se realizaron con éxito.")
        except Exception as e:
            # Manejo de errores
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")

        return render(request, "editar_vw.html", {"vw": {"vw_info": data["vw_info"]}})

    # Renderizar la página con los datos existentes
    return render(request, "editar_vw.html", {"vw": {"vw_info": data["vw_info"]}})



@csrf_exempt
def editar_suzuki(request):
    json_path = "static/data/suzuki.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_suzuki.html", {"vw": {"suzuki_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["suzuki_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_suzuki_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/suzuki_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_suzuki.html", {"suzuki": {"suzuki_info": data["suzuki_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_suzuki.html", {"suzuki": {"suzuki_info": data["suzuki_info"]}})



@csrf_exempt
def editar_harley(request):
    json_path = "static/data/harley.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_harley.html", {"vw": {"harley_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["harley_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_harley_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/harley_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_harley.html", {"harley": {"harley_info": data["harley_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_harley.html", {"harley": {"harley_info": data["harley_info"]}})


@csrf_exempt
def editar_omoda(request):
    json_path = "static/data/omoda.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_omoda.html", {"vw": {"omoda_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["omoda_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_omoda_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/omoda_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_omoda.html", {"omoda": {"omoda_info": data["omoda_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_omoda.html", {"omoda": {"omoda_info": data["omoda_info"]}})



@csrf_exempt
def editar_seat(request):
    json_path = "static/data/seat.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_seat.html", {"vw": {"seat_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["seat_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_seat_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/seat_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_seat.html", {"seat": {"seat_info": data["seat_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_seat.html", {"seat": {"seat_info": data["seat_info"]}})


@csrf_exempt
def editar_sev(request):
    json_path = "static/data/sev.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_sev.html", {"vw": {"sev_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["sev_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_sev_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/sev_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_sev.html", {"sev": {"sev_info": data["sev_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_sev.html", {"sev": {"sev_info": data["sev_info"]}})


@csrf_exempt
def editar_zeekr(request):
    json_path = "static/data/zeekr.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_zeekr.html", {"vw": {"zeekr_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["zeekr_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_zeekr_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/zeekr_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_zeekr.html", {"zeekr": {"zeekr_info": data["zeekr_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_zeekr.html", {"zeekr": {"zeekr_info": data["zeekr_info"]}})



@csrf_exempt
def editar_chirey(request):
    json_path = "static/data/chirey.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_chirey.html", {"vw": {"chirey_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["chirey_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_chirey_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/chirey_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_chirey.html", {"chirey": {"chirey_info": data["chirey_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_chirey.html", {"chirey": {"chirey_info": data["chirey_info"]}})


@csrf_exempt
def editar_motor(request):
    json_path = "static/data/motor.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        # Si ocurre un error al leer el archivo JSON
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_motor.html", {"vw": {"motor_info": []}})

    if request.method == "POST":
        try:
            # Actualizar datos existentes
            for idx, agencia in enumerate(data["motor_info"]):
                agencia["lugar"] = request.POST.get(f"lugar_{idx}", agencia["lugar"])
                agencia["concecionario"] = request.POST.get(f"concecionario_{idx}", agencia["concecionario"])
                agencia["direccion"] = request.POST.get(f"direccion_{idx}", agencia["direccion"])
                agencia["enlace"] = request.POST.get(f"enlace_{idx}", agencia["enlace"])
                agencia["telefono"] = request.POST.get(f"telefono_{idx}", agencia["telefono"])

                # Procesar logo si se actualiza
                logo_key = f"logo_{idx}"
                if logo_key in request.FILES:
                    logo = request.FILES[logo_key]
                    ruta_logo = f"static/images/LOGO_SUCURSAL/logo_motor_{idx + 1}.png"
                    with open(ruta_logo, "wb") as logo_file:
                        for chunk in logo.chunks():
                            logo_file.write(chunk)
                    agencia["logo"] = ruta_logo.replace("static/", "")

                # Procesar imagen si se actualiza
                imagen_key = f"imagen_{idx}"
                if imagen_key in request.FILES:
                    imagen = request.FILES[imagen_key]
                    ruta_imagen = f"static/images/motor_{idx + 1}.png"
                    with open(ruta_imagen, "wb") as imagen_file:
                        for chunk in imagen.chunks():
                            imagen_file.write(chunk)
                    agencia["imagen"] = ruta_imagen.replace("static/", "")

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            messages.success(request, "Los cambios se realizaron con éxito.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")
            return render(request, "editar_motor.html", {"motor": {"motor_info": data["motor_info"]}})  

    # Renderizar la página con los datos existentes
    return render(request, "editar_motor.html", {"motor": {"motor_info": data["motor_info"]}})


@csrf_exempt
def editar_horarios(request):
    json_path = "static/data/horarios.json"

    try:
        # Leer el archivo JSON
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_horarios.html", {"hora": {}})

    if request.method == "POST":
        try:
            # Eliminar la última tarjeta si se ha solicitado
            eliminar_tarjeta_id = request.POST.get("eliminar_tarjeta")
            if eliminar_tarjeta_id == 'last' and len(data["pie_horarios"]) > 0:
                # Eliminar la última tarjeta
                data["pie_horarios"].pop()  # Elimina la última tarjeta
                messages.success(request, "Última tarjeta eliminada con éxito.")
            elif eliminar_tarjeta_id == 'last':
                messages.error(request, "No hay tarjetas para eliminar.")

            # Actualizar las tarjetas existentes
            tarjetas_existentes = len(data["pie_horarios"])
            for idx in range(tarjetas_existentes):
                departamento = request.POST.get(f"departamento_{idx}", data["pie_horarios"][idx]["departamento"])
                horarios = request.POST.get(f"horarios_{idx}", data["pie_horarios"][idx]["horarios"])

                # Actualizamos los datos
                data["pie_horarios"][idx]["departamento"] = departamento
                data["pie_horarios"][idx]["horarios"] = horarios

            # Agregar nuevas tarjetas si hay datos
            nuevas_tarjetas = []
            for key in request.POST.keys():
                if key.startswith("departamento_") and int(key.split("_")[1]) >= tarjetas_existentes:
                    idx = int(key.split("_")[1])
                    departamento = request.POST.get(f"departamento_{idx}", "")
                    horarios = request.POST.get(f"horarios_{idx}", "")

                    nueva_tarjeta = {
                        "departamento": departamento,
                        "horarios": horarios,
                    }

                    nuevas_tarjetas.append(nueva_tarjeta)

            # Agregar nuevas tarjetas al JSON
            data["pie_horarios"].extend(nuevas_tarjetas)

            # Guardar los cambios en el archivo JSON
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            messages.success(request, "Los cambios se realizaron con éxito.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")

        return render(request, "editar_horarios.html", {"hora": data})

    return render(request, "editar_horarios.html", {"hora": data})



@csrf_exempt
def editar_ubicacion(request):
    json_path = "static/data/ubicacion.json"

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
        return render(request, "editar_ubicacion.html", {"ubicacion": {}})

    if request.method == "POST":
        try:
            eliminar_tarjeta_id = request.POST.get("eliminar_tarjeta")
            if eliminar_tarjeta_id == 'last':
                if len(data["pie_ubicacion"]) > 0:
                    data["pie_ubicacion"].pop()
                    messages.success(request, "Última tarjeta eliminada con éxito.")
                else:
                    messages.error(request, "No hay tarjetas para eliminar.")

            for idx in range(len(data["pie_ubicacion"])):
                encabezado = request.POST.get(f"encabezado_{idx}", data["pie_ubicacion"][idx]["encabezado"])
                direccion = request.POST.get(f"direccion_{idx}", data["pie_ubicacion"][idx]["direccion"])
                telefono = request.POST.get(f"telefono_{idx}", data["pie_ubicacion"][idx]["telefono"])

                data["pie_ubicacion"][idx]["encabezado"] = encabezado
                data["pie_ubicacion"][idx]["direccion"] = direccion
                data["pie_ubicacion"][idx]["telefono"] = telefono

            nuevas_tarjetas = []
            for key in request.POST.keys():
                if key.startswith("encabezado_") and int(key.split("_")[1]) >= len(data["pie_ubicacion"]):
                    idx = int(key.split("_")[1])
                    encabezado = request.POST.get(f"encabezado_{idx}", "")
                    direccion = request.POST.get(f"direccion_{idx}", "")
                    telefono = request.POST.get(f"telefono_{idx}", "")

                    if encabezado.strip() and direccion.strip() and telefono.strip():
                        nuevas_tarjetas.append({
                            "encabezado": encabezado,
                            "direccion": direccion,
                            "telefono": telefono,
                        })

            data["pie_ubicacion"].extend(nuevas_tarjetas)

            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            messages.success(request, "Los cambios se realizaron con éxito.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar los cambios: {str(e)}")

        return render(request, "editar_ubicacion.html", {"ubicacion": data})

    return render(request, "editar_ubicacion.html", {"ubicacion": data})