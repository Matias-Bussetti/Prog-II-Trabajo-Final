import csv
import os

# Variables globales que usaremos en este módulo
sucursales = []  # Lista de sucursales
id_sucursal = 1  # Variable para asignar IDs únicos a los sucursales
ruta_archivo_sucursales = "modelo\sucursal.csv"


def inicializar_sucursales():
    """
    Inicializa la lista de sucursales.

    Si existe un archivo CSV con datos de sucursales, los importa.
    Si no existe, agrega dos sucursales de ejemplo a la lista.
    """
    global id_sucursal
    if os.path.exists(ruta_archivo_sucursales):
        importar_datos_desde_csv()


def exportar_a_csv():
    """
    Exporta los datos de sucursales a un archivo CSV.
    """
    with open(ruta_archivo_sucursales, "w", newline="") as csvfile:
        campo_nombres = ["id", "nombre de sucursal", "contraseña_admin", "ciudad"]
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for sucursal in sucursales:
            writer.writerow(sucursal)


def importar_datos_desde_csv():
    """
    Importa los datos de sucursales desde un archivo CSV.
    """
    global sucursales
    global id_sucursal
    sucursales = (
        []
    )  # Limpiamos la lista de sucursales antes de importar desde el archivo CSV
    with open(ruta_archivo_sucursales, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row["id"] = int(row["id"])
            sucursales.append(row)
    if len(sucursales) > 0:
        id_sucursal = sucursales[-1]["id"] + 1
    else:
        id_sucursal = 1


def obtener_sucursales():
    return sucursales


def obtener_sucursal_por_id(id_sucursal):
    if len(sucursales) > 0:
        for sucursal in sucursales:
            if int(sucursal["id"]) == int(id_sucursal):
                return sucursal
    return False


def eliminar_sucursal_por_id(id_sucursal):
    global sucursales

    if len(sucursales) > 0:

        def verdaderoSiSucursalNoTieneIdIgualA(sucursal):
            return int(sucursal["id"]) != int(id_sucursal)

        sucursalBorrada = obtener_sucursal_por_id(id_sucursal)

        sucursales = list(filter(verdaderoSiSucursalNoTieneIdIgualA, sucursales))
        exportar_a_csv()

        return sucursalBorrada
    return False


def crear_sucursal(nombre_sucursal, contrasena_admin, ciudad):
    global id_sucursal
    # Agrega el sucursal a la lista con un ID único
    sucursales.append(
        {
            "id": id_sucursal,
            "nombre de sucursal": nombre_sucursal,
            "contraseña_admin": contrasena_admin,
            "ciudad": ciudad,
        }
    )
    id_sucursal += 1
    exportar_a_csv()
    # Devuelve el sucursal recién creado
    return sucursales[-1]


def editar_sucursal(id_sucursal, nombre_sucursal, contrasena_admin, ciudad):
    global sucursales

    def modificarSucursalConIdIgualA(sucursal):
        if int(sucursal["id"]) == int(id_sucursal):
            return {
                "id": id_sucursal,
                "nombre de sucursal": nombre_sucursal,
                "contraseña_admin": contrasena_admin,
                "ciudad": ciudad,
            }
        return sucursal

    sucursales = list(map(modificarSucursalConIdIgualA, sucursales))

    exportar_a_csv()
    # Devuelve el sucursal recién creado
    return {
        "id": id_sucursal,
        "nombre de sucursal": nombre_sucursal,
        "contraseña_admin": contrasena_admin,
        "ciudad": ciudad,
    }
