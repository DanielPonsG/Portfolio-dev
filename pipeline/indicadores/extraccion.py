"""Extracción: descarga la serie anual de un indicador desde la API pública."""

import logging
import time
from typing import Any

import requests

from .config import API_BASE

log = logging.getLogger(__name__)

INTENTOS = 4
ESPERA_BASE = 2  # segundos; se duplica en cada reintento
TIMEOUT = 30


class ErrorDeExtraccion(Exception):
    """La fuente no entregó una respuesta usable después de los reintentos."""


def crear_sesion() -> requests.Session:
    sesion = requests.Session()
    sesion.headers["User-Agent"] = "portfolio-indicadores (github.com/DanielPonsG/Portfolio-dev)"
    return sesion


def obtener_serie(
    codigo: str,
    anio: int,
    sesion: requests.Session,
    esperar=time.sleep,
) -> dict[str, Any]:
    """Devuelve la respuesta JSON de la API para un indicador y un año.

    Reintenta errores de red y respuestas 5xx con espera exponencial. Un 4xx no
    se reintenta porque no se va a corregir solo.
    """
    url = f"{API_BASE}/{codigo}/{anio}"
    ultimo_error = ""
    for intento in range(1, INTENTOS + 1):
        try:
            respuesta = sesion.get(url, timeout=TIMEOUT)
        except requests.RequestException as error:
            ultimo_error = f"{type(error).__name__}: {error}"
        else:
            if respuesta.status_code < 500:
                if respuesta.status_code != 200:
                    raise ErrorDeExtraccion(f"{url} respondió {respuesta.status_code}")
                try:
                    datos = respuesta.json()
                except ValueError as error:
                    raise ErrorDeExtraccion(f"{url} no devolvió JSON válido") from error
                if not isinstance(datos, dict) or not isinstance(datos.get("serie"), list):
                    raise ErrorDeExtraccion(f"{url} no trae la lista 'serie'")
                return datos
            ultimo_error = f"HTTP {respuesta.status_code}"

        if intento < INTENTOS:
            espera = ESPERA_BASE * 2 ** (intento - 1)
            log.warning("%s falló (%s); reintento en %s s", url, ultimo_error, espera)
            esperar(espera)

    raise ErrorDeExtraccion(f"{url} falló {INTENTOS} veces: {ultimo_error}")
