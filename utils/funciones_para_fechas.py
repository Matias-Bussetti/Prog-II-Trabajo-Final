from datetime import datetime, timedelta


# https://docs.python.org/3/library/datetime.html
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

formato_de_fecha = "%d/%m/%Y"
formato_de_hora = "%H:%M"


def texto_a_fecha(texto):
    return datetime.strptime(texto, formato_de_fecha)


def texto_a_hora(texto):
    return datetime.strptime(texto, formato_de_hora)


def fecha_esta_dentro_de_un_rango_de_30_dias(fecha):
    fecha_convertida = texto_a_fecha(fecha)

    hoy = texto_a_fecha(datetime.now().strftime(formato_de_fecha))

    dentro_de_30_dias = texto_a_fecha(
        (datetime.now() + timedelta(days=30)).strftime(formato_de_fecha)
    )

    return hoy <= fecha_convertida and fecha_convertida <= dentro_de_30_dias


def rango_horario_esta_dentro_de_un_rango_horario(
    rango_horario_inicio,
    rango_horario_fin,
    rango_horario_dentro_inicio,
    rango_horario_dentro_fin,
):
    hora_inicio = texto_a_hora(rango_horario_inicio)
    hora_fin = texto_a_hora(rango_horario_fin)

    rango_inicio = texto_a_hora(rango_horario_dentro_inicio)
    rango_fin = texto_a_hora(rango_horario_dentro_fin)

    rango_inicio_fin_es_valido = rango_inicio < rango_fin
    rango_mayor_a_hora_inicial = hora_inicio < rango_inicio
    rango_menor_a_hora_final = rango_fin < hora_fin

    return (
        rango_inicio_fin_es_valido
        and rango_mayor_a_hora_inicial
        and rango_menor_a_hora_final
    )


def fecha_corresponde_al_numero_dia_de_semana(fecha, numero_de_dia_de_semana):
    formato_de_dia_de_semana = "%w"

    numero_de_dia_de_semana_de_la_fecha = datetime.strptime(
        fecha, formato_de_fecha
    ).strftime(formato_de_dia_de_semana)

    return int(numero_de_dia_de_semana_de_la_fecha) == int(numero_de_dia_de_semana)


def fecha_y_horario_son_validos_para_una_lista_de_horarios(
    lista_de_horarios,
    fecha_a_validar,
    rango_horario_hora_inicio_a_validar,
    rango_horario_hora_fin_a_validar,
):
    if not len(lista_de_horarios) > 0:
        return False

    if not fecha_esta_dentro_de_un_rango_de_30_dias(fecha_a_validar):
        return False

    son_validos = False
    iterador = 0
    while iterador < len(lista_de_horarios):
        horario = lista_de_horarios[iterador]

        if fecha_corresponde_al_numero_dia_de_semana(
            fecha_a_validar, horario["dia_numero"]
        ) and rango_horario_esta_dentro_de_un_rango_horario(
            horario["hora_inicio"],
            horario["hora_fin"],
            rango_horario_hora_inicio_a_validar,
            rango_horario_hora_fin_a_validar,
        ):
            son_validos = True
        iterador += 1

    return son_validos


def fecha_y_hora_se_superpone_con_un_turno_dentro_de_una_lista_de_turnos(
    lista_de_turnos,
    fecha,
    hora,
):
    def rango_horario_esta_fuera_de_un_rango_horario(
        rango_horario_inicio,
        rango_horario_fin,
        rango_horario_fuera_inicio,
        rango_horario_fin_fin,
    ):
        hora_inicio = texto_a_hora(rango_horario_inicio)
        hora_fin = texto_a_hora(rango_horario_fin)

        rango_inicio = texto_a_hora(rango_horario_fuera_inicio)
        rango_fin = texto_a_hora(rango_horario_fin_fin)

        rango_inicio_fin_es_valido = rango_inicio < rango_fin

        rango_menor_a_hora_inicial = rango_fin < hora_inicio

        rango_mayor_a_hora_final = hora_fin < rango_inicio

        return rango_inicio_fin_es_valido and (
            rango_menor_a_hora_inicial or rango_mayor_a_hora_final
        )

    if not len(lista_de_turnos) > 0:
        return False

    se_superpone = False
    iterador = 0
    while iterador < len(lista_de_turnos) and not se_superpone:
        turno = lista_de_turnos[iterador]

        if turno["fecha_solicitud"] == fecha:
            if not rango_horario_esta_fuera_de_un_rango_horario(
                (turno["hora_turno"]),
                devolver_hora_mas_15_minutos_en_string(turno["hora_turno"]),
                (hora),
                devolver_hora_mas_15_minutos_en_string(hora),
            ):
                se_superpone = True
        iterador += 1

    return se_superpone


# https://bobbyhadz.com/blog/python-add-minutes-to-datetime
def devolver_hora_mas_15_minutos_en_string(fecha):
    return (texto_a_hora(fecha) + timedelta(minutes=15)).strftime(formato_de_hora)


# TODO Hacer una función que compruebe que los minutos de
# TODO una hora sean 00 15 30 45
