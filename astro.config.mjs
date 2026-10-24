// @ts-check
import process from 'node:process';
import { defineConfig } from 'astro/config';

import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
// SITE y BASE permiten publicar en otra URL (dominio propio o repo
// DanielPonsG.github.io) sin tocar el código: basta con cambiar las variables
// de entorno en el workflow de despliegue.
export default defineConfig({
  site: process.env.SITE ?? 'https://danielponsg.github.io',
  base: process.env.BASE ?? '/Portfolio-dev',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
