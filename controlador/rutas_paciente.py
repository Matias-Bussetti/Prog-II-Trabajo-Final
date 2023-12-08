from flask import Blueprint, jsonify, request

from modelo.pacientes import obtener_pacientes, crear_paciente
from utils.functions import validar_json_y_campos_del_cuerpo

pacientes_bp = Blueprint("pacientes", __name__)


@pacientes_bp.route("/pacientes/", methods=["GET"])
def obtener_pacientes_json():
    return jsonify(obtener_pacientes())


@pacientes_bp.route("/pacientes", methods=["POST"])
def crear_pacientes_json():
    campos = [
        "dni",
        "nombre",
        "apellido",
        "telefono",
        "email",
        "direccion_calle",
        "direccion_numero",
    ]

    validacion = validar_json_y_campos_del_cuerpo(request.is_json, request.json, campos)

    if not validacion["resultado"]:
        return jsonify({"error": validacion["mensaje"]}), 400

    campos_validados = [request.json[campo] for campo in campos]
    # TODO: Crear pacientes
    # crear_paciente()

    return jsonify({"msg": campos_validados}), 200
