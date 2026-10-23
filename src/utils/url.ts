// Antepone el base path del sitio (por ejemplo `/Portfolio-dev`) a una ruta
// interna, para que imágenes y enlaces funcionen tanto en local como en
// GitHub Pages.
export function withBase(path: string): string {
	const base = import.meta.env.BASE_URL.replace(/\/$/, '');
	return `${base}/${path.replace(/^\//, '')}`;
}
