import csv
import os
ruta_archivo_medicos='modelo\medicos.csv'

medicos = []
id_medicos = 1

def exportar_a_csv():
    """
    Exporta los datos de sucursales a un archivo CSV.
    """
    with open(ruta_archivo_medicos, 'w', newline='', encoding='utf-8') as csvfile:
        campo_nombres = ['id', 'dni', 'nombre','apellido','matrícula','teléfono','email','habilitado']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for medico in medicos:
            writer.writerow(medico)

def importar_datos_desde_csv():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global medicos
    global id_medicos
    medicos = []  # Limpiamos la lista de sucursales antes de importar desde el archivo CSV
    with open(ruta_archivo_medicos, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            medicos.append(row) 
    if len(medicos)>0:
        id_medicos= medicos[-1]["id"]+1
    else:
        id_medicos = 1

def inicializar_medicos():

    global id_medicos
    if os.path.exists(ruta_archivo_medicos):
        importar_datos_desde_csv()


def crear_medico(nombre_medico, apellido_medico, dni, matricula, telefono, email, habilitado):
   
    global id_medicos
    # Agrega la sucursal a la lista con un ID único
    medicos.append({
        "id": id_medicos,
        "nombre": nombre_medico,
        "apellido": apellido_medico,
        "dni": dni,
        "matricula": matricula,
        "telefono": telefono,
        "email": email,
        "habilitado": habilitado
    })
    id_medicos += 1
    exportar_a_csv()
    # Devuelve la sucursal recién creada
    return medicos[-1]

def obtener_medicos():
    
    # Devuelve la lista de sucursales
    return medicos

def obtener_medicos_por_id(id_medicos):
    # Devuelve la lista de sucursales por id
    return [medico for medico in medicos if medico['id'] == id_medicos]

def editar_medicos_por_id(id_medicos,nombre_medico, apellido_medico, dni, matricula, telefono, email, habilitado):

    # Recorre la lista de sucursales
    for medico in medicos:
        # Si el ID de producto coincide, actualiza el nombre de producto y la descripcion
        if medico["id"] == id_medicos:
            medico["nombre"] = nombre_medico
            medico["apellido"] = apellido_medico
            medico["dni"] = dni
            medico["matricula"] = matricula
            medico["telefono"] = telefono
            medico["email"] = email
            medico["habilitado"] = habilitado
            exportar_a_csv()
            return medico
    # Devuelve None si no se encuentra el producto
    return None


def deshabilitar_medicos_por_id(id_medicos,habilitado):
    # Recorre la lista de sucursales
    for medico in medicos:
        # Si el ID de producto coincide, actualiza el nombre de producto y la descripcion
        if medico["id"] == id_medicos:
            medico["habilitado"] = habilitado
            exportar_a_csv()
            return medico
    # Devuelve None si no se encuentra el producto
    return None

def eliminar_medicos_por_id(id_medicos):
   
    global medicos
    # Crea una nueva lista sin el producto a eliminar
    medicos = [medico for medico in medicos if medico["id"] != id_medicos]
    exportar_a_csv()