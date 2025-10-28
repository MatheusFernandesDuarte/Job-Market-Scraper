"use client";

import React, {
    createContext,
    useContext,
    useState,
    useEffect,
    ReactNode,
} from "react";

type Language = "pt" | "en" | "es";

type LanguageContextType = {
    lang: Language;
    setLang: (val: Language) => void;
};

const LanguageContext = createContext<LanguageContextType | undefined>(
    undefined
);

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [lang, setLang] = useState<Language>(() => {
        if (typeof window !== "undefined") {
            return (localStorage.getItem("lang") as Language) || "pt";
        }
        return "pt";
    });

    useEffect(() => {
        localStorage.setItem("lang", lang);
    }, [lang]);

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
