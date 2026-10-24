"""Transformación: normaliza la respuesta de la API y valida la calidad de los datos."""

from typing import Any

import pandas as pd

from .config import Indicador

COLUMNAS = ["fecha", "indicador", "valor"]


class ErrorDeCalidad(Exception):
    """Los datos no cumplen las reglas de calidad; el pipeline no escribe nada."""

    def __init__(self, indicador: str, problemas: list[str]):
        self.problemas = problemas
        super().__init__(f"{indicador}: " + "; ".join(problemas))


def normalizar(respuesta: dict[str, Any], indicador: Indicador) -> pd.DataFrame:
    """Convierte la respuesta de la API en filas (fecha, indicador, valor) validadas.

    La API marca cada día como la medianoche de Chile expresada en UTC: 03:00Z en
    horario de verano y 04:00Z en invierno. Sumar 12 horas antes de tomar la fecha
    UTC devuelve el día correcto en ambos horarios, y también si la API llegara a
    entregar medianoche UTC, sin depender de las fechas de cambio de hora.
    """
    codigo_respuesta = respuesta.get("codigo")
    if codigo_respuesta is not None and codigo_respuesta != indicador.codigo:
        raise ErrorDeCalidad(
            indicador.codigo, [f"la API devolvió el indicador '{codigo_respuesta}'"]
        )

    crudo = pd.DataFrame(respuesta["serie"], columns=["fecha", "valor"])
    if crudo.empty:
        return pd.DataFrame(columns=COLUMNAS)

    fechas = pd.to_datetime(crudo["fecha"], utc=True, format="ISO8601", errors="coerce")
    datos = pd.DataFrame(
        {
            "fecha": (fechas + pd.Timedelta(hours=12)).dt.strftime("%Y-%m-%d"),
            "indicador": indicador.codigo,
            "valor": pd.to_numeric(crudo["valor"], errors="coerce"),
        }
    )

    problemas = []
    sin_fecha = int(datos["fecha"].isna().sum())
    if sin_fecha:
        problemas.append(f"{sin_fecha} fechas inválidas")
    sin_valor = int(datos["valor"].isna().sum())
    if sin_valor:
        problemas.append(f"{sin_valor} valores no numéricos")

    fuera_de_rango = datos[
        datos["valor"].notna() & ~datos["valor"].between(indicador.minimo, indicador.maximo)
    ]
    if not fuera_de_rango.empty:
        ejemplo = fuera_de_rango.iloc[0]
        problemas.append(
            f"{len(fuera_de_rango)} valores fuera del rango "
            f"[{indicador.minimo}, {indicador.maximo}], por ejemplo "
            f"{ejemplo['valor']} el {ejemplo['fecha']}"
        )

    # Una misma fecha repetida con el mismo valor se descarta; con valores
    # distintos no se puede saber cuál es el correcto.
    datos = datos.drop_duplicates()
    conflictos = datos[datos.duplicated("fecha", keep=False)]["fecha"].unique()
    if len(conflictos):
        problemas.append(
            f"{len(conflictos)} fechas con valores distintos, por ejemplo {conflictos[0]}"
        )

    if problemas:
        raise ErrorDeCalidad(indicador.codigo, problemas)

    datos["valor"] = datos["valor"].round(indicador.decimales)
    return datos.sort_values("fecha").reset_index(drop=True)
