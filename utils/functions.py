import csv


def crear_csv_con_encabezados(ruta, encabezados):
    with open(ruta, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=encabezados)
        writer.writeheader()


def exportar_lista_a_csv(ruta, campos, lista):
    with open(ruta, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()
        for elemento in lista:
            writer.writerow(elemento)


def hacer_por_cada_fila_de_csv(ruta, funcion):
    with open(ruta, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            funcion(row)


def validar_campos_del_cuerpo(tienen_que_estar, cuerpo_peticion, campos):
    campos_en_json = [campo for campo in campos if campo in cuerpo_peticion]

    if tienen_que_estar and len(campos_en_json) != len(campos):
        return {
            "resultado": False,
            "mensaje": "El formato del cuerpo de la petición no contiene los campos necesarios: "
            + ", ".join([campo for campo in campos if not campo in campos_en_json])
            + ".Necesarios: "
            + ", ".join(campos),
        }

    def campo_es_vacio_falso_o_nulo(campo):
        if str(campo) == "":
            return True

        return False

    campos_vacios_en_cuerpo = [
        campo_vacio
        for campo_vacio in campos_en_json
        if (campo_es_vacio_falso_o_nulo(cuerpo_peticion[campo_vacio]))
    ]

    if len(campos_vacios_en_cuerpo) > 0:
        return {
            "resultado": False,
            "mensaje": "Los siguiente campos se encuentran vacíos: "
            + ", ".join(campos_vacios_en_cuerpo),
        }

    return {"resultado": True, "campos": campos_en_json}


def obtener_elemento_de_lista_cuando_campo_es_igual(lista, campo, es_igual_a):
    iterador = 0
    while iterador < len(lista):
        if lista[iterador][campo] == es_igual_a:
            return lista[iterador]
        iterador += 1

    return False


def campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable(
    cuerpo_de_peticion,
    arreglo_de_tuplas_campo_y_tipo,
):
    def campo_de_la_peticion_es_del_tipo_correspondiente(campo):
        tipo = campo[1]
        llave = campo[0]
        if llave in cuerpo_de_peticion:
            if tipo == "string":
                return type(cuerpo_de_peticion[llave]) == str
            elif tipo == "int":
                return type(cuerpo_de_peticion[llave]) == int
            elif tipo == "email":
                return (
                    type(cuerpo_de_peticion[llave]) == str
                    and "@" in cuerpo_de_peticion[llave]
                )

        return True

    campos_que_fallaron_la_validacion = [
        campo
        for campo in arreglo_de_tuplas_campo_y_tipo
        if not campo_de_la_peticion_es_del_tipo_correspondiente(campo)
    ]

    def armar_mensaje_con_campos_que_falloron_la_validacion():
        print(campos_que_fallaron_la_validacion)
        return "Los siguiente campos no son del tipo correspondiente: " + ", ".join(
            [
                campo[0] + " no corresponde a => " + campo[1]
                for campo in campos_que_fallaron_la_validacion
            ]
        )

    if len(campos_que_fallaron_la_validacion) > 0:
        return {
            "resultado": False,
            "mensaje": armar_mensaje_con_campos_que_falloron_la_validacion(),
        }

    return {"resultado": True}
