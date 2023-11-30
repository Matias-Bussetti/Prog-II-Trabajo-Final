# -----------------------------------------------------------------
# Módulo de funciones sobre productos
# -----------------------------------------------------------------

import csv
import os

# Variables globales que usaremos en este módulo
productos = []  # Lista de productos
id_producto = 1  # Variable para asignar IDs únicos a los productos
ruta_archivo_productos = "modelo\productos.csv"


def inicializar_productos():
    """
    Inicializa la lista de productos.

    Si existe un archivo CSV con datos de productos, los importa.
    Si no existe, agrega dos productos de ejemplo a la lista.
    """
    global id_producto
    if os.path.exists(ruta_archivo_productos):
        importar_datos_desde_csv()


def crear_producto(nombre_producto, descripcion, precio):
    """
    Crea un nuevo producto con el nombre de producto y descripcion especificados.

    Parameters:
    nombre_producto (str): El nombre de producto del nuevo producto.
    descripcion (str): La descripcion del nuevo producto.
    precio (int): La descripcion del nuevo producto.

    Returns:
    dict: El producto recién creado, con un ID único.
    """
    global id_producto
    # Agrega el producto a la lista con un ID único
    productos.append(
        {
            "id": id_producto,
            "nombre de producto": nombre_producto,
            "descripcion": descripcion,
            "precio": precio,
        }
    )
    id_producto += 1
    exportar_a_csv()
    # Devuelve el producto recién creado
    return productos[-1]


def obtener_productos():
    """
    Obtiene todos los productos.

    Returns:
    list: La lista de todos los productos.
    """
    # Devuelve la lista de productos
    return productos


def editar_producto_por_id(
    id_producto, nuevo_nombre_producto, nueva_descripcion, nuevo_precio
):
    """
    Edita el nombre de producto y descripcion de un producto existente.

    Parameters:
    id_producto (int): El ID del producto a editar.
    nuevo_nombre_producto (str): El nuevo nombre de producto.
    nueva_descripcion (str): La nueva descripcion.

    Returns:
    dict: El producto editado, o None si no se encuentra.
    """
    # Recorre la lista de productos
    for producto in productos:
        # Si el ID de producto coincide, actualiza el nombre de producto y la descripcion
        if producto["id"] == id_producto:
            producto["nombre de producto"] = nuevo_nombre_producto
            producto["descripcion"] = nueva_descripcion
            producto["precio"] = nuevo_precio
            exportar_a_csv()
            return producto
    # Devuelve None si no se encuentra el producto
    return None


def eliminar_producto_por_id(id_producto):
    """
    Elimina un producto por su ID.

    Parameters:
    id_producto (int): El ID del producto a eliminar.
    """
    global productos
    # Crea una nueva lista sin el producto a eliminar
    productos = [producto for producto in productos if producto["id"] != id_producto]
    exportar_a_csv()


def exportar_a_csv():
    """
    Exporta los datos de productos a un archivo CSV.
    """
    with open(ruta_archivo_productos, "w", newline="") as csvfile:
        campo_nombres = ["id", "nombre de producto", "descripcion", "precio"]
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for producto in productos:
            writer.writerow(producto)


def importar_datos_desde_csv():
    """
    Importa los datos de productos desde un archivo CSV.
    """
    global productos
    global id_producto
    productos = (
        []
    )  # Limpiamos la lista de productos antes de importar desde el archivo CSV
    with open(ruta_archivo_productos, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertimos el ID de cadena a entero
            row["id"] = int(row["id"])
            productos.append(row)
    if len(productos) > 0:
        id_producto = productos[-1]["id"] + 1
    else:
        id_producto = 1


####


def obtener_producto_por_id(id_producto):
    if len(productos) > 0:
        for producto in productos:
            if int(producto["id"]) == int(id_producto):
                return producto
    return False
