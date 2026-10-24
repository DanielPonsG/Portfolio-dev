import datos from "../data/indicadores.json";
import { localeDe, type Idioma } from "../i18n";

// El pipeline de /pipeline escribe src/data/indicadores.json en cada ejecución.
export interface Indicador {
    codigo: string;
    nombre: string;
    unidad: string;
    decimales: number;
    ultimo: { fecha: string; valor: number };
    variacion: number | null;
    serie: [string, number][];
}

interface Resumen {
    generado: string | null;
    registros: number;
    dias_variacion: number;
    indicadores: Indicador[];
}

// TypeScript infiere cada punto de la serie como (string | number)[] y no como
// tupla, así que el JSON se convierte pasando por unknown.
export const resumen = datos as unknown as Resumen;

// El pipeline publica los nombres en español; estos son los de la versión en inglés.
const nombresEn: Record<string, string> = {
    dolar: "US dollar (observed)",
    euro: "Euro",
    uf: "UF (indexed unit)",
    libra_cobre: "Copper (per pound)",
};

export const nombre = (indicador: Indicador, lang: Idioma) =>
    lang === "en" ? (nombresEn[indicador.codigo] ?? indicador.nombre) : indicador.nombre;

export function formatos(lang: Idioma) {
    const locale = localeDe[lang];
    const porcentaje = new Intl.NumberFormat(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return {
        moneda: (valor: number, unidad: string, decimales: number) =>
            new Intl.NumberFormat(locale, {
                style: "currency",
                currency: unidad,
                minimumFractionDigits: decimales,
                maximumFractionDigits: decimales,
            }).format(valor),
        dia: (iso: string) =>
            new Intl.DateTimeFormat(locale, { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }).format(
                new Date(`${iso}T00:00:00Z`),
            ),
        fechaHora: (iso: string) =>
            new Intl.DateTimeFormat(locale, { dateStyle: "long", timeStyle: "short", timeZone: "America/Santiago" }).format(
                new Date(iso),
            ),
        entero: (valor: number) => valor.toLocaleString(locale),
        porcentaje: (valor: number) => `${porcentaje.format(valor)} %`,
    };
}

// Geometría de una sparkline en unidades de su viewBox.
export function sparkline(serie: [string, number][], ancho: number, alto: number, margen = 6) {
    const valores = serie.map(([, valor]) => valor);
    const minimo = Math.min(...valores);
    const maximo = Math.max(...valores);
    const rango = maximo - minimo || 1;
    const paso = (ancho - 2 * margen) / Math.max(serie.length - 1, 1);
    const puntos = valores.map((valor, i) => [
        +(margen + i * paso).toFixed(1),
        +(margen + ((maximo - valor) / rango) * (alto - 2 * margen)).toFixed(1),
    ]);
    const linea = puntos.map(([x, y], i) => `${i ? "L" : "M"}${x},${y}`).join("");
    const [primero] = puntos;
    const ultimo = puntos[puntos.length - 1];
    const area = `${linea}L${ultimo[0]},${alto}L${primero[0]},${alto}Z`;
    return { puntos, linea, area, ultimo, minimo, maximo };
}
