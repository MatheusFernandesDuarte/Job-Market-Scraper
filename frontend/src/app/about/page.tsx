"use client";

import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";
import { siteConfig } from "@/config/site";

export default function AboutPage() {
    const { lang } = useLanguage();
    const t = translations[lang];

    const sections = [
        {
            icon: "🔍",
            title: t.aboutSection1Title,
            description: t.aboutSection1Desc,
            details: t.aboutSection1Details,
        },
        {
            icon: "🤖",
            title: t.aboutSection2Title,
            description: t.aboutSection2Desc,
            details: t.aboutSection2Details,
        },
        {
            icon: "🎯",
            title: t.aboutSection3Title,
            description: t.aboutSection3Desc,
            details: t.aboutSection3Details,
        },
        {
            icon: "⚡",
            title: t.aboutSection4Title,
            description: t.aboutSection4Desc,
            details: t.aboutSection4Details,
        },
    ];

    const techStack = {
        frontend: {
            title: t.aboutTechFrontend,
            items: siteConfig.techStack.frontend,
            color: "sky" as const,
        },
        backend: {
            title: t.aboutTechBackend,
            items: siteConfig.techStack.backend,
            color: "emerald" as const,
        },
        infra: {
            title: t.aboutTechInfra,
            items: siteConfig.techStack.infra,
            color: "violet" as const,
        },
    };

    return (
        <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white p-8">
            <div className="max-w-5xl mx-auto flex flex-col gap-8">
                <Header />

                <section className="bg-white rounded-2xl shadow-sm p-8">
                    <h2 className="text-3xl font-bold text-slate-800 mb-2">
                        {t.aboutTitle}
                    </h2>
                    <p className="text-slate-600 mb-8">{t.aboutSubtitle}</p>

                    <div className="space-y-8">
                        {sections.map((section, idx) => (
                            <div key={idx} className="border-l-4 border-sky-500 pl-6 py-2">
                                <div className="flex items-center gap-3 mb-3">
                                    <span className="text-3xl">{section.icon}</span>
                                    <h3 className="text-xl font-semibold text-slate-800">
                                        {section.title}
                                    </h3>
                                </div>
                                <p className="text-slate-600 mb-4">{section.description}</p>
                                <ul className="space-y-2">
                                    {section.details.map((detail: string, detailIdx: string) => (
                                        <li
                                            key={detailIdx}
                                            className="flex items-start gap-2 text-sm text-slate-600"
                                        >
                                            <span className="text-sky-500 mt-1">✓</span>
                                            {detail}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>

                    {/* Tech Stack */}
                    <div className="mt-12 pt-8 border-t border-slate-200">
                        <h3 className="text-2xl font-bold text-slate-800 mb-6">
                            {t.aboutTechStackTitle}
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <TechStackCard
                                title={techStack.frontend.title}
                                items={techStack.frontend.items}
                                color={techStack.frontend.color}
                            />
                            <TechStackCard
                                title={techStack.backend.title}
                                items={techStack.backend.items}
                                color={techStack.backend.color}
                            />
                            <TechStackCard
                                title={techStack.infra.title}
                                items={techStack.infra.items}
                                color={techStack.infra.color}
                            />
                        </div>
                    </div>

                    {/* Open Source */}
                    <div className="mt-12 pt-8 border-t border-slate-200 text-center">
                        <h3 className="text-2xl font-bold text-slate-800 mb-3">
                            {t.aboutOpenSourceTitle}
                        </h3>
                        <p className="text-slate-600 mb-6">{t.aboutOpenSourceDesc}</p>
                        <a
                            href={siteConfig.links.github}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 px-6 py-3 bg-slate-800 text-white rounded-lg hover:bg-slate-700 transition-colors"
                        >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                            </svg>
                            {t.aboutOpenSourceCta}
                        </a>
                    </div>
                </section>

                <Footer />
            </div>
        </main>
    );
}

function TechStackCard({
    title,
    items,
    color,
}: {
    title: string;
    items: readonly string[];
    color: "sky" | "emerald" | "violet";
}) {
    const colorClasses = {
        sky: "bg-sky-50 border-sky-200",
        emerald: "bg-emerald-50 border-emerald-200",
        violet: "bg-violet-50 border-violet-200",
    };

    return (
        <div className={`p-4 rounded-lg border ${colorClasses[color]}`}>
            <h4 className="font-semibold text-slate-800 mb-3">{title}</h4>
            <ul className="space-y-2">
                {items.map((item, idx) => (
                    <li key={idx} className="text-sm text-slate-600">
                        • {item}
                    </li>
                ))}
            </ul>
        </div>
    );
}
