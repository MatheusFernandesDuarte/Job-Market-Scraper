"use client";

import { useState, useEffect, useRef } from "react";
import { useLanguage } from "@/context/LanguageContext";

const flags = {
    pt: "/flags/br.svg",
    en: "/flags/us.svg",
    es: "/flags/es.svg",
};

export function LanguageSelector() {
    const { lang, setLang } = useLanguage();
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <div ref={ref} className="relative inline-block text-left">
            <button
                onClick={() => setOpen((o) => !o)}
                aria-haspopup="listbox"
                aria-expanded={open}
                className="flex items-center gap-2 px-3 py-1 rounded-md border bg-white shadow-sm hover:shadow-md transition"
            >
                <img
                    src={flags[lang]}
                    alt={lang === "pt" ? "Português" : "English"}
                    className="w-5 h-5"
                />
                <span className="text-sm uppercase">{lang}</span>
            </button>

            {open && (
                <ul
                    role="listbox"
                    className="absolute mt-1 right-0 rounded-md border bg-white shadow-lg w-28 animate-in fade-in zoom-in"
                >
                    {Object.entries(flags).map(([key, flag]) => (
                        <li
                            key={key}
                            onClick={() => {
                                setLang(key as "pt" | "en");
                                setOpen(false);
                            }}
                            className={`flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-sky-50 ${lang === key ? "font-semibold text-sky-600" : ""
                                }`}
                        >
                            <img src={flag} alt={`${key} flag`} className="w-5 h-5" />
                            {key.toUpperCase()}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
