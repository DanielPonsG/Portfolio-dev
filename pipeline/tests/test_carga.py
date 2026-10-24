import json
from datetime import UTC, date, datetime

import pandas as pd

from indicadores.carga import (
    combinar,
    construir_resumen,
    escribir_historico,
    escribir_resumen,
    leer_historico,
)


def tabla(filas: list[tuple[str, str, float]]) -> pd.DataFrame:
    return pd.DataFrame(filas, columns=["fecha", "indicador", "valor"])


def test_combinar_agrega_actualiza_y_es_idempotente():
    historico = tabla([("2026-01-01", "dolar", 900.0), ("2026-01-02", "dolar", 901.0)])
    nuevos = tabla([("2026-01-02", "dolar", 905.0), ("2026-01-03", "dolar", 902.0)])

    combinado, cambios = combinar(historico, nuevos)
    assert combinado["valor"].tolist() == [900.0, 905.0, 902.0]
    assert (cambios.nuevas, cambios.actualizadas) == (1, 1)

    otra_vez, cambios = combinar(combinado, nuevos)
    pd.testing.assert_frame_equal(otra_vez, combinado)
    assert (cambios.nuevas, cambios.actualizadas) == (0, 0)


def test_combinar_con_historico_vacio(tmp_path):
    vacio = leer_historico(tmp_path / "no-existe.csv")
    combinado, cambios = combinar(vacio, tabla([("2026-01-01", "uf", 39_000.0)]))
    assert len(combinado) == 1
    assert cambios.nuevas == 1


def test_resumen_ignora_fechas_futuras_y_calcula_variacion():
    historico = tabla(
        [
            ("2026-09-01", "uf", 39_000.0),
            ("2026-10-01", "uf", 39_100.0),
            ("2026-10-23", "uf", 39_390.0),
            # La UF se conoce por adelantado: no es el "último" valor de hoy.
            ("2026-11-09", "uf", 39_500.0),
        ]
    )
    resumen = construir_resumen(historico, date(2026, 10, 23), datetime(2026, 10, 23, tzinfo=UTC))

    (uf,) = resumen["indicadores"]
    assert uf["ultimo"] == {"fecha": "2026-10-23", "valor": 39_390.0}
    # 30 días antes del 23-10 es el 23-09; el último valor disponible es el del 01-09.
    assert uf["variacion"] == 1.0
    assert [fecha for fecha, _ in uf["serie"]] == ["2026-09-01", "2026-10-01", "2026-10-23"]
    assert resumen["registros"] == 4


def test_resumen_sin_historia_suficiente_no_calcula_variacion():
    historico = tabla([("2026-10-20", "dolar", 900.0), ("2026-10-23", "dolar", 910.0)])
    resumen = construir_resumen(historico, date(2026, 10, 23), datetime(2026, 10, 23, tzinfo=UTC))
    assert resumen["indicadores"][0]["variacion"] is None


def test_escritura_y_lectura_conservan_los_datos(tmp_path):
    historico = tabla([("2026-01-01", "dolar", 900.5), ("2026-01-01", "uf", 39_000.12)])
    ruta = tmp_path / "data" / "indicadores.csv"
    escribir_historico(historico, ruta)
    pd.testing.assert_frame_equal(leer_historico(ruta), historico)

    resumen = construir_resumen(historico, date(2026, 1, 1), datetime(2026, 1, 1, tzinfo=UTC))
    ruta_json = tmp_path / "src" / "data" / "indicadores.json"
    escribir_resumen(resumen, ruta_json)
    assert json.loads(ruta_json.read_text(encoding="utf-8")) == resumen
    assert not list(tmp_path.rglob("*.tmp"))
