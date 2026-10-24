# Portfolio Daniel Pons

Sitio personal de Daniel Pons, Ingeniero Informático enfocado en automatización, integraciones y Data Engineering.

Publicado en **https://danielponsg.github.io/Portfolio-dev/**

## Stack

- [Astro](https://astro.build) 7, sitio estático
- [Tailwind CSS](https://tailwindcss.com) 4
- GitHub Actions para CI/CD y GitHub Pages como hosting
- Python 3.13, Pandas y pytest para el pipeline de datos

## Estructura del sitio

- Dos idiomas: español en `/` y en `/casos/<caso>/`, inglés en `/en/` y en `/en/cases/<caso>/`. Los textos de la
  interfaz están en [`src/i18n/ui.ts`](src/i18n/ui.ts) y los contenidos (casos, experiencia, stack, proyectos y
  formación) en [`src/data/`](src/data), siempre con una versión por idioma.
- Modo claro y oscuro: los colores son variables CSS en [`src/styles/global.css`](src/styles/global.css). El sitio
  sigue el tema del sistema hasta que el visitante elige uno, y la elección se guarda en `localStorage`.
- Avatar 3D de [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) (Microsoft, licencia MIT, ver
  [`public/avatar/LICENSE.txt`](public/avatar/LICENSE.txt)). La animación del saludo se detiene si el sistema pide
  reducir el movimiento.
- SEO: `hreflang` entre idiomas, sitemap (`@astrojs/sitemap`), datos estructurados `Person` e imágenes para redes en
  [`public/og/`](public/og).

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

1. `npm ci`, `astro check`, `astro build` y revisión de enlaces internos, incluidas las anclas a secciones de otras
   páginas.
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
