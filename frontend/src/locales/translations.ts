export const translations = {
    pt: {
        // HEADER
        headerTitle: "Job Market Scraper — Perfil",
        headerSubtitle:
            "Preencha seu perfil para receber vagas ranqueadas por compatibilidade.",

        // RESULTS
        resultsTitle: "Resultados",
        noResultsMessage:
            "Nenhuma vaga encontrada. Submeta o formulário para carregar resultados.",
        viewOnSite: "Ver no site",

        // FORM LABELS
        stack: "Stack Desejada",
        stackHelp: "Separe as tecnologias por vírgula (ex: Python, React, AWS)",
        location: "Localização",
        locationHelp: "Separe locais ou termos por vírgula (ex: Remote, Brazil)",
        seniority: "Senioridade",
        placeholderStack: "Ex: Python, React, AWS, Docker",
        placeholderLocation: "Ex: Remote, Brazil",
        select: "Selecione...",
        button: "Buscar vagas",
        loading: "Buscando...",

        // SENIORITY OPTIONS
        seniorityOptions: [
            { value: "", label: "Selecione..." },
            { value: "junior", label: "Júnior" },
            { value: "mid-level", label: "Pleno" },
            { value: "senior", label: "Sênior" },
            { value: "staff", label: "Staff" },
        ],

        // TABLE HEADERS
        match: "Compatibilidade",
        jobTitle: "Vaga",
        salary: "Salário",
        experience: "Experiência",
        date: "Data",

        // SKILLS
        matched: "Combinadas",
        missing: "Faltando",

        // FOOTER
        footerText: "Job Market Scraper • Matheus Fernandes",
    },

    en: {
        // HEADER
        headerTitle: "Job Market Scraper — Profile",
        headerSubtitle:
            "Fill in your profile to receive ranked job listings by compatibility.",

        // RESULTS
        resultsTitle: "Results",
        noResultsMessage: "No jobs found. Submit the form to load results.",
        viewOnSite: "View on site",

        // FORM LABELS
        stack: "Desired Stack",
        stackHelp: "Separate technologies with commas (e.g. Python, React, AWS)",
        location: "Location",
        locationHelp: "Separate terms with commas (e.g. Remote, Brazil)",
        seniority: "Seniority",
        placeholderStack: "E.g.: Python, React, AWS, Docker",
        placeholderLocation: "E.g.: Remote, Brazil",
        select: "Select...",
        button: "Search jobs",
        loading: "Searching...",

        // SENIORITY OPTIONS
        seniorityOptions: [
            { value: "", label: "Select..." },
            { value: "junior", label: "Junior" },
            { value: "mid-level", label: "Mid-level" },
            { value: "senior", label: "Senior" },
            { value: "staff", label: "Staff" },
        ],

        // TABLE HEADERS
        match: "Match",
        jobTitle: "Job",
        salary: "Salary",
        experience: "Experience",
        date: "Date",

        // SKILLS
        matched: "Matched",
        missing: "Missing",

        // FOOTER
        footerText: "Job Market Scraper • Matheus Fernandes",
    },
    es: {
        // HEADER
        headerTitle: "Job Market Scraper — Perfil",
        headerSubtitle:
            "Completa tu perfil para recibir ofertas de trabajo clasificadas por compatibilidad.",

        // RESULTS
        resultsTitle: "Resultados",
        noResultsMessage: "No se encontraron ofertas. Envía el formulario para cargar resultados.",
        viewOnSite: "Ver en el sitio",

        // FORM LABELS
        stack: "Stack Deseado",
        stackHelp: "Separa las tecnologías por comas (ej: Python, React, AWS)",
        location: "Ubicación",
        locationHelp: "Separa ubicaciones o términos por comas (ej: Remoto, Brasil)",
        seniority: "Seniority",
        placeholderStack: "Ej: Python, React, AWS, Docker",
        placeholderLocation: "Ej: Remoto, Brasil",
        select: "Seleccione...",
        button: "Buscar ofertas",
        loading: "Buscando...",

        // SENIORITY OPTIONS
        seniorityOptions: [
            { value: "", label: "Seleccione..." },
            { value: "junior", label: "Junior" },
            { value: "mid-level", label: "Pleno" },
            { value: "senior", label: "Senior" },
            { value: "staff", label: "Staff" },
        ],

        // TABLE HEADERS
        match: "Compatibilidad",
        jobTitle: "Puesto",
        salary: "Salario",
        experience: "Experiencia",
        date: "Fecha",

        // SKILLS
        matched: "Coinciden",
        missing: "Faltantes",

        // FOOTER
        footerText: "Job Market Scraper • Matheus Fernandes",
    },
} as const;
