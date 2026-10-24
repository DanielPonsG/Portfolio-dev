import pytest
import requests

from indicadores.extraccion import INTENTOS, ErrorDeExtraccion, obtener_serie


class RespuestaFalsa:
    def __init__(self, status_code: int, datos=None):
        self.status_code = status_code
        self._datos = datos

    def json(self):
        if self._datos is None:
            raise ValueError("sin JSON")
        return self._datos


class SesionFalsa:
    def __init__(self, respuestas):
        self.respuestas = list(respuestas)
        self.urls = []

    def get(self, url, timeout):
        self.urls.append(url)
        respuesta = self.respuestas.pop(0)
        if isinstance(respuesta, Exception):
            raise respuesta
        return respuesta


def test_reintenta_errores_de_red_y_5xx():
    esperas = []
    sesion = SesionFalsa(
        [
            requests.ConnectionError("sin red"),
            RespuestaFalsa(503),
            RespuestaFalsa(200, {"codigo": "dolar", "serie": []}),
        ]
    )
    datos = obtener_serie("dolar", 2026, sesion, esperar=esperas.append)
    assert datos["codigo"] == "dolar"
    assert sesion.urls == ["https://mindicador.cl/api/dolar/2026"] * 3
    assert esperas == [2, 4]


def test_falla_despues_del_ultimo_intento():
    sesion = SesionFalsa([RespuestaFalsa(502)] * INTENTOS)
    with pytest.raises(ErrorDeExtraccion, match="HTTP 502"):
        obtener_serie("dolar", 2026, sesion, esperar=lambda _: None)


def test_no_reintenta_errores_4xx():
    sesion = SesionFalsa([RespuestaFalsa(404)])
    with pytest.raises(ErrorDeExtraccion, match="404"):
        obtener_serie("dolar", 2026, sesion, esperar=lambda _: None)
    assert len(sesion.urls) == 1


@pytest.mark.parametrize("datos", [None, [], {"codigo": "dolar"}])
def test_rechaza_respuestas_sin_serie(datos):
    sesion = SesionFalsa([RespuestaFalsa(200, datos)])
    with pytest.raises(ErrorDeExtraccion):
        obtener_serie("dolar", 2026, sesion, esperar=lambda _: None)
