import { withBase } from "../utils/url";

export const idiomas = ["es", "en"] as const;
export type Idioma = (typeof idiomas)[number];

export const localeDe: Record<Idioma, string> = { es: "es-CL", en: "en-US" };

// Rutas de cada página en los dos idiomas. El español no lleva prefijo.
export const rutas = {
    inicio: (lang: Idioma) => withBase(lang === "es" ? "/" : "/en/"),
    caso: (lang: Idioma, slug: string) => withBase(lang === "es" ? `/casos/${slug}/` : `/en/cases/${slug}/`),
};

export function seccion(lang: Idioma, id: string): string {
    return `${rutas.inicio(lang)}#${id}`;
}
