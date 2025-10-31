"use client";

import React, {
    createContext,
    useContext,
    useState,
    useEffect,
    ReactNode,
} from "react";
import { Language, LANGUAGE_CODES, DEFAULT_LANGUAGE } from "@/config/languages";

type LanguageContextType = {
    lang: Language;
    setLang: (val: Language) => void;
};

const LanguageContext = createContext<LanguageContextType | undefined>(
    undefined
);

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [lang, setLang] = useState<Language>(DEFAULT_LANGUAGE);
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        const saved = localStorage.getItem("lang") as Language;
        if (saved && LANGUAGE_CODES.includes(saved)) {
            setLang(saved);
        }
    }, []);

    useEffect(() => {
        if (mounted) {
            localStorage.setItem("lang", lang);
        }
    }, [lang, mounted]);

    return (
        <LanguageContext.Provider value={{ lang, setLang }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const ctx = useContext(LanguageContext);
    if (!ctx)
        throw new Error("useLanguage must be used within a LanguageProvider");
    return ctx;
}
