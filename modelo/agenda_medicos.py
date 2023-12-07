import csv
import os
ruta_archivo_agenda_medicos='modelo/agenda_medicos.csv'

agenda_medicos = []

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

    agenda_medicos = []  # Limpiamos la lista de sucursales antes de importar desde el archivo CSV
    with open(ruta_archivo_agenda_medicos, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            agenda_medicos.append(row) 
    if len(agenda_medicos)>0:
        id_agenda_medicos= agenda_medicos[-1]["id"]+1
    else:
        id_agenda_medicos = 1
