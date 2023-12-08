from flask import Blueprint, jsonify, request

from modelo.pacientes import (
    obtener_pacientes,
    crear_paciente,
    obtener_paciente_por_id,
    editar_paciente_por_id,
    eliminar_paciente_por_id,
)
from utils.functions import validar_campos_del_cuerpo

pacientes_bp = Blueprint("pacientes", __name__)


@pacientes_bp.route("/pacientes/", methods=["GET"])
def obtener_pacientes_json():
    return jsonify(obtener_pacientes())


@pacientes_bp.route("/pacientes", methods=["POST"])
def crear_pacientes_json():
    if not request.is_json:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

    campos = [
        "nombre",
        "apellido",
        "dni",
        "telefono",
        "email",
        "direccion_calle",
        "direccion_numero",
    ]

    validacion = validar_campos_del_cuerpo(True, request.json, campos)

    if not validacion["resultado"]:
        return jsonify({"error": validacion["mensaje"]}), 400

    # TODO: Crear pacientes
    # TODO Comprobar Que se Cree Bien XD
    return (
        jsonify(
            crear_paciente(
                request.json["nombre"],
                request.json["apellido"],
                request.json["dni"],
                request.json["telefono"],
                request.json["email"],
                request.json["direccion_calle"],
                request.json["direccion_numero"],
            )
        ),
        201,
    )


@pacientes_bp.route("/pacientes/<string:id>", methods=["GET"])
def obtener_info_de_paciente(id):
    # TODO comprobar id nulo o vacío
    return jsonify(obtener_paciente_por_id(id)), 200


@pacientes_bp.route("/pacientes/<string:id>", methods=["DELETE"])
def eliminar_paciente(id):
    # TODO: Compobar que exista
    return jsonify(eliminar_paciente_por_id(id)), 200


@pacientes_bp.route("/pacientes/<string:id>", methods=["PUT"])
def actualizar_paciente_json(id):
    if not request.is_json:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

    campos = [
        "dni",
        "nombre",
        "apellido",
        "telefono",
        "email",
        "direccion_calle",
        "direccion_numero",
    ]

    validacion = validar_campos_del_cuerpo(False, request.json, campos)

    if not validacion["resultado"]:
        return jsonify({"error": validacion["mensaje"]}), 400

    # TODO: Crear pacientes
    # TODO Comprobar Que se Cree Bien XD
    return (
        jsonify(editar_paciente_por_id(id, validacion["campos"], request.json)),
        200,
    )
