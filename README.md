# Portfolio Daniel Pons

Sitio personal de Daniel Pons, Ingeniero Informático enfocado en automatización, integraciones y Data Engineering.

Publicado en **https://danielponsg.github.io/Portfolio-dev/**

## Stack

- [Astro](https://astro.build) 7, sitio estático
- [Tailwind CSS](https://tailwindcss.com) 4
- GitHub Actions para CI/CD y GitHub Pages como hosting

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

### Publicar en otra URL

`astro.config.mjs` lee `SITE` y `BASE` del entorno. Para un dominio propio o para el repositorio
`DanielPonsG.github.io`, basta con definir `BASE=/` (y `SITE` con la URL nueva) en el workflow.
