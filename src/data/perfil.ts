import type { Idioma } from "../i18n";

// Experiencia, stack, proyectos y formación, en los dos idiomas.

export interface Trabajo {
    cargo: string;
    empresa: string;
    fecha: string;
    logros: string[];
}

export const experiencia: Record<Idioma, Trabajo[]> = {
    es: [
        {
            cargo: "Desarrollador RPA y Automatización",
            empresa: "Vinci Compass",
            fecha: "Diciembre 2025 - Presente",
            logros: [
                "Migro procesos operativos desde robots RPA (Rocketbot) a pipelines en Python orquestados con Prefect, con modo de ensayo, reintentos y trazabilidad de cada corrida.",
                "Desarrollo procesos ETL con Pandas: extracción desde archivos de custodios, planillas y APIs; validación y conciliación; y carga masiva en la plataforma de inversiones.",
                "Integro las APIs de Addepar, Salesforce, Monday, Microsoft Graph (SharePoint), SendGrid y Bloomberg.",
                "Reduje en un 70% el tiempo de ejecución de un flujo crítico corporativo.",
                "Desarrollé un SDK interno en Python (contexto de ejecución, reintentos, logging e integraciones) para estandarizar las automatizaciones del equipo.",
                "Implemento CI/CD con GitHub Actions: pruebas con pytest, lint con ruff y despliegue automático a los servidores de ejecución.",
            ],
        },
        {
            cargo: "Desarrollador Web",
            empresa: "Zenitx",
            fecha: "Octubre 2022 - Febrero 2023",
            logros: [
                "Participé en el desarrollo de una plataforma de e-commerce con PHP, JavaScript, HTML y CSS.",
                "Colaboré en las funcionalidades de gestión de productos, carrito de compras y sistemas de pago.",
                "Trabajé con Scrum y usé Git y GitHub para el control de versiones.",
            ],
        },
    ],
    en: [
        {
            cargo: "RPA and Automation Developer",
            empresa: "Vinci Compass",
            fecha: "December 2025 - Present",
            logros: [
                "Migrate operations processes from RPA robots (Rocketbot) to Python pipelines orchestrated with Prefect, with a dry-run mode, retries and traceability for every run.",
                "Build ETL processes with Pandas: extraction from custodian files, spreadsheets and APIs; validation and reconciliation; and bulk loads into the investment platform.",
                "Integrate the Addepar, Salesforce, Monday, Microsoft Graph (SharePoint), SendGrid and Bloomberg APIs.",
                "Cut the run time of a critical corporate workflow by 70%.",
                "Built an internal Python SDK (run context, retries, logging and integrations) to standardize the team's automations.",
                "Run CI/CD with GitHub Actions: tests with pytest, linting with ruff and automated deployment to the execution servers.",
            ],
        },
        {
            cargo: "Web Developer",
            empresa: "Zenitx",
            fecha: "October 2022 - February 2023",
            logros: [
                "Helped build an e-commerce platform with PHP, JavaScript, HTML and CSS.",
                "Worked on product management, shopping cart and payment features.",
                "Worked in Scrum and used Git and GitHub for version control.",
            ],
        },
    ],
};

export interface Capa {
    titulo: string;
    descripcion: string;
    items: string[];
}

export const stack: Record<Idioma, Capa[]> = {
    es: [
        { titulo: "Lenguajes", descripcion: "Base para pipelines, scripts y servicios.", items: ["Python", "SQL", "JavaScript", "TypeScript", "PHP"] },
        {
            titulo: "Procesamiento de datos",
            descripcion: "Extracción, limpieza, validación y carga.",
            items: ["Pandas", "ETL", "Conciliación de datos", "Excel y CSV", "Archivos de ancho fijo"],
        },
        {
            titulo: "Orquestación y automatización",
            descripcion: "Ejecución programada o bajo demanda, con reintentos y trazabilidad.",
            items: ["Prefect", "GitHub Actions", "Rocketbot (Xperience y Orchestrator)", "Webhooks"],
        },
        {
            titulo: "Integraciones",
            descripcion: "APIs empresariales y servicios de terceros.",
            items: ["APIs REST", "GraphQL", "Addepar", "Salesforce", "Monday", "Microsoft Graph y SharePoint", "SendGrid", "Bloomberg"],
        },
        {
            titulo: "Bases de datos y analítica",
            descripcion: "Modelado, consultas y visualización.",
            items: ["PostgreSQL", "NoSQL", "Power BI", "Hadoop, HDFS y Hive (académico)", "AWS (académico)"],
        },
        {
            titulo: "Calidad y DevOps",
            descripcion: "Código probado, revisado y desplegado automáticamente.",
            items: ["pytest", "ruff", "Git y GitHub", "CI/CD", "Azure Key Vault", "Windows y Linux"],
        },
        { titulo: "Desarrollo web", descripcion: "Interfaces y aplicaciones completas.", items: ["Astro", "Tailwind CSS", "Django", "Bootstrap", "HTML y CSS"] },
    ],
    en: [
        { titulo: "Languages", descripcion: "The base for pipelines, scripts and services.", items: ["Python", "SQL", "JavaScript", "TypeScript", "PHP"] },
        {
            titulo: "Data processing",
            descripcion: "Extraction, cleaning, validation and loading.",
            items: ["Pandas", "ETL", "Data reconciliation", "Excel and CSV", "Fixed-width files"],
        },
        {
            titulo: "Orchestration and automation",
            descripcion: "Scheduled or on-demand runs, with retries and traceability.",
            items: ["Prefect", "GitHub Actions", "Rocketbot (Xperience and Orchestrator)", "Webhooks"],
        },
        {
            titulo: "Integrations",
            descripcion: "Enterprise APIs and third-party services.",
            items: ["REST APIs", "GraphQL", "Addepar", "Salesforce", "Monday", "Microsoft Graph and SharePoint", "SendGrid", "Bloomberg"],
        },
        {
            titulo: "Databases and analytics",
            descripcion: "Modeling, querying and visualization.",
            items: ["PostgreSQL", "NoSQL", "Power BI", "Hadoop, HDFS and Hive (academic)", "AWS (academic)"],
        },
        {
            titulo: "Quality and DevOps",
            descripcion: "Code that is tested, reviewed and deployed automatically.",
            items: ["pytest", "ruff", "Git and GitHub", "CI/CD", "Azure Key Vault", "Windows and Linux"],
        },
        { titulo: "Web development", descripcion: "Interfaces and full applications.", items: ["Astro", "Tailwind CSS", "Django", "Bootstrap", "HTML and CSS"] },
    ],
};

export interface Proyecto {
    titulo: string;
    descripcion: string;
    imagen?: string;
    enlace?: string;
    tags: string[];
}

export const proyectos: Record<Idioma, Proyecto[]> = {
    es: [
        {
            titulo: "Este sitio y su pipeline de datos",
            descripcion:
                "Sitio estático bilingüe con modo claro y oscuro. Cada cambio pasa por chequeo de tipos, build y verificación de enlaces, y se publica en GitHub Pages. Un ETL en Python lo actualiza cada semana con datos reales.",
            imagen: "/projects/portfolio.webp",
            enlace: "https://github.com/DanielPonsG/Portfolio-dev",
            tags: ["Astro", "Tailwind CSS", "Python", "Pandas", "GitHub Actions"],
        },
        {
            titulo: "SAM · Sistema de gestión académica",
            descripcion:
                "Aplicación web full stack para colegios: estudiantes, profesores, asignaturas, notas, asistencia, calendario y libro de anotaciones, con permisos por rol (dirección, profesores y apoderados). Base de datos PostgreSQL en Supabase y despliegue en Vercel.",
            tags: ["Python", "Django", "PostgreSQL (Supabase)", "Vercel"],
        },
    ],
    en: [
        {
            titulo: "This site and its data pipeline",
            descripcion:
                "A bilingual static site with light and dark modes. Every change goes through type checking, a build and a link check, and is published to GitHub Pages. A Python ETL refreshes it every week with real data.",
            imagen: "/projects/portfolio.webp",
            enlace: "https://github.com/DanielPonsG/Portfolio-dev",
            tags: ["Astro", "Tailwind CSS", "Python", "Pandas", "GitHub Actions"],
        },
        {
            titulo: "SAM · School management system",
            descripcion:
                "A full-stack web app for schools: students, teachers, subjects, grades, attendance, calendar and conduct records, with role-based permissions (principals, teachers and guardians). PostgreSQL database on Supabase, deployed on Vercel.",
            tags: ["Python", "Django", "PostgreSQL (Supabase)", "Vercel"],
        },
    ],
};

export interface Formacion {
    titulos: { titulo: string; institucion: string; fecha: string }[];
    certificados: string[];
    cursos: string[];
}

export const formacion: Record<Idioma, Formacion> = {
    es: {
        titulos: [
            { titulo: "Ingeniería Informática", institucion: "INACAP", fecha: "Marzo 2023 - Agosto 2025" },
            { titulo: "Analista Programador", institucion: "INACAP", fecha: "Marzo 2020 - Julio 2022" },
        ],
        certificados: [
            "Arquitectura Cloud",
            "Diseño y Gestión de Base de Datos",
            "Desarrollador Full Stack",
            "Diseño Ágil de Sistemas",
            "Soporte Computacional",
        ],
        cursos: [
            "Bases de datos relacionales y no estructuradas",
            "Big Data",
            "Minería de datos",
            "Inteligencia artificial",
            "Tecnología cloud",
            "Seguridad de la información",
            "Ingeniería de software",
            "Desarrollo front end y back end",
            "Metodologías ágiles",
        ],
    },
    en: {
        titulos: [
            { titulo: "Computer Engineering", institucion: "INACAP", fecha: "March 2023 - August 2025" },
            { titulo: "Programmer Analyst", institucion: "INACAP", fecha: "March 2020 - July 2022" },
        ],
        certificados: [
            "Cloud Architecture",
            "Database Design and Management",
            "Full Stack Developer",
            "Agile Systems Design",
            "Computer Support",
        ],
        cursos: [
            "Relational and non-relational databases",
            "Big Data",
            "Data mining",
            "Artificial intelligence",
            "Cloud technology",
            "Information security",
            "Software engineering",
            "Front-end and back-end development",
            "Agile methodologies",
        ],
    },
};
