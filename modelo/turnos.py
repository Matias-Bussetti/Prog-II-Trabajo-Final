import csv
import os

# Para los IDS
import uuid

from utils.functions import (
    hacer_por_cada_fila_de_csv,
    exportar_lista_a_csv,
    obtener_elemento_de_lista_cuando_campo_es_igual,
    crear_csv_con_encabezados,
)

ruta_archivo_turnos = r"modelo\db\turnos.csv"

turnos = []

# TODO: Agregar id


def exportar_a_csv():
    exportar_lista_a_csv(
        ruta_archivo_turnos,
        [
            "id_medico",
            "id_paciente",
            "hora_turno",
            "fecha_solicitud",
        ],
        turnos,
    )


def importar_datos_desde_csv():
    global turnos
    turnos = []

    def por_cada_fila(fila):
        # id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion
        turnos.append(
            {
                "id_medico": fila["id_medico"],
                "id_paciente": fila["id_paciente"],
                "hora_turno": fila["hora_turno"],
                "fecha_solicitud": fila["fecha_solicitud"],
            }
        )

    hacer_por_cada_fila_de_csv(ruta_archivo_turnos, por_cada_fila)


def inicializar_turnos():
    if os.path.exists(ruta_archivo_turnos):
        importar_datos_desde_csv()
    else:
        crear_csv_con_encabezados(
            ruta_archivo_turnos,
            [
                "id_medico",
                "id_paciente",
                "hora_turno",
                "fecha_solicitud",
            ],
        )


# ---------------------------------------------


def obtener_turnos():
    return turnos


def crear_turno(
    id_medico,
    id_paciente,
    hora_turno,
    fecha_solicitud,
):
    # TODO: Id's de participantes hacer funcinar???
    # Agrega la sucursal a la lista con un ID único
    turnos.append(
        {
            id_medico: id_medico,
            id_paciente: id_paciente,
            hora_turno: hora_turno,
            fecha_solicitud: fecha_solicitud,
        }
    )
    exportar_a_csv()
    return turnos[-1]


def obtener_turno_por_id(id):
    return obtener_elemento_de_lista_cuando_campo_es_igual(turnos, "id", id)


def editar_turno_por_id(id, campos, datos):
    turno_actualizado = None

    def actualizar(turno):
        nonlocal turno_actualizado
        if turno["id"] == id:
            for campo in campos:
                turno[campo] = datos[campo]
            turno_actualizado = turno
        return turno

    global turnos
    turnos = [actualizar(turno) for turno in turnos]
    exportar_a_csv()

    return turno_actualizado


def inhabilitar_turno_por_id(id):
    # TODO: Compobar que exista
    editar_turno_por_id(id, ["habilitado"], {"habilitado": False})
