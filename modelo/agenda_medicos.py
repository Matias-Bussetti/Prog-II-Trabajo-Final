import csv
import os
from datetime import datetime, time

ruta_archivo_agenda_medicos='modelo/agenda_medicos.csv'

agenda_medicos = []
id_agenda = 1

def exportar_a_csv():
    """
    Exporta los datos de sucursales a un archivo CSV.
    """
    with open(ruta_archivo_agenda_medicos, 'w', newline='', encoding='utf-8') as csvfile:
        campo_nombres = ['id_medico', 'dia_numero', 'hora_inicio', 'hora_fin', 'fecha_actualizacion']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for agenda in agenda_medicos:
            writer.writerow(agenda)

def importar_datos_desde_csv():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global agenda_medicos
    global id_agenda
    agenda_medicos = []
    with open(ruta_archivo_agenda_medicos, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id_medico'] = int(row['id_medico'])
            row['dia_numero'] = int(row['dia_numero'])
            agenda_medicos.append(row)
    if len(agenda_medicos) > 0:
        id_agenda = agenda_medicos[-1]["id_medico"] + 1
    else:
        id_agenda = 1

def inicializar_agenda_medicos():
    global id_agenda
    if os.path.exists(ruta_archivo_agenda_medicos):
        importar_datos_desde_csv()

def obtener_agenda():
    return sorted(agenda_medicos, key=lambda x: (x['id_medico'], x['dia_numero']))


def agregar_horario_agenda(id_medico, dia_numero, hora_inicio, hora_fin):
    global agenda_medicos
    fecha_actualizacion = datetime.now().strftime('%Y/%m/%d')
    agenda_medicos.append({
        "id_medico": id_medico,
        "dia_numero": dia_numero,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "fecha_actualizacion": fecha_actualizacion
    })
    exportar_a_csv()
    return agenda_medicos[-1]

def verificar_disponibilidad(id_medico, dia_numero, hora_inicio, hora_fin):
    for agenda in agenda_medicos:
        if (
            agenda["id_medico"] == id_medico and
            agenda["dia_numero"] == dia_numero and
            (
                (
                    time.fromisoformat(agenda["hora_inicio"]) <= time.fromisoformat(hora_inicio) <= time.fromisoformat(agenda["hora_fin"])
                ) or (
                    time.fromisoformat(agenda["hora_inicio"]) <= time.fromisoformat(hora_fin) <= time.fromisoformat(agenda["hora_fin"])
                )
            )
        ):
            return False
    return True

def modificar_horarios_agenda(id_medico, dia_numero, hora_inicio, hora_fin):
    global agenda_medicos
    
    # Verificar que el médico trabaje ese día
    if any(agenda["id_medico"] == id_medico and agenda["dia_numero"] == dia_numero for agenda in agenda_medicos):
        # Verificar disponibilidad de horarios
        if verificar_disponibilidad(id_medico, dia_numero, hora_inicio, hora_fin):
            for agenda in agenda_medicos:
                if agenda["id_medico"] == id_medico and agenda["dia_numero"] == dia_numero:
                    agenda["hora_inicio"] = hora_inicio
                    agenda["hora_fin"] = hora_fin
                    agenda["fecha_actualizacion"] = datetime.now().strftime('%Y/%m/%d')
        else:
            print(f"El médico ya tiene un turno registrado para el día {dia_numero} y horario {hora_inicio} - {hora_fin}.")
    else:
        print(f"El médico no trabaja el día {dia_numero}.")

    exportar_a_csv()
    return obtener_agenda()


def eliminar_horario_agenda(id_medico, dia_numero):
    global agenda_medicos
    agenda_medicos = [agenda for agenda in agenda_medicos if agenda["id_medico"]!= id_medico or agenda["dia_numero"]!= dia_numero]
    exportar_a_csv()

