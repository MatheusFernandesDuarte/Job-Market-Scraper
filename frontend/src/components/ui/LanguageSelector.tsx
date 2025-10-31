"use client";

import { useState, useEffect, useRef, useMemo } from "react";
import { useLanguage } from "@/context/LanguageContext";
import { LANGUAGES, Language } from "@/config/languages";
import { translations } from "@/locales";

const LANGUAGES_BY_CONTINENT = {
    americas: ["pt", "en", "es_ar"],
    europe: ["es", "fr", "de", "it", "nl", "pl", "sv", "ro", "cs", "uk", "pt_pt", "el", "bg", "fi", "ru"],
    asia: ["hi", "ja", "zh", "ko", "vi", "tr", "id", "th", "he"],
    middle_east: ["ar"],
};

export function LanguageSelector() {
    const { lang, setLang } = useLanguage();
    const t = translations[lang];
    const [open, setOpen] = useState(false);
    const [search, setSearch] = useState("");
    const ref = useRef<HTMLDivElement>(null);
    const searchRef = useRef<HTMLInputElement>(null);

    // Nomes dos continentes dinâmicos
    const continentNames: Record<string, string> = {
        americas: t.continentAmericas,
        europe: t.continentEurope,
        asia: t.continentAsia,
        middle_east: t.continentMiddleEast,
    };

    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setOpen(false);
                setSearch("");
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    useEffect(() => {
        if (open && searchRef.current) {
            searchRef.current.focus();
        }
    }, [open]);

    const filteredLanguages = useMemo(() => {
        if (!search) return LANGUAGES_BY_CONTINENT;

        const searchLower = search.toLowerCase();
        const filtered: Record<string, string[]> = {};

        Object.entries(LANGUAGES_BY_CONTINENT).forEach(([continent, codes]) => {
            const matches = codes.filter((code) => {
                const config = LANGUAGES[code as Language];
                return (
                    code.toLowerCase().includes(searchLower) ||
                    config.name.toLowerCase().includes(searchLower)
                );
            });
            if (matches.length > 0) {
                filtered[continent] = matches;
            }
        });

        return filtered;
    }, [search]);

    return (
        <div ref={ref} className="relative inline-block text-left">
            <button
                onClick={() => setOpen((o) => !o)}
                aria-haspopup="listbox"
                aria-expanded={open}
                className="flex items-center gap-2 px-3 py-1.5 rounded-md border border-slate-300 bg-white shadow-sm hover:shadow-md transition-shadow"
            >
                <img
                    src={LANGUAGES[lang].flag}
                    alt={LANGUAGES[lang].name}
                    className="w-5 h-5 object-cover"
                />
                <span className="text-sm font-medium text-sky-600 uppercase">
                    {lang}
                </span>
                <svg
                    className={`w-4 h-4 text-slate-400 transition-transform ${open ? "rotate-180" : ""
                        }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                    />
                </svg>
            </button>

            {open && (
                <div className="absolute mt-1 right-0 rounded-lg border border-slate-200 bg-white shadow-xl w-64 z-50 overflow-hidden">
                    {/* Search input */}
                    <div className="p-2 border-b border-slate-200">
                        <input
                            ref={searchRef}
                            type="text"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            placeholder="Search language..."
                            className="w-full px-3 py-1.5 text-sm border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                        />
                    </div>

                    {/* Scrollable list */}
                    <ul
                        role="listbox"
                        className="max-h-96 overflow-y-auto overscroll-contain"
                        style={{
                            scrollbarWidth: "thin",
                            scrollbarColor: "#cbd5e1 #f1f5f9",
                        }}
                    >
                        {Object.entries(filteredLanguages).map(([continent, codes]) => (
                            <li key={continent}>
                                {/* Continent header */}
                                <div className="sticky top-0 bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-600 uppercase tracking-wide border-b border-slate-200">
                                    {continentNames[continent]}
                                </div>

                                {/* Languages in continent */}
                                {codes.map((code) => {
                                    const config = LANGUAGES[code as Language];
                                    return (
                                        <button
                                            key={code}
                                            onClick={() => {
                                                setLang(code as Language);
                                                setOpen(false);
                                                setSearch("");
                                            }}
                                            className={`w-full flex items-center gap-3 px-3 py-2 text-sm text-left transition-colors ${lang === code
                                                ? "font-semibold text-sky-600 bg-sky-50"
                                                : "text-slate-700 hover:bg-slate-50"
                                                }`}
                                        >
                                            <img
                                                src={config.flag}
                                                alt={`${code} flag`}
                                                className="w-5 h-5 object-cover rounded-sm shadow-sm"
                                            />
                                            <span className="flex-1">{config.name}</span>
                                            <span className="text-xs text-slate-400 uppercase font-mono">
                                                {code}
                                            </span>
                                        </button>
                                    );
                                })}
                            </li>
                        ))}

                        {Object.keys(filteredLanguages).length === 0 && (
                            <li className="px-3 py-8 text-center text-sm text-slate-400">
                                No languages found
                            </li>
                        )}
                    </ul>
                </div>
            )}

            <style jsx>{`
                /* Custom scrollbar for webkit browsers */
                ul::-webkit-scrollbar {
                    width: 8px;
                }
                ul::-webkit-scrollbar-track {
                    background: #f1f5f9;
                }
                ul::-webkit-scrollbar-thumb {
                    background: #cbd5e1;
                    border-radius: 4px;
                }
                ul::-webkit-scrollbar-thumb:hover {
                    background: #94a3b8;
                }
            `}</style>
        </div>
    );
}
