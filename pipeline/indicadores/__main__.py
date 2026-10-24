"""Uso: python -m indicadores [--anios 2025 2026] [--dry-run]"""

import argparse
import logging
import sys

from .pipeline import ErrorDeCalidad, ErrorDeExtraccion, ejecutar


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline ETL de indicadores económicos")
    parser.add_argument(
        "--anios", type=int, nargs="+", help="años a extraer (por defecto, el actual y el anterior)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="extrae y valida sin escribir archivos"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        ejecutar(anios=args.anios, dry_run=args.dry_run)
    except (ErrorDeExtraccion, ErrorDeCalidad) as error:
        logging.error("El pipeline se detuvo sin escribir cambios: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
