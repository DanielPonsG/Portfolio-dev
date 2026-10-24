"""Configuración del pipeline: indicadores, rutas y parámetros de la fuente."""

from dataclasses import dataclass
from pathlib import Path

API_BASE = "https://mindicador.cl/api"
ZONA_HORARIA = "America/Santiago"

RAIZ_REPO = Path(__file__).resolve().parents[2]
RUTA_HISTORICO = RAIZ_REPO / "data" / "indicadores.csv"
RUTA_RESUMEN = RAIZ_REPO / "src" / "data" / "indicadores.json"

# Días de historia que se publican en el resumen para los gráficos del sitio.
DIAS_SERIE = 365
# Período de comparación de la variación que se muestra junto al último valor.
DIAS_VARIACION = 30


@dataclass(frozen=True)
class Indicador:
    codigo: str
    nombre: str
    unidad: str
    decimales: int
    # Rango de valores plausibles. Un valor fuera de rango detiene el pipeline
    # antes de escribir, en vez de publicar un dato corrupto.
    minimo: float
    maximo: float


INDICADORES = {
    i.codigo: i
    for i in (
        Indicador("dolar", "Dólar observado", "CLP", 2, 300, 2_000),
        Indicador("euro", "Euro", "CLP", 2, 300, 2_500),
        Indicador("uf", "Unidad de Fomento (UF)", "CLP", 2, 10_000, 100_000),
        Indicador("libra_cobre", "Cobre (libra)", "USD", 2, 1, 20),
    )
}
