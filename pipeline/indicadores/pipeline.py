"""Orquestación: extracción, transformación y carga, en ese orden y sin escrituras parciales."""

import logging
import os
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from . import carga
from .config import INDICADORES, RUTA_HISTORICO, RUTA_RESUMEN, ZONA_HORARIA
from .extraccion import ErrorDeExtraccion, crear_sesion, obtener_serie
from .transformacion import ErrorDeCalidad, normalizar

log = logging.getLogger(__name__)

Extractor = Callable[[str, int], dict[str, Any]]


@dataclass
class Resultado:
    filas_extraidas: int
    cambios: carga.Cambios
    registros: int
    escrito: bool


def anios_por_defecto(hoy: date) -> list[int]:
    # Siempre el año anterior también, para cubrir los 365 días del gráfico.
    return [hoy.year - 1, hoy.year]


def extraer_y_transformar(anios: list[int], obtener: Extractor) -> pd.DataFrame:
    partes = []
    for codigo, indicador in INDICADORES.items():
        filas = [normalizar(obtener(codigo, anio), indicador) for anio in anios]
        datos = pd.concat(filas, ignore_index=True)
        if datos.empty:
            raise ErrorDeCalidad(codigo, [f"la API no devolvió datos para {anios}"])
        log.info(
            "%s: %s filas (%s a %s)", codigo, len(datos), datos["fecha"].min(), datos["fecha"].max()
        )
        partes.append(datos)
    return pd.concat(partes, ignore_index=True)


def ejecutar(
    anios: list[int] | None = None,
    dry_run: bool = False,
    obtener: Extractor | None = None,
    ruta_historico: Path = RUTA_HISTORICO,
    ruta_resumen: Path = RUTA_RESUMEN,
    ahora: datetime | None = None,
) -> Resultado:
    ahora = ahora or datetime.now(UTC)
    hoy = ahora.astimezone(ZoneInfo(ZONA_HORARIA)).date()
    anios = anios or anios_por_defecto(hoy)
    if obtener is None:
        sesion = crear_sesion()

        def obtener(codigo: str, anio: int) -> dict[str, Any]:
            return obtener_serie(codigo, anio, sesion)

    nuevos = extraer_y_transformar(anios, obtener)
    historico, cambios = carga.combinar(carga.leer_historico(ruta_historico), nuevos)
    resumen = carga.construir_resumen(historico, hoy, ahora)
    log.info(
        "%s filas nuevas, %s actualizadas, %s registros en total",
        cambios.nuevas,
        cambios.actualizadas,
        len(historico),
    )

    if not dry_run:
        carga.escribir_historico(historico, ruta_historico)
        carga.escribir_resumen(resumen, ruta_resumen)
    resultado = Resultado(len(nuevos), cambios, len(historico), not dry_run)
    escribir_resumen_de_ejecucion(resultado, resumen)
    return resultado


def escribir_resumen_de_ejecucion(resultado: Resultado, resumen: dict[str, Any]) -> None:
    """Agrega una tabla al resumen del run cuando corre en GitHub Actions."""
    destino = os.environ.get("GITHUB_STEP_SUMMARY")
    if not destino:
        return
    lineas = [
        "### Pipeline de indicadores",
        "",
        f"- Filas extraídas: {resultado.filas_extraidas}",
        f"- Nuevas: {resultado.cambios.nuevas} · actualizadas: {resultado.cambios.actualizadas}",
        f"- Registros en el histórico: {resultado.registros}",
        f"- Archivos escritos: {'sí' if resultado.escrito else 'no (dry run)'}",
        "",
        "| Indicador | Fecha | Último valor | Variación |",
        "|---|---|---|---|",
    ]
    for i in resumen["indicadores"]:
        variacion = "–" if i["variacion"] is None else f"{i['variacion']:+.2f} %"
        lineas.append(
            f"| {i['nombre']} | {i['ultimo']['fecha']} | {i['ultimo']['valor']} | {variacion} |"
        )
    with open(destino, "a", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")


__all__ = ["ErrorDeCalidad", "ErrorDeExtraccion", "Resultado", "ejecutar"]
