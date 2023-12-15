from flask import Blueprint, jsonify, request

from modelo.agenda_medicos import (
    obtener_agenda,
    agregar_horario_agenda,
    eliminar_horario_agenda,
    modificar_horarios_agenda,
    verificar_disponibilidad
)

from utils.functions import validar_campos_del_cuerpo

agenda_medicos_bp = Blueprint("agenda_medicos", __name__)

@agenda_medicos_bp.route("/agenda_medicos/", methods=["GET"])
def obtener_agenda_json():
    return jsonify(obtener_agenda())



