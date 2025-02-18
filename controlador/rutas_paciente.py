from flask import Blueprint, jsonify, request

from modelo.pacientes import (
    obtener_pacientes,
    crear_paciente,
    obtener_paciente_por_id,
    editar_paciente_por_id,
    eliminar_paciente_por_id,
)
from utils.functions import (
    validar_campos_del_cuerpo,
    campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable,
)

pacientes_bp = Blueprint("pacientes", __name__)


@pacientes_bp.route("/pacientes/", methods=["GET"])
def obtener_pacientes_json():
    try:
        return jsonify(obtener_pacientes())
    except:
        return jsonify({"error": "Falla en el server"}), 500


@pacientes_bp.route("/pacientes", methods=["POST"])
def crear_pacientes_json():
    try:
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

        arreglo_de_tuplas_campo_y_tipo = [
            ("dni", "int"),
            ("nombre", "string"),
            ("apellido", "string"),
            ("telefono", "string"),
            ("email", "email"),
            ("direccion_calle", "string"),
            ("direccion_numero", "int"),
        ]

        validacion_de_tipo_de_datos = (
            campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable(
                request.json, arreglo_de_tuplas_campo_y_tipo
            )
        )

        if not validacion_de_tipo_de_datos["resultado"]:
            return jsonify({"error": validacion_de_tipo_de_datos["mensaje"]}), 400

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
    except:
        return jsonify({"error": "Falla en el server"}), 500


@pacientes_bp.route("/pacientes/<string:id>", methods=["GET"])
def obtener_paciente(id):
    try:
        paciente = obtener_paciente_por_id(id)
        if not paciente:
            return jsonify({"error": "Paciente no existe"}), 404

        return jsonify(paciente), 200
    except:
        return jsonify({"error": "Falla en el server"}), 500


@pacientes_bp.route("/pacientes/<string:id>", methods=["DELETE"])
def eliminar_paciente(id):
    try:
        paciente = obtener_paciente_por_id(id)
        if not paciente:
            return jsonify({"error": "Paciente no existe"}), 404

        return jsonify(eliminar_paciente_por_id(id)), 200
    except:
        return jsonify({"error": "Falla en el server"}), 500


@pacientes_bp.route("/pacientes/<string:id>", methods=["PUT"])
def actualizar_paciente_json(id):
    try:
        if not request.is_json:
            return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

        paciente = obtener_paciente_por_id(id)
        if not paciente:
            return jsonify({"error": "Paciente no existe"}), 404

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

        arreglo_de_tuplas_campo_y_tipo = [
            ("dni", "int"),
            ("nombre", "string"),
            ("apellido", "string"),
            ("telefono", "string"),
            ("email", "email"),
            ("direccion_calle", "string"),
            ("direccion_numero", "int"),
        ]

        validacion_de_tipo_de_datos = (
            campos_de_un_cuerpo_corresponden_a_su_tipo_de_variable(
                request.json, arreglo_de_tuplas_campo_y_tipo
            )
        )

        if not validacion_de_tipo_de_datos["resultado"]:
            return jsonify({"error": validacion_de_tipo_de_datos["mensaje"]}), 400

        return (
            jsonify(editar_paciente_por_id(id, validacion["campos"], request.json)),
            200,
        )
    except:
        return jsonify({"error": "Falla en el server"}), 500
