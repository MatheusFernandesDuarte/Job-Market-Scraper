export const LANGUAGES = {
    pt: {
        code: "pt",
        name: "Português",
        flag: "/flags/americas/br.svg",
    },
    en: {
        code: "en",
        name: "English",
        flag: "/flags/americas/us.svg",
    },
    es: {
        code: "es",
        name: "Español",
        flag: "/flags/europe/es.svg",
    },
    fr: {
        code: "fr",
        name: "Français",
        flag: "/flags/europe/fr.svg",
    },
    de: {
        code: "de",
        name: "Deutsch",
        flag: "/flags/europe/de.svg",
    },
    hi: {
        code: "hi",
        name: "हिन्दी",
        flag: "/flags/asia/in.svg",
    },
    ja: {
        code: "ja",
        name: "日本語",
        flag: "/flags/asia/jp.svg",
    },
    zh: {
        code: "zh",
        name: "简体中文",
        flag: "/flags/asia/cn.svg",
    },
    ko: {
        code: "ko",
        name: "한국어",
        flag: "/flags/asia/kr.svg",
    },
    ru: {
        code: "ru",
        name: "Русский",
        flag: "/flags/europe/ru.svg",
    },
    it: {
        code: "it",
        name: "Italiano",
        flag: "/flags/europe/it.svg",
    },
    nl: {
        code: "nl",
        name: "Nederlands",
        flag: "/flags/europe/nl.svg",
    },
    vi: {
        code: "vi",
        name: "Tiếng Việt",
        flag: "/flags/asia/vn.svg",
    },
    pl: {
        code: "pl",
        name: "Polski",
        flag: "/flags/europe/pl.svg",
    },
    tr: {
        code: "tr",
        name: "Türkçe",
        flag: "/flags/asia/tr.svg",
    },
    sv: {
        code: "sv",
        name: "Svenska",
        flag: "/flags/europe/se.svg",
    },
    id: {
        code: "id",
        name: "Bahasa Indonesia",
        flag: "/flags/asia/id.svg",
    },
    th: {
        code: "th",
        name: "ไทย",
        flag: "/flags/asia/th.svg",
    },
    ar: {
        code: "ar",
        name: "العربية",
        flag: "/flags/middle_east/ae.svg",
    },
    ro: {
        code: "ro",
        name: "Română",
        flag: "/flags/europe/ro.svg",
    },
    cs: {
        code: "cs",
        name: "Čeština",
        flag: "/flags/europe/cz.svg",
    },
    uk: {
        code: "uk",
        name: "Українська",
        flag: "/flags/europe/ua.svg",
    },
    pt_pt: {
        code: "pt_pt",
        name: "Português (PT)",
        flag: "/flags/europe/pt.svg",
    },
    el: {
        code: "el",
        name: "Ελληνικά",
        flag: "/flags/europe/gr.svg",
    },
    he: {
        code: "he",
        name: "עברית",
        flag: "/flags/asia/il.svg",
    },
    es_ar: {
        code: "es_ar",
        name: "Español (AR)",
        flag: "/flags/americas/ar.svg",
    },
    bg: {
        code: "bg",
        name: "Български",
        flag: "/flags/europe/bg.svg",
    },
    fi: {
        code: "fi",
        name: "Suomi",
        flag: "/flags/europe/fi.svg",
    },
} as const;

export type Language = keyof typeof LANGUAGES;
export const LANGUAGE_CODES = Object.keys(LANGUAGES) as Language[];
export const DEFAULT_LANGUAGE: Language = "pt";
