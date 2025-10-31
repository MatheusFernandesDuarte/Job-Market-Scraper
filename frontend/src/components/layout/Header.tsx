"use client";

import { LanguageSelector } from "@/components/ui/LanguageSelector";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";

export function Header() {
    const { lang } = useLanguage();
    const t = translations[lang];

    return (
        <header className="flex flex-col md:flex-row md:justify-between md:items-center gap-4">
            <div className="flex-1">
                <h1 className="text-3xl md:text-4xl font-bold text-slate-800 bg-gradient-to-r from-sky-600 to-slate-800 bg-clip-text text-transparent">
                    {t.headerTitle}
                </h1>
                <p className="text-sm md:text-base text-slate-600 mt-2 max-w-2xl">
                    {t.headerSubtitle}
                </p>
                <div className="flex gap-3 mt-3 text-xs text-slate-500">
                    <span className="flex items-center gap-1">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                        {t.statusBadge}
                    </span>
                </div>
            </div>
            <LanguageSelector />
        </header>
    );
}
