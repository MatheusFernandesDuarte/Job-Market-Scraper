"use client";

import { LanguageSelector } from "@/components/ui/LanguageSelector";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";
import { useState, useEffect } from "react";
import { siteConfig } from "@/config/site";
import Link from "next/link";

export function Header() {
    const { lang } = useLanguage();
    const t = translations[lang];

    return (
        <header className="bg-white rounded-2xl shadow-lg border border-slate-200">
            {/* Top section - Main header */}
            <div className="p-6 md:p-8 border-b border-slate-100">
                <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6">
                    {/* Left - Branding & Description */}
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="w-12 h-12 bg-gradient-to-br from-sky-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                                <svg
                                    className="w-7 h-7 text-white"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                            </div>
                            <div>
                                <h1 className="text-2xl md:text-3xl font-bold text-slate-800 tracking-tight">
                                    {t.headerTitle}
                                </h1>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="flex items-center gap-1.5 px-2 py-0.5 bg-green-50 text-green-700 rounded-full border border-green-200 text-xs font-medium">
                                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                                        {t.statusBadge}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <p className="text-sm md:text-base text-slate-600 leading-relaxed max-w-2xl">
                            {t.headerSubtitle}
                        </p>
                    </div>

                    {/* Right - Stats & Language */}
                    <div className="flex flex-col gap-4">

                        {/* Language Selector */}
                        <div className="flex justify-end">
                            <LanguageSelector />
                        </div>

                    </div>
                </div>
            </div>

            {/* Navigation bar */}
            <nav className="px-6 md:px-8 py-3 flex items-center justify-between bg-slate-50 rounded-b-2xl">
                <div className="flex items-center gap-1">
                    <Link
                        href="/"
                        className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-white rounded-lg transition-all"
                    >
                        🏠 {t.footerHome}
                    </Link>
                    <Link
                        href="/about"
                        className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-white rounded-lg transition-all"
                    >
                        ℹ️ {t.footerAbout}
                    </Link>
                    <Link
                        href="/docs"
                        className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-white rounded-lg transition-all"
                    >
                        📚 {t.footerApiDocs}
                    </Link>
                    <Link
                        href="/privacy"
                        className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-sky-600 hover:bg-white rounded-lg transition-all"
                    >
                        🔒 {t.footerPrivacy}
                    </Link>
                </div>

                {/* GitHub link */}
                <a
                    href={siteConfig.links.github_profile}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-700 hover:text-slate-900 hover:bg-white rounded-lg transition-all"
                >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                    </svg>
                    GitHub
                </a>
            </nav>
        </header>
    );
}
