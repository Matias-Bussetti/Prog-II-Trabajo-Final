import csv
from flask import jsonify


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


def validar_json_y_campos_del_cuerpo(es_json, cuerpo_peticion, campos):
    if not es_json:
        return {"resultado": False, "mensaje": "El formato de la solicitud no es JSON"}

    campos_en_json = [campo for campo in campos if campo in cuerpo_peticion]

    if len(campos_en_json) != len(campos):
        return {
            "resultado": False,
            "mensaje": "El formato del cuerpo de la petición no contiene los campos necesarios: "
            + ", ".join(cuerpo_peticion)
            + ".Necesarios: "
            + ", ".join(campos),
        }

    # TODO: Agregar validación de que no esten vacíos
    # TODO: esto no funca :(
    campos_vacios_en_json = [
        campo_vacio for campo_vacio in cuerpo_peticion if (len(campo_vacio) == 0)
    ]

    if len(campos_vacios_en_json) > 0:
        return {
            "resultado": False,
            "mensaje": "Los siguiente campos se encuentran vacíos: "
            + ", ".join(campos_vacios_en_json),
        }

    return {"resultado": True}
