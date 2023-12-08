import csv
import os

from utils.functions import hacer_por_cada_fila_de_csv, exportar_lista_a_csv

ruta_archivo_pacientes = "modelo\pacientes.csv"
ruta_api_pacientes = "modelo\pacientes_api.csv"

pacientes = []
id_pacientes = 1  # TODO: Comprobar si se usa


def exportar_a_csv():
    exportar_lista_a_csv(
        ruta_archivo_pacientes,
        [
            "id",
            "dni",
            "nombre",
            "apellido",
            "telefono",
            "email",
            "direccion_calle",
            "direccion_numero",
        ],
        pacientes,
    )


def importar_datos_desde_csv():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global pacientes
    global id_pacientes
    pacientes = []

    def por_cada_fila(fila):
        pacientes.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "apellido": fila["apellido"],
                "dni": fila["dni"],
                "telefono": fila["telefono"],
                "email": fila["email"],
                "direccion_calle": fila["direccion_calle"],
                "direccion_numero": fila["direccion_numero"],
            }
        )

    hacer_por_cada_fila_de_csv(ruta_archivo_pacientes, por_cada_fila)


def importar_datos_desde_api():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global pacientes
    global id_pacientes
    pacientes = []

    def por_cada_fila(fila):
        pacientes.append(
            {
                "id": fila["login.uuid"],
                "nombre": fila["name.first"],
                "apellido": fila["name.last"],
                "dni": fila["id.value"],
                "telefono": fila["phone"],
                "email": fila["email"],
                "direccion_calle": fila["location.street.name"],
                "direccion_numero": fila["location.street.number"],
            }
        )

    hacer_por_cada_fila_de_csv(ruta_api_pacientes, por_cada_fila)


def inicializar_pacientes():
    global id_pacientes
    if os.path.exists(ruta_archivo_pacientes):
        importar_datos_desde_csv()
    else:
        importar_datos_desde_api()


def crear_paciente(
    nombre_paciente,
    apellido_paciente,
    dni,
    telefono,
    email,
    direccion_calle,
    direccion_numero,
):
    # TODO: Id's de participantes hacer funcinar???
    global id_pacientes
    # Agrega la sucursal a la lista con un ID único
    medicos.append(
        {
            "id": id_pacientes,
            "nombre": nombre_paciente,
            "apellido": apellido_paciente,
            "dni": dni,
            "telefono": telefono,
            "email": email,
            "direccion_calle": direccion_calle,
            "direccion_numero": direccion_numero,
        }
    )
    id_pacientes += 1
    exportar_a_csv()
    return pacientes[-1]


def obtener_pacientes():
    return pacientes


def obtener_pacientes_por_id(id_pacientes):
    return [paciente for paciente in pacientes if paciente["id"] == id_pacientes]


def editar_pacientes_por_id(
    id_paciente,
    nombre_paciente,
    apellido_paciente,
    dni,
    telefono,
    email,
    direccion_calle,
    direccion_numero,
):
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
    pacientes = [paciente for paciente in pacientes if paciente["id"] != id_pacientes]
    exportar_a_csv()
