from flask import Blueprint, jsonify, request

from modelo.turnos import (
    crear_turno,
    obtener_turno_por_id,
    obtener_turnos_de_medico_con_id_igual_a,
    obtener_turnos_de_paciente_con_id_igual_a,
    eliminar_turno_por_id,
)
from modelo.medicos import obtener_medico_por_id
from modelo.pacientes import obtener_paciente_por_id
from modelo.agenda_medicos import obtener_agenda_medico_por_id

from utils.functions import (
    validar_campos_del_cuerpo,
    campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable,
)
from utils.funciones_para_fechas import (
    fecha_y_horario_son_validos_para_una_lista_de_horarios,
    devolver_hora_mas_15_minutos_en_string,
    fecha_y_hora_se_superpone_con_un_turno_dentro_de_una_lista_de_turnos,
)

turnos_bp = Blueprint("turnos", __name__)


# * TEST * --------------------------
# def obtener_agenda_medico_por_id(id):
#     return [
#         {
#             "dia_numero": "1",
#             "hora_inicio": "8:00",
#             "hora_fin": "10:00",
#             "id_medico": "707ec1f9-e503-4858-b4d3-eb187eefebcb",
#             "fecha_actualizacion": "2023/11/5",
#         },
#         {
#             "dia_numero": "3",
#             "hora_inicio": "18:00",
#             "hora_fin": "21:00",
#             "id_medico": "707ec1f9-e503-4858-b4d3-eb187eefebcb",
#             "fecha_actualizacion": "2023/11/5",
#         },
#         {
#             "dia_numero": "6",
#             "hora_inicio": "4:00",
#             "hora_fin": "16:00",
#             "id_medico": "707ec1f9-e503-4858-b4d3-eb187eefebcb",
#             "fecha_actualizacion": "2023/11/5",
#         },
#     ]


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

    arreglo_de_tuplas_campo_y_tipo = [
        ("id_medico", "string"),
        ("id_paciente", "string"),
        ("hora_turno", "hora_de_turno"),
        ("fecha_solicitud", "dia"),
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

    paciente = obtener_paciente_por_id(cuerpo["id_paciente"])
    if not paciente:
        return jsonify({"error": "Paciente no existe"}), 404

    horarios_disponibles_del_medico = obtener_agenda_medico_por_id(cuerpo["id_medico"])

    if not fecha_y_horario_son_validos_para_una_lista_de_horarios(
        horarios_disponibles_del_medico,
        cuerpo["fecha_solicitud"],
        cuerpo["hora_turno"],
        devolver_hora_mas_15_minutos_en_string(cuerpo["hora_turno"]),
    ):
        return jsonify({"error": "el horario no esta disponible"}), 406

    # print(obtener_turnos_de_medico_con_id_igual_a(cuerpo["id_medico"]))
    if fecha_y_hora_se_superpone_con_un_turno_dentro_de_una_lista_de_turnos(
        obtener_turnos_de_medico_con_id_igual_a(cuerpo["id_medico"]),
        cuerpo["fecha_solicitud"],
        cuerpo["hora_turno"],
    ):
        return (
            jsonify({"error": "El turno a pedir se superpone con otro"}),
            201,
        )

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
    paciente = obtener_paciente_por_id(id_paciente)
    if not paciente:
        return jsonify({"error": "Paciente no existe"}), 404
    return jsonify(obtener_turnos_de_paciente_con_id_igual_a(id_paciente)), 200


@turnos_bp.route("/turnos/medico/<string:id_medico>", methods=["GET"])
def obtener_turnos_de_medico(id_medico):
    medico = obtener_medico_por_id(id_medico)
    if not medico:
        return jsonify({"error": "Médico no existe"}), 404

    return jsonify(obtener_turnos_de_medico_con_id_igual_a(id_medico)), 200


@turnos_bp.route("/turnos/<string:id>", methods=["DELETE"])
def eliminar_turno(id):
    turno = obtener_turno_por_id(id)
    if not turno:
        return jsonify({"error": "Turno no existe"}), 404

    return jsonify(eliminar_turno_por_id(id)), 200
