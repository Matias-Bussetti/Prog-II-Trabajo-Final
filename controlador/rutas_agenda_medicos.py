from flask import Blueprint, jsonify, request

from modelo.agenda_medicos import (
    obtener_agenda,
    agregar_horario_agenda,
    eliminar_horario_agenda,
    modificar_horarios_agenda,
    verificar_disponibilidad,
)

from utils.functions import (
    validar_campos_del_cuerpo,
    campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable,
)

from modelo.medicos import obtener_medico_por_id

agenda_medicos_bp = Blueprint("agenda_medicos", __name__)


@agenda_medicos_bp.route("/agenda_medicos/", methods=["GET"])
def obtener_agenda_json():
    return jsonify(obtener_agenda())


@agenda_medicos_bp.route("/agenda_medicos/agregar_horario", methods=["POST"])
def agregar_horario_agenda_json():
    try:
        cuerpo = request.json

        if not request.is_json:
            return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

        campos = [
            "id_medico",
            "dia_numero",
            "hora_inicio",
            "hora_fin",
            "fecha_actualizacion",
        ]

        validacion = validar_campos_del_cuerpo(True, request.json, campos)

        if not validacion["resultado"]:
            return jsonify({"error": validacion["mensaje"]}), 400

        arreglo_de_tuplas_campo_y_tipo = [
            ("id_medico", "string"),
            ("dia_numero", "numero_de_dia_de_semana"),
            ("hora_inicio", "hora"),
            ("hora_fin", "hora"),
            ("fecha_actualizacion", "dia"),
        ]

        validacion_de_tipo_de_datos = (
            campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable(
                request.json, arreglo_de_tuplas_campo_y_tipo
            )
        )

        if not validacion_de_tipo_de_datos["resultado"]:
            return jsonify({"error": validacion_de_tipo_de_datos["mensaje"]}), 400

        medico = obtener_medico_por_id(cuerpo["id_medico"])
        if not medico:
            return jsonify({"error": "Médico no existe"}), 404

        return (
            jsonify(
                agregar_horario_agenda(
                    request.json["id_medico"],
                    request.json["dia_numero"],
                    request.json["hora_inicio"],
                    request.json["hora_fin"],
                    request.json["fecha_actualizacion"],
                )
            ),
            201,
        )
    except:
        return jsonify({"error": "Falla en el server"}), 500


@agenda_medicos_bp.route("/agenda_medicos/<string:id_medico>", methods=["PUT"])
def modificar_horarios_agenda_json(id_medico):
    # try:
    medico = obtener_medico_por_id(id_medico)
    if not medico:
        return jsonify({"error": "Médico no existe"}), 404

    cuerpo = request.json

    if not request.is_json:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

    campos = [
        "dia",
        "hora_inicio",
        "hora_fin",
    ]
    #! Validando cada agenda
    for agenda_en_cuerpo in cuerpo:
        validacion = validar_campos_del_cuerpo(True, agenda_en_cuerpo, campos)

        if not validacion["resultado"]:
            return jsonify({"error": validacion["mensaje"]}), 400

        arreglo_de_tuplas_campo_y_tipo = [
            ("dia", "numero_de_dia_de_semana"),
            ("hora_inicio", "hora"),
            ("hora_fin", "hora"),
        ]

        validacion_de_tipo_de_datos = (
            campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable(
                agenda_en_cuerpo, arreglo_de_tuplas_campo_y_tipo
            )
        )

        if not validacion_de_tipo_de_datos["resultado"]:
            return jsonify({"error": validacion_de_tipo_de_datos["mensaje"]}), 400
    #! Validando cada agenda

    return (
        jsonify(modificar_horarios_agenda(id_medico, cuerpo)),
        200,
    )


# except:
#     return jsonify({"error": "Falla en el server"}), 500


@agenda_medicos_bp.route("/agenda_medicos/<string:id_medico>", methods=["DELETE"])
def eliminar_agenda(id_medico):
    # try:
    medico = obtener_medico_por_id(id_medico)
    if not medico:
        return jsonify({"error": "Medico no existe"}), 404

    if eliminar_horario_agenda(id):
        return jsonify({"mensaje": "Se elimino la agenda del medico"}), 200
    else:
        return jsonify({"mensaje": "No se elimino la agenda del medico"}), 200


# except:
#     return jsonify({"error": "Falla en el server"}), 500
