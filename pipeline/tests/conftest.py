from datetime import date, timedelta

import pytest


def respuesta(codigo: str, valores: dict[str, float]) -> dict:
    """Respuesta con la forma de la API: fechas como medianoche de Chile en UTC."""
    return {
        "version": "1.7.0",
        "autor": "mindicador.cl",
        "codigo": codigo,
        "nombre": codigo,
        "unidad_medida": "Pesos",
        "serie": [{"fecha": f"{fecha}T03:00:00.000Z", "valor": v} for fecha, v in valores.items()],
    }


def dias(desde: date, cantidad: int, valor_inicial: float, paso: float = 1.0) -> dict[str, float]:
    return {
        (desde + timedelta(days=i)).isoformat(): round(valor_inicial + i * paso, 2)
        for i in range(cantidad)
    }


VALORES_BASE = {"dolar": 900.0, "euro": 1000.0, "uf": 39_000.0, "libra_cobre": 4.0}


@pytest.fixture
def api_falsa():
    """Extractor falso que devuelve 400 días de datos para cada indicador."""
    llamadas = []

    def obtener(codigo: str, anio: int) -> dict:
        llamadas.append((codigo, anio))
        inicio = date(anio, 1, 1)
        fin = min(date(anio, 12, 31), date(2026, 10, 23))
        cantidad = (fin - inicio).days + 1
        paso = 0.01 if codigo == "libra_cobre" else 1.0
        return respuesta(codigo, dias(inicio, cantidad, VALORES_BASE[codigo], paso))

    obtener.llamadas = llamadas
    return obtener
