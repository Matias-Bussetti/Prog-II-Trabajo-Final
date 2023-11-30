from flask import Blueprint, jsonify, request
from modelo.sucursal import (
    obtener_sucursales,
    obtener_sucursal_por_id,
    eliminar_sucursal_por_id,
    crear_sucursal,
    editar_sucursal,
)


sucursales_bp = Blueprint("sucursales", __name__)


@sucursales_bp.route("/sucursales/", methods=["GET"])
def obtener_sucursales_json():
    return jsonify(obtener_sucursales())


@sucursales_bp.route("/sucursales/<int:id_sucursal>", methods=["GET"])
def obtener_sucursal_por_id_a_json(id_sucursal):
    if int(id_sucursal) > 0:
        sucursal = obtener_sucursal_por_id(id_sucursal)
        if sucursal:
            return jsonify(sucursal), 200
        return jsonify({"error": "not found"}), 404
    else:
        return jsonify({"error": "El formato de la solicitud incorrecta"}), 200


@sucursales_bp.route("/sucursales/<int:id_sucursal>", methods=["DELETE"])
def eliminar_sucursal(id_sucursal):
    # TODO Validar
    sucursalBorrada = eliminar_sucursal_por_id(id_sucursal)
    if sucursalBorrada:
        return jsonify(sucursalBorrada), 200
    return (
        jsonify({"message": "recurso no encontrado, o requerido incorrectamente"}),
        400,
    )


@sucursales_bp.route("/sucursales", methods=["POST"])
def crear_sucursal_json():
    if request.is_json:
        if (
            "nombre_de_sucursal" in request.json
            and "password" in request.json
            and "ciudad" in request.json
        ):
            sucursal = request.get_json()
            sucursal_creado = crear_sucursal(
                sucursal["nombre_de_sucursal"],
                sucursal["password"],
                sucursal["ciudad"],
            )
            return jsonify(sucursal_creado), 200
        else:
            return jsonify({"error": "Faltan datos"}), 200
    else:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 200


@sucursales_bp.route("/sucursales/<int:id_sucursal>", methods=["PUT"])
def modificar_sucursal_json(id_sucursal):
    if request.is_json:
        if (
            "nombre_de_sucursal" in request.json
            and "password" in request.json
            and "ciudad" in request.json
        ):
            sucursal = request.get_json()
            sucursal_modificado = editar_sucursal(
                id_sucursal,
                sucursal["nombre_de_sucursal"],
                sucursal["password"],
                sucursal["ciudad"],
            )
            return jsonify(sucursal_modificado), 200
        else:
            return jsonify({"error": "Faltan datos"}), 200
    else:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 200
