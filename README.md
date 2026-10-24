# Portfolio Daniel Pons

Sitio personal de Daniel Pons, Ingeniero Informático enfocado en automatización, integraciones y Data Engineering.

Publicado en **https://danielponsg.github.io/Portfolio-dev/**

## Stack

- [Astro](https://astro.build) 7, sitio estático
- [Tailwind CSS](https://tailwindcss.com) 4
- GitHub Actions para CI/CD y GitHub Pages como hosting
- Python 3.13, Pandas y pytest para el pipeline de datos

## Desarrollo local

Requiere Node.js 22.12 o superior. CI usa Node 24 LTS (ver `.nvmrc`).

```bash
npm ci              # instala las dependencias exactas del lockfile
npm run dev         # http://localhost:4321/Portfolio-dev/
npm run check       # revisa tipos y plantillas
npm run build       # genera dist/
npm run check:links # revisa que los enlaces internos de dist/ existan
npm run preview     # sirve dist/ para revisar el resultado final
```

## CI/CD

El workflow [`ci-cd.yml`](.github/workflows/ci-cd.yml) corre en cada pull request y en cada push a `main`:

1. `npm ci`, `astro check`, `astro build` y revisión de enlaces internos.
2. Solo en `main`: publica `dist/` en GitHub Pages.

Dependabot propone actualizaciones de dependencias y de las acciones de GitHub.

## Pipeline de indicadores

La sección *Pipeline en vivo* del sitio la alimenta un ETL en Python que está en [`pipeline/`](pipeline):

1. **Extracción** ([`extraccion.py`](pipeline/indicadores/extraccion.py)): descarga de la API pública de
   [mindicador.cl](https://mindicador.cl) el dólar, el euro, la UF y el cobre del año actual y del anterior,
   con reintentos y espera exponencial.
2. **Transformación** ([`transformacion.py`](pipeline/indicadores/transformacion.py)): normaliza las fechas y
   valida tipos, rangos plausibles y fechas duplicadas con Pandas. Si algo falla, el pipeline se detiene sin
   escribir nada.
3. **Carga** ([`carga.py`](pipeline/indicadores/carga.py)): hace un upsert idempotente sobre el histórico
   versionado [`data/indicadores.csv`](data/indicadores.csv) y genera `src/data/indicadores.json`, que el sitio
   lee al compilar.

El workflow [`pipeline.yml`](.github/workflows/pipeline.yml) lo ejecuta cada lunes, hace commit de los datos y
lanza el despliegue del sitio. En los pull requests que tocan el pipeline corre ruff, pytest y una extracción
real sin escribir (`--dry-run`).

```bash
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest && ruff check .
python -m indicadores --dry-run   # extrae y valida sin escribir
python -m indicadores             # actualiza data/ y src/data/
```

### Publicar en otra URL

`astro.config.mjs` lee `SITE` y `BASE` del entorno. Para un dominio propio o para el repositorio
`DanielPonsG.github.io`, basta con definir `BASE=/` (y `SITE` con la URL nueva) en el workflow.
