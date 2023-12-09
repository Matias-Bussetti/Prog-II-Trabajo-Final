import csv
import os

# Para los IDS
import uuid

from utils.functions import (
    hacer_por_cada_fila_de_csv,
    exportar_lista_a_csv,
    obtener_elemento_de_lista_cuando_campo_es_igual,
)

ruta_archivo_turnos = r"modelo\db\turnos.csv"
ruta_api_turnos = r"modelo\api\turnos_api.csv"

turnos = []


def exportar_a_csv():
    exportar_lista_a_csv(
        ruta_archivo_turnos,
        [
            "id",
            "dni",
            "nombre",
            "apellido",
            "telefono",
            "email",
            "matricula",
            "habilitado",
        ],
        turnos,
    )


def importar_datos_desde_csv():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global turnos
    turnos = []

    def por_cada_fila(fila):
        turnos.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "apellido": fila["apellido"],
                "dni": fila["dni"],
                "telefono": fila["telefono"],
                "email": fila["email"],
                "matricula": fila["matricula"],
                "habilitado": bool(fila["habilitado"]),
            }
        )

    hacer_por_cada_fila_de_csv(ruta_archivo_turnos, por_cada_fila)


def importar_datos_desde_api():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global turnos
    global id_turnos
    turnos = []

    def por_cada_fila(fila):
        turnos.append(
            {
                "id": fila["login.uuid"],
                "nombre": fila["name.first"],
                "apellido": fila["name.last"],
                "dni": fila["id.value"][:-2],
                "telefono": fila["phone"],
                "email": fila["email"],
                "matricula": fila["login.password"],
                "habilitado": True,
            }
        )

    hacer_por_cada_fila_de_csv(ruta_api_turnos, por_cada_fila)
    exportar_a_csv()


def inicializar_turnos():
    global id_turnos
    if os.path.exists(ruta_archivo_turnos):
        importar_datos_desde_csv()
    else:
        importar_datos_desde_api()


# ---------------------------------------------
def obtener_turnos():
    return turnos


def crear_turno(
    nombre_turno,
    apellido_turno,
    dni,
    telefono,
    email,
    matricula,
):
    # TODO: Id's de participantes hacer funcinar???
    # Agrega la sucursal a la lista con un ID único
    turnos.append(
        {
            "id": uuid.uuid1(),
            "nombre": nombre_turno,
            "apellido": apellido_turno,
            "dni": dni,
            "telefono": telefono,
            "email": email,
            "matricula": matricula,
            "habilitado": True,
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
