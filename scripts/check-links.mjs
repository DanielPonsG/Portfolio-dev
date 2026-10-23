// Revisa que todos los enlaces y recursos internos del sitio generado existan
// en dist/. Así un error como el de las imágenes con /public/ en la ruta se
// detecta en CI y no en producción.
import { readdir, readFile, access } from 'node:fs/promises';
import { join } from 'node:path';

const DIST = 'dist';
const BASE = (process.env.BASE ?? '/Portfolio-dev').replace(/\/$/, '');

async function htmlFiles(dir) {
	const entries = await readdir(dir, { withFileTypes: true });
	const files = await Promise.all(
		entries.map((e) => {
			const path = join(dir, e.name);
			if (e.isDirectory()) return htmlFiles(path);
			return e.name.endsWith('.html') ? [path] : [];
		}),
	);
	return files.flat();
}

async function exists(path) {
	try {
		await access(path);
		return true;
	} catch {
		return false;
	}
}

const errores = [];
for (const file of await htmlFiles(DIST)) {
	const html = await readFile(file, 'utf8');
	const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
	for (const [, url] of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
		if (/^(https?:|mailto:|tel:|data:)/.test(url)) continue;
		if (url.startsWith('#')) {
			if (url.length > 1 && !ids.has(url.slice(1))) errores.push(`${file}: ancla inexistente ${url}`);
			continue;
		}
		const path = url.split(/[?#]/)[0];
		if (!path.startsWith(`${BASE}/`) && path !== BASE) {
			errores.push(`${file}: ruta fuera del base path ${url}`);
			continue;
		}
		const relative = path.slice(BASE.length) || '/';
		const target = relative.endsWith('/') ? join(DIST, relative, 'index.html') : join(DIST, relative);
		if (!(await exists(target)) && !(await exists(join(DIST, relative, 'index.html')))) {
			errores.push(`${file}: no existe ${url}`);
		}
	}
}

if (errores.length) {
	console.error(errores.join('\n'));
	process.exit(1);
}
console.log('Enlaces internos OK');
