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
            "id",
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
                "id": fila["id"],
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
                "id",
                "id_medico",
                "id_paciente",
                "hora_turno",
                "fecha_solicitud",
            ],
        )


# ---------------------------------------------


def obtener_turnos_de_paciente_con_id_igual_a(id_paciente):
    return [turno for turno in turnos if turno["id_paciente"] == id_paciente]


def obtener_turnos_de_medico_con_id_igual_a(id_medico):
    return [turno for turno in turnos if turno["id_medico"] == id_medico]


def crear_turno(
    id_medico,
    id_paciente,
    hora_turno,
    fecha_solicitud,
):
    turnos.append(
        {
            "id": uuid.uuid1(),
            "id_medico": id_medico,
            "id_paciente": id_paciente,
            "hora_turno": hora_turno,
            "fecha_solicitud": fecha_solicitud,
        }
    )
    exportar_a_csv()
    return turnos[-1]


def obtener_turno_por_id(id):
    return obtener_elemento_de_lista_cuando_campo_es_igual(turnos, "id", id)


def eliminar_turno_por_id(id):
    # TODO: Compobar que exista
    global turnos
    turno = [turno for turno in turnos if turno["id"] == id]
    if len(turno) > 0:
        turno = turno[0]
        turnos = [turno for turno in turnos if turno["id"] != id]
        exportar_a_csv()
        return turno
    return {"error": "turno no existe"}
