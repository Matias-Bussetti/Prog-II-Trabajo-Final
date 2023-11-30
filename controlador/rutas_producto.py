from flask import Blueprint, jsonify, request
from modelo.producto import (
    crear_producto,
    obtener_producto_por_id,
    obtener_productos,
    editar_producto_por_id,
    eliminar_producto_por_id,
)


# Creamos el blueprint
productos_bp = Blueprint("productos", __name__)


@productos_bp.route("/productos/", methods=["GET"])
def obtener_productos_json():
    return jsonify(obtener_productos())


@productos_bp.route("/productos", methods=["POST"])
def crear_producto_json():
    if request.is_json:
        if (
            "nombre_de_producto" in request.json
            and "descripcion" in request.json
            and "precio" in request.json
        ):
            producto = request.get_json()
            producto_creado = crear_producto(
                producto["nombre_de_producto"],
                producto["descripcion"],
                producto["precio"],
            )
            return jsonify(producto_creado), 200
        else:
            return jsonify({"error": "Faltan datos"}), 200
    else:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 200


@productos_bp.route("/productos/<int:id_producto>", methods=["PUT"])
def modificar_producto_json(id_producto):
    if request.is_json:
        if (
            "nombre_de_producto" in request.json
            and "descripcion" in request.json
            and "precio" in request.json
        ):
            producto = request.get_json()
            producto_modificado = editar_producto_por_id(
                id_producto,
                producto["nombre_de_producto"],
                producto["descripcion"],
                producto["precio"],
            )
            return jsonify(producto_modificado), 200
        else:
            return jsonify({"error": "Faltan datos"}), 200
    else:
        return jsonify({"error": "El formato de la solicitud no es JSON"}), 200


@productos_bp.route("/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto_json(id_producto):
    return jsonify(eliminar_producto_por_id(id_producto)), 200


@productos_bp.route("/productos/<int:id_producto>", methods=["GET"])
def obtener_producto_con_id_a_json(id_producto):
    if int(id_producto) > 0:
        producto = obtener_producto_por_id(id_producto)
        if producto:
            return jsonify(producto), 200
        return jsonify({"error": "not found"}), 404
    else:
        return jsonify({"error": "El formato de la solicitud incorrecta"}), 200
