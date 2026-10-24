"""Carga: combina con el histórico versionado y genera el resumen que lee el sitio."""

import json
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from .config import API_BASE, DIAS_SERIE, DIAS_VARIACION, INDICADORES
from .transformacion import COLUMNAS

LLAVE = ["indicador", "fecha"]


@dataclass
class Cambios:
    nuevas: int
    actualizadas: int


def leer_historico(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        return pd.DataFrame(columns=COLUMNAS)
    return pd.read_csv(ruta, dtype={"fecha": str, "indicador": str, "valor": float})


def combinar(historico: pd.DataFrame, nuevos: pd.DataFrame) -> tuple[pd.DataFrame, Cambios]:
    """Upsert por (indicador, fecha): los datos nuevos reemplazan a los anteriores.

    Correr el pipeline dos veces con los mismos datos no cambia el resultado.
    """
    anteriores = historico.set_index(LLAVE)["valor"]
    recientes = nuevos.set_index(LLAVE)["valor"]
    en_ambos = recientes.index.intersection(anteriores.index)
    cambios = Cambios(
        nuevas=len(recientes.index.difference(anteriores.index)),
        actualizadas=int((recientes[en_ambos] != anteriores[en_ambos]).sum()),
    )
    combinado = (
        pd.concat([historico, nuevos])
        .drop_duplicates(LLAVE, keep="last")
        .sort_values(LLAVE)
        .reset_index(drop=True)
    )
    return combinado[COLUMNAS], cambios


def construir_resumen(historico: pd.DataFrame, hoy: date, generado: datetime) -> dict[str, Any]:
    """Arma el JSON que consume el sitio: último valor, variación y serie reciente.

    La UF se publica por adelantado, así que se ignoran las fechas posteriores a hoy.
    """
    hasta = hoy.isoformat()
    desde = (hoy - timedelta(days=DIAS_SERIE)).isoformat()
    resumen = []
    for codigo, indicador in INDICADORES.items():
        serie = historico[(historico["indicador"] == codigo) & (historico["fecha"] <= hasta)]
        if serie.empty:
            continue
        serie = serie.sort_values("fecha")
        ultimo = serie.iloc[-1]
        referencia = date.fromisoformat(ultimo["fecha"]) - timedelta(days=DIAS_VARIACION)
        previos = serie[serie["fecha"] <= referencia.isoformat()]
        variacion = None
        if not previos.empty:
            base = previos.iloc[-1]["valor"]
            variacion = round((ultimo["valor"] / base - 1) * 100, 2)
        reciente = serie[serie["fecha"] >= desde]
        resumen.append(
            {
                "codigo": codigo,
                "nombre": indicador.nombre,
                "unidad": indicador.unidad,
                "decimales": indicador.decimales,
                "ultimo": {"fecha": ultimo["fecha"], "valor": float(ultimo["valor"])},
                "variacion": variacion,
                "serie": [
                    [f, float(v)] for f, v in zip(reciente["fecha"], reciente["valor"], strict=True)
                ],
            }
        )

    return {
        "generado": generado.isoformat(timespec="seconds"),
        "fuente": {"nombre": "mindicador.cl", "url": API_BASE},
        "registros": len(historico),
        "dias_variacion": DIAS_VARIACION,
        "indicadores": resumen,
    }


def escribir_texto(ruta: Path, contenido: str) -> None:
    """Escribe en un archivo temporal y lo reemplaza, para no dejar archivos a medias."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    temporal.write_text(contenido, encoding="utf-8")
    os.replace(temporal, ruta)


def escribir_historico(historico: pd.DataFrame, ruta: Path) -> None:
    escribir_texto(ruta, historico.to_csv(index=False, lineterminator="\n"))


def escribir_resumen(resumen: dict[str, Any], ruta: Path) -> None:
    # Compacto: es un archivo generado; el histórico legible está en el CSV.
    escribir_texto(ruta, json.dumps(resumen, ensure_ascii=False, separators=(",", ":")) + "\n")
