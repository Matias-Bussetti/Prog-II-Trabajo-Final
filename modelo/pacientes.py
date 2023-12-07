import csv
import os
ruta_archivo_pacientes='modelo\pacientes.csv'

pacientes = []
id_pacientes = 1

def exportar_a_csv():
    """
    Exporta los datos de sucursales a un archivo CSV.
    """
    with open(ruta_archivo_pacientes, 'w', newline='', encoding='utf-8') as csvfile:
        campo_nombres = ['id', 'dni', 'nombre','apellido','teléfono','email','direccion_calle','direccion_numero']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for paciente in pacientes:
            writer.writerow(paciente)

def importar_datos_desde_csv():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global pacientes
    global id_pacientes
    pacientes = []  # Limpiamos la lista de sucursales antes de importar desde el archivo CSV
    with open(ruta_archivo_pacientes, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row['id'] = int(row['id'])
            pacientes.append(row) 
    if len(pacientes)>0:
        id_pacientes= pacientes[-1]["id"]+1
    else:
        id_pacientes = 1

def inicializar_pacientes():

    global id_pacientes
    if os.path.exists(ruta_archivo_pacientes):
        importar_datos_desde_csv()


def crear_paciente(nombre_paciente, apellido_paciente, dni, telefono, email, direccion_calle, direccion_numero):
   
    global id_pacientes
    # Agrega la sucursal a la lista con un ID único
    medicos.append({
        "id": id_pacientes,
        "nombre": nombre_paciente,
        "apellido": apellido_paciente,
        "dni": dni,
        "telefono": telefono,
        "email": email,
        "direccion_calle": direccion_calle,
        "direccion_numero": direccion_numero
    })
    id_pacientes += 1
    exportar_a_csv()
    # Devuelve la sucursal recién creada
    return pacientes[-1]

def obtener_pacientes():
    
    # Devuelve la lista de sucursales
    return pacientes

def obtener_pacientes_por_id(id_pacientes):
    # Devuelve la lista de sucursales por id
    return [paciente for paciente in pacientes if paciente['id'] == id_pacientes]

def editar_pacientes_por_id(id_paciente,nombre_paciente, apellido_paciente, dni, telefono, email, direccion_calle, direccion_numero):

    # Recorre la lista de sucursales
    for paciente in pacientes:
        # Si el ID de producto coincide, actualiza el nombre de producto y la descripcion
        if paciente["id"] == id_paciente:
            paciente["nombre"] = nombre_paciente
            paciente["apellido"] = apellido_paciente
            paciente["dni"] = dni
            paciente["telefono"] = telefono
            paciente["email"] = email
            paciente["direccion_calle"] = direccion_calle
            paciente["direccion_numero"] = direccion_numero
            exportar_a_csv()
            return paciente
    # Devuelve None si no se encuentra el producto
    return None


def eliminar_pacientes_por_id(id_pacientes):
   
    global pacientes
    # Crea una nueva lista sin el producto a eliminar
    pacientes = [paciente for paciente in pacientes if paciente["id"] != id_pacientes]
    exportar_a_csv()