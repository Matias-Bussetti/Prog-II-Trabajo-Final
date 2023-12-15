import random
import os

# Para los IDS
import uuid

from utils.functions import (
    hacer_por_cada_fila_de_csv,
    exportar_lista_a_csv,
    obtener_elemento_de_lista_cuando_campo_es_igual,
    ejecutar_funcion_por_cada_elemento_obtenido_de_una_api,
)

ruta_archivo_medicos = r"modelo\db\medicos.csv"
url_medicos = "https://randomuser.me/api/?password=number,8&noinfo=&inc=login,name,id,phone,email,location&results=200"


medicos = []


def exportar_a_csv():
    exportar_lista_a_csv(
        ruta_archivo_medicos,
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
        medicos,
    )


def importar_datos_desde_csv():
    global medicos
    medicos = []

    def por_cada_fila(fila):
        medicos.append(
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

    hacer_por_cada_fila_de_csv(ruta_archivo_medicos, por_cada_fila)


def importar_datos_desde_api():
    global medicos
    medicos = []

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

        medicos.append(
            {
                "id": fila["login"]["uuid"],
                "nombre": fila["name"]["first"],
                "apellido": fila["name"]["last"],
                "telefono": fila["phone"],
                "dni": dni,
                "email": fila["email"],
                "matricula": fila["login"]["password"],
                "habilitado": True,
            }
        )

    ejecutar_funcion_por_cada_elemento_obtenido_de_una_api(url_medicos, por_cada_fila)
    exportar_a_csv()


def inicializar_medicos():
    if os.path.exists(ruta_archivo_medicos):
        importar_datos_desde_csv()
    else:
        importar_datos_desde_api()


# ---------------------------------------------
def obtener_medicos():
    return medicos


def crear_medico(
    nombre_medico,
    apellido_medico,
    dni,
    telefono,
    email,
    matricula,
):
    global medicos
    medicos.append(
        {
            "id": uuid.uuid1(),
            "nombre": nombre_medico,
            "apellido": apellido_medico,
            "dni": dni,
            "telefono": telefono,
            "email": email,
            "matricula": matricula,
            "habilitado": True,
        }
    )
    exportar_a_csv()
    return medicos[-1]


def obtener_medico_por_id(id):
    global medicos

    return obtener_elemento_de_lista_cuando_campo_es_igual(medicos, "id", id)


def editar_medico_por_id(id, campos, datos):
    global medicos

    medico_actualizado = None

    def actualizar(medico):
        nonlocal medico_actualizado
        if medico["id"] == id:
            for campo in campos:
                medico[campo] = datos[campo]
            medico_actualizado = medico
        return medico

    global medicos
    medicos = [actualizar(medico) for medico in medicos]
    exportar_a_csv()

    return medico_actualizado


def inhabilitar_medico_por_id(id):
    # TODO: Compobar que exista
    editar_medico_por_id(id, ["habilitado"], {"habilitado": False})
