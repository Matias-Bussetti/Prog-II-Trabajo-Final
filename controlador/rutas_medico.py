from flask import Blueprint, jsonify, request

from modelo.medicos import (
    obtener_medicos,
    crear_medico,
    obtener_medico_por_id,
    editar_medico_por_id,
    inhabilitar_medico_por_id,
)
from utils.functions import validar_campos_del_cuerpo

medicos_bp = Blueprint("medicos", __name__)


@medicos_bp.route("/medicos/", methods=["GET"])
def obtener_medicos_json():
    return jsonify(obtener_medicos())


@medicos_bp.route("/medicos", methods=["POST"])
def crear_medicos_json():
    if not request.is_json:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

    campos = [
        "nombre",
        "apellido",
        "dni",
        "telefono",
        "email",
        "matricula",
    ]

    validacion = validar_campos_del_cuerpo(True, request.json, campos)

    if not validacion["resultado"]:
        return jsonify({"error": validacion["mensaje"]}), 400

    # TODO: Crear medicos
    # TODO Comprobar Que se Cree Bien XD
    return (
        jsonify(
            crear_medico(
                request.json["nombre"],
                request.json["apellido"],
                request.json["dni"],
                request.json["telefono"],
                request.json["email"],
                request.json["matricula"],
            )
        ),
        201,
    )


@medicos_bp.route("/medicos/<string:id>", methods=["GET"])
def obtener_info_de_medico(id):
    # TODO comprobar id nulo o vacío
    medico = obtener_medico_por_id(id)
    if not medico:
        return jsonify({"error": "Médico no existe"}), 404

    return jsonify(medico), 200


@medicos_bp.route("/medicos/inhabilitar/<string:id>", methods=["PUT"])
def inhabilitar_medico(id):
    medico = obtener_medico_por_id(id)
    if not medico:
        return jsonify({"error": "Médico no existe"}), 404

    return jsonify(inhabilitar_medico_por_id(id)), 200


@medicos_bp.route("/medicos/<string:id>", methods=["PUT"])
def actualizar_medico_json(id):
    if not request.is_json:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

    medico = obtener_medico_por_id(id)
    if not medico:
        return jsonify({"error": "Médico no existe"}), 404

    campos = [
        "nombre",
        "apellido",
        "dni",
        "telefono",
        "email",
        "matricula",
    ]

    validacion = validar_campos_del_cuerpo(False, request.json, campos)

    if not validacion["resultado"]:
        return jsonify({"error": validacion["mensaje"]}), 400

    # TODO: Crear medicos
    # TODO Comprobar Que se Cree Bien XD
    return (
        jsonify(editar_medico_por_id(id, validacion["campos"], request.json)),
        200,
    )
