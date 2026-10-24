import type { Idioma } from "../i18n";

// Casos basados en mi trabajo actual. Los nombres de clientes, bancos y
// sistemas internos se omiten a propósito.
export interface Caso {
    slug: string;
    area: string;
    titulo: string;
    resumen: string;
    problema: string;
    solucion: string;
    resultado: string;
    flujo: string[];
    stack: string[];
}

export const casos: Record<Idioma, Caso[]> = {
    es: [
        {
            slug: "migracion-rpa-a-prefect",
            area: "Orquestación",
            titulo: "Migración de robots RPA a pipelines orquestados",
            resumen: "Procesos de operaciones reescritos en Python y Prefect, con pruebas, modo de ensayo y despliegue automático.",
            problema:
                "Los procesos de operaciones corrían en robots RPA difíciles de probar, versionar y monitorear.",
            solucion:
                "Reescribo cada proceso como un flujo de Python orquestado con Prefect, separado en capas (configuración, entrada, reglas de negocio, salida y métricas). Cada flujo tiene un modo de ensayo que no escribe en los sistemas de negocio, lee sus secretos desde Azure Key Vault y se despliega con GitHub Actions después de pasar pytest y ruff.",
            resultado: "Más de 15 procesos versionados, con pruebas y trazabilidad de cada corrida.",
            flujo: ["Solicitud", "Enrutador", "Prefect", "Python y Pandas", "APIs y archivos", "Notificación"],
            stack: ["Python", "Prefect", "Pandas", "pytest", "ruff", "GitHub Actions", "Azure Key Vault"],
        },
        {
            slug: "enrutador-de-solicitudes",
            area: "Integración",
            titulo: "Enrutador de solicitudes durante la migración",
            resumen: "Un servicio que decide, solicitud por solicitud, si un proceso corre en Prefect o en el robot, sin perder ninguna.",
            problema:
                "Había tres tablas de enrutamiento que nadie validaba entre sí, y el servicio anterior respondía 200 siempre, así que una solicitud mal enrutada se perdía sin aviso.",
            solucion:
                "Servicio en Flask que, por cada solicitud, consulta al orquestador si el proceso tiene un deployment activo: si lo tiene, crea la corrida en Prefect; si no, la envía a la cola del robot RPA. Si el orquestador no responde devuelve 503 para que el origen reintente, y usa una clave de idempotencia para que los reintentos generen una sola ejecución.",
            resultado:
                "Migración gradual sin perder solicitudes. Volver un proceso al robot es pausar su deployment, sin desplegar nada.",
            flujo: ["Webhook", "Flask", "¿Deployment activo?", "Prefect o RPA"],
            stack: ["Python", "Flask", "API de Prefect", "GraphQL"],
        },
        {
            slug: "pipeline-de-custodia",
            area: "ETL",
            titulo: "Pipeline de custodia hacia la plataforma de inversiones",
            resumen: "Transacciones de un banco custodio consolidadas, enriquecidas y cargadas por API, en vez de a mano.",
            problema:
                "Las transacciones trimestrales de un banco custodio internacional se consolidaban y cargaban a mano en la plataforma de reporting de inversiones.",
            solucion:
                "El pipeline lee el archivo comprimido del custodio, consolida los movimientos de caja, controla las cuentas incluidas, resuelve los identificadores de cada entidad con la API de Addepar, genera el template de carga y lo importa por API. Las pruebas de caracterización reprocesan corridas reales de producción para detectar cualquier cambio en el resultado.",
            resultado: "Carga completa y repetible, con validación previa en modo ensayo antes de importar.",
            flujo: ["ZIP del custodio", "Consolidación", "Control de cuentas", "Enriquecimiento", "Carga en Addepar"],
            stack: ["Python", "Pandas", "API de Addepar", "Prefect", "pytest"],
        },
        {
            slug: "reportes-regulatorios-cmf",
            area: "Calidad de datos",
            titulo: "Reportes regulatorios para la CMF",
            resumen: "Ocho archivos normativos generados desde planillas, validados y con trazabilidad completa.",
            problema:
                "Los archivos normativos de ancho fijo se armaban desde planillas Excel con alto riesgo de error de formato.",
            solucion:
                "Flujo que transforma las planillas en los archivos de ancho fijo que exige la norma, genera sus carátulas, valida el resultado y deja trazabilidad con hashes, métricas y respaldo de entradas y salidas en SharePoint.",
            resultado: "Ocho reportes de dos normas generados por un único proceso auditable.",
            flujo: ["Excel", "Reglas de la norma", "Ancho fijo y carátulas", "Validación", "Respaldo"],
            stack: ["Python", "Prefect", "Microsoft Graph", "SendGrid"],
        },
        {
            slug: "archivos-para-custodios",
            area: "Transformación",
            titulo: "Archivos de operaciones para custodios globales",
            resumen: "Un export de Bloomberg convertido en tres layouts distintos, con cada custodio procesado de forma aislada.",
            problema:
                "Las operaciones exportadas desde Bloomberg debían convertirse a mano al formato distinto de cada custodio.",
            solucion:
                "El proceso identifica los custodios presentes según las cuentas del archivo, valida cada contraparte contra su mantenedor y genera tres layouts distintos (CSV de 47 campos, Excel de 33 y de 82 columnas). Cada custodio se procesa aislado: si uno falla, los demás igual reciben su archivo y la corrida termina como parcial.",
            resultado:
                "Un solo archivo de entrada produce las entregas para todos los custodios, con fallos aislados.",
            flujo: ["Export Bloomberg", "Detección de custodio", "Validación", "3 layouts", "Envío"],
            stack: ["Python", "Pandas", "Prefect", "SendGrid"],
        },
    ],
    en: [
        {
            slug: "migracion-rpa-a-prefect",
            area: "Orchestration",
            titulo: "Migrating RPA robots to orchestrated pipelines",
            resumen: "Operations processes rewritten in Python and Prefect, with tests, a dry-run mode and automated deployment.",
            problema: "Operations processes ran on RPA robots that were hard to test, version and monitor.",
            solucion:
                "I rewrite each process as a Python flow orchestrated by Prefect, split into layers (configuration, input, business rules, output and metrics). Every flow has a dry-run mode that never writes to business systems, reads its secrets from Azure Key Vault and is deployed with GitHub Actions after passing pytest and ruff.",
            resultado: "15+ processes under version control, with tests and traceability for every run.",
            flujo: ["Request", "Router", "Prefect", "Python and Pandas", "APIs and files", "Notification"],
            stack: ["Python", "Prefect", "Pandas", "pytest", "ruff", "GitHub Actions", "Azure Key Vault"],
        },
        {
            slug: "enrutador-de-solicitudes",
            area: "Integration",
            titulo: "Request router during the migration",
            resumen: "A service that decides, request by request, whether a process runs on Prefect or on the robot, without losing any.",
            problema:
                "There were three routing tables nobody kept in sync, and the old service always answered 200, so a misrouted request was silently lost.",
            solucion:
                "A Flask service that, for each request, asks the orchestrator whether the process has an active deployment: if it does, it creates the Prefect run; if not, it sends the request to the RPA robot's queue. When the orchestrator does not answer it returns 503 so the sender retries, and an idempotency key makes retries produce a single run.",
            resultado:
                "A gradual migration with no lost requests. Moving a process back to the robot only takes pausing its deployment, with no redeploy.",
            flujo: ["Webhook", "Flask", "Active deployment?", "Prefect or RPA"],
            stack: ["Python", "Flask", "Prefect API", "GraphQL"],
        },
        {
            slug: "pipeline-de-custodia",
            area: "ETL",
            titulo: "Custody pipeline into the investment platform",
            resumen: "Custodian bank transactions consolidated, enriched and loaded through an API instead of by hand.",
            problema:
                "Quarterly transactions from an international custodian bank were consolidated and loaded by hand into the investment reporting platform.",
            solucion:
                "The pipeline reads the custodian's compressed file, consolidates cash movements, checks which accounts are included, resolves each entity's identifiers through the Addepar API, builds the import template and loads it through the API. Characterization tests replay real production runs to catch any change in the output.",
            resultado: "A complete, repeatable load, validated in dry-run mode before importing.",
            flujo: ["Custodian ZIP", "Consolidation", "Account checks", "Enrichment", "Load into Addepar"],
            stack: ["Python", "Pandas", "Addepar API", "Prefect", "pytest"],
        },
        {
            slug: "reportes-regulatorios-cmf",
            area: "Data quality",
            titulo: "Regulatory reports for Chile's financial regulator (CMF)",
            resumen: "Eight regulatory files generated from spreadsheets, validated and fully traceable.",
            problema:
                "Fixed-width regulatory files were built from Excel spreadsheets with a high risk of formatting errors.",
            solucion:
                "A flow that turns the spreadsheets into the fixed-width files the regulation requires, generates their cover sheets, validates the output and keeps an audit trail with hashes, metrics and backups of inputs and outputs in SharePoint.",
            resultado: "Eight reports from two regulations produced by a single auditable process.",
            flujo: ["Excel", "Regulation rules", "Fixed width and covers", "Validation", "Backup"],
            stack: ["Python", "Prefect", "Microsoft Graph", "SendGrid"],
        },
        {
            slug: "archivos-para-custodios",
            area: "Transformation",
            titulo: "Trade files for global custodians",
            resumen: "One Bloomberg export turned into three different layouts, with each custodian processed in isolation.",
            problema:
                "Trades exported from Bloomberg had to be converted by hand into each custodian's own format.",
            solucion:
                "The process detects which custodians are present from the file's accounts, validates each counterparty against its reference table and produces three different layouts (a 47-field CSV and 33- and 82-column Excel files). Each custodian is processed in isolation: if one fails, the others still get their file and the run ends as partial.",
            resultado: "A single input file produces the deliveries for every custodian, with isolated failures.",
            flujo: ["Bloomberg export", "Custodian detection", "Validation", "3 layouts", "Delivery"],
            stack: ["Python", "Pandas", "Prefect", "SendGrid"],
        },
    ],
};
