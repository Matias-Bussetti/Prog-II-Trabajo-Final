from flask import Blueprint, jsonify, request

from modelo.turnos import (
    crear_turno,
    obtener_turno_por_id,
    obtener_turnos_de_medico_con_id_igual_a,
    obtener_turnos_de_paciente_con_id_igual_a,
    eliminar_turno_por_id,
)
from modelo.medicos import obtener_medico_por_id


from utils.functions import validar_campos_del_cuerpo
from utils.funciones_para_fechas import (
    fecha_y_horario_son_validos_para_una_lista_de_horarios,
    devolver_hora_mas_15_minutos_en_string,
)

turnos_bp = Blueprint("turnos", __name__)


# * TEST * --------------------------
def obtener_agenda_medico_por_id(id):
    return [
        {
            "dia_numero": "1",
            "hora_inicio": "8:00",
            "hora_fin": "10:00",
            "id_medico": "707ec1f9-e503-4858-b4d3-eb187eefebcb",
            "fecha_actualizacion": "2023/11/5",
        },
        {
            "dia_numero": "3",
            "hora_inicio": "18:00",
            "hora_fin": "21:00",
            "id_medico": "707ec1f9-e503-4858-b4d3-eb187eefebcb",
            "fecha_actualizacion": "2023/11/5",
        },
        {
            "dia_numero": "6",
            "hora_inicio": "4:00",
            "hora_fin": "6:00",
            "id_medico": "707ec1f9-e503-4858-b4d3-eb187eefebcb",
            "fecha_actualizacion": "2023/11/5",
        },
    ]


# * TEST * --------------------------


@turnos_bp.route("/turnos", methods=["POST"])
def crear_turnos_json():
    if not request.is_json:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

    cuerpo = request.json
    campos = [
        "id_medico",
        "id_paciente",
        "hora_turno",
        "fecha_solicitud",
    ]

    validacion = validar_campos_del_cuerpo(True, cuerpo, campos)

    if not validacion["resultado"]:
        return jsonify({"error": validacion["mensaje"]}), 400

    medico = obtener_medico_por_id(cuerpo["id_medico"])
    if not medico:
        return jsonify({"error": "Médico no existe"}), 404

    horarios_disponibles_del_medico = obtener_agenda_medico_por_id(cuerpo["id_medico"])

    if not fecha_y_horario_son_validos_para_una_lista_de_horarios(
        horarios_disponibles_del_medico,
        cuerpo["fecha_solicitud"],
        cuerpo["hora_turno"],
        devolver_hora_mas_15_minutos_en_string(cuerpo["hora_turno"]),
    ):
        return jsonify({"error": "el horario no esta disponible"}), 406

    # TODO: Comprobar que el paciente existe
    # TODO: Comprobar que no se pise con otros horarios
    # TODO: Crear Turno

    return (
        jsonify(
            crear_turno(
                cuerpo["id_medico"],
                cuerpo["id_paciente"],
                cuerpo["hora_turno"],
                cuerpo["fecha_solicitud"],
            )
        ),
        201,
    )


@turnos_bp.route("/turnos/paciente/<string:id_paciente>", methods=["GET"])
def obtener_turnos_de_paciente(id_paciente):
    # TODO comprobar id nulo o vacío
    return jsonify(obtener_turnos_de_paciente_con_id_igual_a(id_paciente)), 200


@turnos_bp.route("/turnos/medico/<string:id_medico>", methods=["GET"])
def obtener_turnos_de_medico(id_medico):
    # TODO comprobar id nulo o vacío
    return jsonify(obtener_turnos_de_medico_con_id_igual_a(id_medico)), 200


# ? -------------- HACIENDO
@turnos_bp.route("/turnos/<string:id>", methods=["DELETE"])
def eliminar_turno(id):
    # TODO: Compobar que exista
    turno = obtener_turno_por_id(id)
    if not turno:
        return jsonify({"error": "Turno no existe"}), 404

    return jsonify(eliminar_turno_por_id(id)), 200


# ? -------------- HACIENDO
