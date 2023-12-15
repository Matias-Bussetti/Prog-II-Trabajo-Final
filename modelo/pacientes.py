import random
import os

# Para los IDS
import uuid

from utils.functions import (
    ejecutar_funcion_por_cada_elemento_obtenido_de_una_api,
    exportar_lista_a_csv,
    hacer_por_cada_fila_de_csv,
    obtener_elemento_de_lista_cuando_campo_es_igual,
)

ruta_archivo_pacientes = r"modelo\db\pacientes.csv"
url_pacientes = "https://randomuser.me/api/?password=number,8&noinfo=&inc=login,name,id,phone,email,location&results=200"

pacientes = []


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
    global pacientes
    pacientes = []

    def por_cada_fila(fila):
        pacientes.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "apellido": fila["apellido"],
                "dni": int(fila["dni"]),
                "telefono": fila["telefono"],
                "email": fila["email"],
                "direccion_calle": fila["direccion_calle"],
                "direccion_numero": int(fila["direccion_numero"]),
            }
        )

    hacer_por_cada_fila_de_csv(ruta_archivo_pacientes, por_cada_fila)


def importar_datos_desde_api():
    global pacientes
    pacientes = []

    def por_cada_fila(fila):
        dni = ""
        if fila["id"]["value"]:
            dni = int(
                "".join(
                    [
                        numeros
                        for numeros in (fila["id"]["value"])
                        if numeros in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    ]
                )
            )
        else:
            dni = random.randint(20000000, 80000000)

        pacientes.append(
            {
                "id": fila["login"]["uuid"],
                "nombre": fila["name"]["first"],
                "apellido": fila["name"]["last"],
                "telefono": fila["phone"],
                "dni": dni,
                "email": fila["email"],
                "direccion_calle": fila["location"]["street"]["name"],
                "direccion_numero": int(fila["location"]["street"]["number"]),
            }
        )

    ejecutar_funcion_por_cada_elemento_obtenido_de_una_api(url_pacientes, por_cada_fila)
    exportar_a_csv()


def inicializar_pacientes():
    if os.path.exists(ruta_archivo_pacientes):
        importar_datos_desde_csv()
    else:
        importar_datos_desde_api()


# ---------------------------------------------
def obtener_pacientes():
    return pacientes


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
    global pacientes
    # Agrega la sucursal a la lista con un ID único
    pacientes.append(
        {
            "id": uuid.uuid1(),
            "nombre": nombre_paciente,
            "apellido": apellido_paciente,
            "dni": dni,
            "telefono": telefono,
            "email": email,
            "direccion_calle": direccion_calle,
            "direccion_numero": direccion_numero,
        }
    )
    exportar_a_csv()
    return pacientes[-1]


def obtener_paciente_por_id(id):
    global pacientes
    return obtener_elemento_de_lista_cuando_campo_es_igual(pacientes, "id", id)


def editar_paciente_por_id(id, campos, datos):
    paciente_actualizado = None

    def actualizar(paciente):
        nonlocal paciente_actualizado
        if paciente["id"] == id:
            for campo in campos:
                paciente[campo] = datos[campo]
            paciente_actualizado = paciente
        return paciente

    global pacientes
    pacientes = [actualizar(paciente) for paciente in pacientes]
    exportar_a_csv()

    return paciente_actualizado


def eliminar_paciente_por_id(id):
    # TODO: Compobar que exista
    global pacientes
    paciente = [paciente for paciente in pacientes if paciente["id"] == id]
    if len(paciente) > 0:
        paciente = paciente[0]
        pacientes = [paciente for paciente in pacientes if paciente["id"] != id]
        exportar_a_csv()
        return paciente
    return {"error": "paciente no existe"}
