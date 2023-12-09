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


def validar_campos_del_cuerpo(tienen_que_estar, cuerpo_peticion, campos):
    campos_en_json = [campo for campo in campos if campo in cuerpo_peticion]

    if tienen_que_estar and len(campos_en_json) != len(campos):
        print("asd")
        return {
            "resultado": False,
            "mensaje": "El formato del cuerpo de la petición no contiene los campos necesarios: "
            + ", ".join(cuerpo_peticion)
            + ".Necesarios: "
            + ", ".join(campos),
        }

    # TODO: Agregar validación de que no esten vacíos
    # TODO: esto no funca :(
    # campos_vacios_en_json = [
    #     campo_vacio for campo_vacio in campos_en_json if (len(campo_vacio) == 0)
    # ]

    # if len(campos_vacios_en_json) > 0:
    #     return {
    #         "resultado": False,
    #         "mensaje": "Los siguiente campos se encuentran vacíos: "
    #         + ", ".join(campos_vacios_en_json),
    #     }

    return {"resultado": True, "campos": campos_en_json}
