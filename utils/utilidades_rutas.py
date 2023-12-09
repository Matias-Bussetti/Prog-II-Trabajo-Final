def comprobar_existe_el_recurso(obtener_recurso, valor_busqueda, si_no_esta):
    recurso = obtener_recurso(valor_busqueda)
    if not recurso:
        si_no_esta({"error": "Recurso no existe"})
