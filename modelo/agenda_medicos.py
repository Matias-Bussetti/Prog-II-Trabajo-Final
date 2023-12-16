import csv
import os
from datetime import datetime, time

from utils.functions import obtener_elemento_de_lista_cuando_campo_es_igual

ruta_archivo_agenda_medicos = "modelo/db/agenda_medicos.csv"

agenda_medicos = []


def exportar_a_csv():
    with open(
        ruta_archivo_agenda_medicos, "w", newline="", encoding="utf-8"
    ) as csvfile:
        campo_nombres = [
            "id_medico",
            "dia_numero",
            "hora_inicio",
            "hora_fin",
            "fecha_actualizacion",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for agenda in agenda_medicos:
            writer.writerow(agenda)


def importar_datos_desde_csv():
    global agenda_medicos
    agenda_medicos = []
    with open(ruta_archivo_agenda_medicos, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["id_medico"] = row["id_medico"]
            row["dia_numero"] = int(row["dia_numero"])
            agenda_medicos.append(row)


def inicializar_agenda_medicos():
    if os.path.exists(ruta_archivo_agenda_medicos):
        importar_datos_desde_csv()


def obtener_agenda():
    return sorted(agenda_medicos, key=lambda x: (x["id_medico"], x["dia_numero"]))


def obtener_agenda_medico_por_id(id_medico):
    return [agenda for agenda in agenda_medicos if agenda["id_medico"] == id_medico]


def agregar_horario_agenda(
    id_medico, dia_numero, hora_inicio, hora_fin, fecha_actualizacion
):
    global agenda_medicos
    fecha_actualizacion = datetime.now().strftime("%Y/%m/%d")
    agenda_medicos.append(
        {
            "id_medico": id_medico,
            "dia_numero": dia_numero,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "fecha_actualizacion": fecha_actualizacion,
        }
    )
    exportar_a_csv()
    return agenda_medicos[-1]


def verificar_disponibilidad(id_medico, dia_numero, hora_inicio, hora_fin):
    for agenda in agenda_medicos:
        if (
            agenda["id_medico"] == id_medico
            and agenda["dia_numero"] == dia_numero
            and (
                (
                    time.fromisoformat(agenda["hora_inicio"])
                    <= time.fromisoformat(hora_inicio)
                    <= time.fromisoformat(agenda["hora_fin"])
                )
                or (
                    time.fromisoformat(agenda["hora_inicio"])
                    <= time.fromisoformat(hora_fin)
                    <= time.fromisoformat(agenda["hora_fin"])
                )
            )
        ):
            return False
    return True


def modificar_horarios_agenda(id_medico, lista_de_horarios):
    global agenda_medicos

    for horarios in lista_de_horarios:

        def actualizar(agenda):
            actualizadaAgenda = agenda
            if (
                actualizadaAgenda["id_medico"] == id_medico
                and actualizadaAgenda["dia_numero"] == horarios["dia"]
            ):
                actualizadaAgenda["hora_inicio"] = horarios["hora_inicio"]
                actualizadaAgenda["hora_fin"] = horarios["hora_fin"]
            return actualizadaAgenda

        exportar_a_csv()
        agenda_medicos = [actualizar(agenda) for agenda in agenda_medicos]

    return obtener_agenda_medico_por_id(id_medico)


def eliminar_horario_agenda(id_medico):
    global agenda_medicos

    agenda_medicos = [
        agenda for agenda in agenda_medicos if agenda["id_medico"] == id_medico
    ]
    exportar_a_csv()
    if len(agenda_medicos) > 0:
        agenda = agenda[0]
        agenda_medicos = [
            agenda for agenda in agenda_medicos if agenda["id_medico"] != id_medico
        ]
        exportar_a_csv()
        return agenda
    return {"error": "agenda no existe"}
