import pytest

from indicadores.config import INDICADORES
from indicadores.transformacion import ErrorDeCalidad, normalizar

from .conftest import respuesta

DOLAR = INDICADORES["dolar"]


def test_convierte_la_medianoche_de_chile_en_utc_a_la_fecha_del_dia():
    datos = normalizar(
        {
            "codigo": "dolar",
            "serie": [
                # Horario de verano (UTC-3), de invierno (UTC-4) y medianoche UTC.
                {"fecha": "2026-01-15T03:00:00.000Z", "valor": 950.5},
                {"fecha": "2026-06-10T04:00:00.000Z", "valor": 940.25},
                {"fecha": "2026-07-01T00:00:00.000Z", "valor": 941.0},
            ],
        },
        DOLAR,
    )
    assert datos["fecha"].tolist() == ["2026-01-15", "2026-06-10", "2026-07-01"]
    assert datos["indicador"].unique().tolist() == ["dolar"]
    assert datos["valor"].tolist() == [950.5, 940.25, 941.0]


def test_dias_consecutivos_alrededor_del_cambio_de_hora():
    # Chile pasa a horario de invierno a inicios de abril (UTC-3 a UTC-4).
    serie = {
        "codigo": "dolar",
        "serie": [
            {"fecha": "2026-04-03T03:00:00.000Z", "valor": 950.0},
            {"fecha": "2026-04-06T04:00:00.000Z", "valor": 951.0},
        ],
    }
    assert normalizar(serie, DOLAR)["fecha"].tolist() == ["2026-04-03", "2026-04-06"]


def test_ordena_por_fecha_y_redondea():
    datos = normalizar(respuesta("dolar", {"2026-02-02": 951.239, "2026-02-01": 950.0}), DOLAR)
    assert datos["fecha"].tolist() == ["2026-02-01", "2026-02-02"]
    assert datos["valor"].tolist() == [950.0, 951.24]


def test_serie_vacia_devuelve_tabla_vacia():
    datos = normalizar(respuesta("dolar", {}), DOLAR)
    assert datos.empty
    assert list(datos.columns) == ["fecha", "indicador", "valor"]


def test_descarta_duplicados_identicos():
    serie = respuesta("dolar", {"2026-02-01": 950.0})
    serie["serie"] *= 2
    assert len(normalizar(serie, DOLAR)) == 1


def test_rechaza_fechas_repetidas_con_valores_distintos():
    serie = respuesta("dolar", {"2026-02-01": 950.0})
    serie["serie"].append({"fecha": "2026-02-01T03:00:00.000Z", "valor": 951.0})
    with pytest.raises(ErrorDeCalidad, match="valores distintos"):
        normalizar(serie, DOLAR)


def test_rechaza_valores_fuera_de_rango():
    with pytest.raises(ErrorDeCalidad, match="fuera del rango"):
        normalizar(respuesta("dolar", {"2026-02-01": 95_000.0}), DOLAR)


def test_rechaza_valores_y_fechas_invalidos_y_reporta_todos_los_problemas():
    serie = {
        "codigo": "dolar",
        "serie": [
            {"fecha": "no es fecha", "valor": 950.0},
            {"fecha": "2026-02-01T03:00:00.000Z", "valor": "N/D"},
        ],
    }
    with pytest.raises(ErrorDeCalidad) as error:
        normalizar(serie, DOLAR)
    assert len(error.value.problemas) == 2


def test_rechaza_un_indicador_distinto_al_pedido():
    with pytest.raises(ErrorDeCalidad, match="'euro'"):
        normalizar(respuesta("euro", {"2026-02-01": 1000.0}), DOLAR)
