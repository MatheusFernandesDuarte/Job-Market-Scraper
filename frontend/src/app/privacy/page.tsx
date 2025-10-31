"use client";

import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";
import { siteConfig } from "@/config/site";

export default function PrivacyPage() {
    const { lang } = useLanguage();
    const t = translations[lang];

    const sections = [
        {
            title: t.privacySection1Title,
            subsections: [
                {
                    title: t.privacySection1_1Title,
                    text: t.privacySection1_1Text,
                },
                {
                    title: t.privacySection1_2Title,
                    text: t.privacySection1_2Text,
                },
                {
                    title: t.privacySection1_3Title,
                    text: t.privacySection1_3Text,
                },
            ],
        },
        {
            title: t.privacySection2Title,
            intro: t.privacySection2Text,
            list: t.privacySection2List,
        },
        {
            title: t.privacySection3Title,
            text: t.privacySection3Text,
        },
        {
            title: t.privacySection4Title,
            text: t.privacySection4Text,
        },
        {
            title: t.privacySection5Title,
            intro: t.privacySection5Text,
            list: t.privacySection5List,
        },
        {
            title: t.privacySection6Title,
            text: t.privacySection6Text,
        },
        {
            title: t.privacySection7Title,
            text: t.privacySection7Text,
        },
        {
            title: t.privacySection8Title,
            text: t.privacySection8Text,
        },
        {
            title: t.privacySection9Title,
            text: t.privacySection9Text,
        },
    ];

    return (
        <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white p-8">
            <div className="max-w-4xl mx-auto flex flex-col gap-8">
                <Header />

                <section className="bg-white rounded-2xl shadow-sm p-8">
                    <h2 className="text-3xl font-bold text-slate-800 mb-2">
                        {t.privacyTitle}
                    </h2>
                    <p className="text-xs text-slate-500 mb-6">{t.privacyLastUpdated}</p>
                    <p className="text-slate-600 mb-8 leading-relaxed">
                        {t.privacyIntro}
                    </p>

                    <div className="space-y-8">
                        {sections.map((section, idx) => (
                            <div key={idx} className="pb-6 border-b border-slate-200 last:border-0">
                                <h3 className="text-xl font-semibold text-slate-800 mb-4">
                                    {section.title}
                                </h3>

                                {/* Se tem subsections (Seção 1) */}
                                {section.subsections && (
                                    <div className="space-y-4">
                                        {section.subsections.map((sub, subIdx) => (
                                            <div key={subIdx}>
                                                <h4 className="text-base font-medium text-slate-700 mb-2">
                                                    {sub.title}
                                                </h4>
                                                <p className="text-sm text-slate-600 leading-relaxed">
                                                    {sub.text}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {/* Se tem intro + list (Seções 2 e 5) */}
                                {section.intro && section.list && (
                                    <>
                                        <p className="text-sm text-slate-600 mb-3 leading-relaxed">
                                            {section.intro}
                                        </p>
                                        <ul className="space-y-2 ml-4">
                                            {section.list.map((item: string, itemIdx: number) => (
                                                <li
                                                    key={itemIdx}
                                                    className="flex items-start gap-2 text-sm text-slate-600"
                                                >
                                                    <span className="text-sky-500 mt-1">•</span>
                                                    <span>{item}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </>
                                )}

                                {/* Se tem apenas text (demais seções) */}
                                {section.text && (
                                    <p className="text-sm text-slate-600 leading-relaxed">
                                        {section.text}
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Contact Section */}
                    <div className="mt-8 p-6 bg-sky-50 border border-sky-200 rounded-lg">
                        <h3 className="text-lg font-semibold text-slate-800 mb-2">
                            {t.privacySection10Title}
                        </h3>
                        <p className="text-sm text-slate-600 mb-4">
                            {t.privacySection10Text}
                        </p>
                        <div className="flex gap-4">
                            <a
                                href={siteConfig.links.github}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 text-sm text-sky-600 hover:text-sky-700 font-medium"
                            >
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                                </svg>
                                GitHub
                            </a>
                            <a
                                href={siteConfig.links.linkedin}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 text-sm text-sky-600 hover:text-sky-700 font-medium"
                            >
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                                </svg>
                                LinkedIn
                            </a>
                        </div>
                    </div>
                </section>

                <Footer />
            </div>
        </main>
    );
}
