import json
from datetime import UTC, datetime

import pytest

from indicadores.pipeline import ErrorDeCalidad, ejecutar

from .conftest import respuesta

AHORA = datetime(2026, 10, 23, 15, 0, tzinfo=UTC)


def test_ejecucion_completa_escribe_historico_y_resumen(tmp_path, api_falsa):
    historico = tmp_path / "indicadores.csv"
    resumen = tmp_path / "indicadores.json"

    resultado = ejecutar(
        obtener=api_falsa, ruta_historico=historico, ruta_resumen=resumen, ahora=AHORA
    )

    assert {anio for _, anio in api_falsa.llamadas} == {2025, 2026}
    assert resultado.escrito
    assert resultado.cambios.nuevas == resultado.registros == resultado.filas_extraidas
    datos = json.loads(resumen.read_text(encoding="utf-8"))
    assert [i["codigo"] for i in datos["indicadores"]] == ["dolar", "euro", "uf", "libra_cobre"]
    assert all(i["ultimo"]["fecha"] == "2026-10-23" for i in datos["indicadores"])
    assert all(len(i["serie"]) == 366 for i in datos["indicadores"])

    # Una segunda corrida con los mismos datos no agrega ni cambia filas.
    otra = ejecutar(obtener=api_falsa, ruta_historico=historico, ruta_resumen=resumen, ahora=AHORA)
    assert (otra.cambios.nuevas, otra.cambios.actualizadas) == (0, 0)


def test_dry_run_no_escribe(tmp_path, api_falsa):
    resultado = ejecutar(
        dry_run=True,
        obtener=api_falsa,
        ruta_historico=tmp_path / "indicadores.csv",
        ruta_resumen=tmp_path / "indicadores.json",
        ahora=AHORA,
    )
    assert not resultado.escrito
    assert not list(tmp_path.iterdir())


def test_un_dato_invalido_detiene_todo_sin_escribir(tmp_path, api_falsa):
    def obtener(codigo, anio):
        if codigo == "uf":
            return respuesta("uf", {"2026-10-23": -1.0})
        return api_falsa(codigo, anio)

    with pytest.raises(ErrorDeCalidad, match="uf"):
        ejecutar(
            obtener=obtener,
            ruta_historico=tmp_path / "indicadores.csv",
            ruta_resumen=tmp_path / "indicadores.json",
            ahora=AHORA,
        )
    assert not list(tmp_path.iterdir())


def test_resumen_de_github_actions(tmp_path, api_falsa, monkeypatch):
    resumen_run = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(resumen_run))
    ejecutar(dry_run=True, obtener=api_falsa, ahora=AHORA)
    contenido = resumen_run.read_text(encoding="utf-8")
    assert "| Dólar observado | 2026-10-23 |" in contenido
    assert "no (dry run)" in contenido
