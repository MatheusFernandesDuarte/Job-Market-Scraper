import Image from "next/image";
import Link from "next/link";
import { siteConfig } from "@/config/site";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";

export function Footer() {
    const { lang } = useLanguage();
    const t = translations[lang];
    const currentYear = new Date().getFullYear();

    return (
        <footer className="border-t border-slate-200 pt-8 mt-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-6">
                {/* Coluna 1: Sobre o projeto */}
                <div>
                    <h3 className="font-semibold text-slate-800 mb-3">
                        {t.footerAbout}
                    </h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                        {t.footerAboutText}
                    </p>
                    <div className="flex gap-2 mt-3">
                        <Link
                            href={siteConfig.links.github}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-xs text-sky-600 hover:text-sky-700 transition-colors"
                        >
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                            </svg>
                            {t.footerGithub}
                        </Link>
                    </div>
                </div>

                {/* Coluna 2: Recursos */}
                <div>
                    <h3 className="font-semibold text-slate-800 mb-3">
                        {t.footerResources}
                    </h3>
                    <ul className="space-y-2 text-xs text-slate-600">
                        <li>
                            <Link
                                href="/"
                                className="hover:text-sky-600 transition-colors"
                            >
                                🏠 {t.footerHome}
                            </Link>
                        </li>
                        <li>
                            <Link
                                href="/docs"
                                className="hover:text-sky-600 transition-colors"
                            >
                                📚 {t.footerApiDocs}
                            </Link>
                        </li>
                        <li>
                            <Link
                                href="/about"
                                className="hover:text-sky-600 transition-colors"
                            >
                                ⚙️ {t.footerHowItWorks}
                            </Link>
                        </li>
                        <li>
                            <Link
                                href="/privacy"
                                className="hover:text-sky-600 transition-colors"
                            >
                                🔒 {t.footerPrivacy}
                            </Link>
                        </li>
                    </ul>
                </div>

                {/* Coluna 3: Contato */}
                <div>
                    <h3 className="font-semibold text-slate-800 mb-3">
                        {t.footerContact}
                    </h3>
                    <p className="text-xs text-slate-600 mb-3">
                        {t.footerDeveloper}{" "}
                        <span className="font-medium text-slate-800">
                            {siteConfig.author}
                        </span>
                    </p>
                    <div className="flex gap-3">
                        <Link
                            href={siteConfig.links.linkedin}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group"
                            aria-label="LinkedIn"
                        >
                            <div className="p-2 rounded-lg bg-slate-100 group-hover:bg-sky-100 transition-colors">
                                <Image
                                    src="/contacts/linkedin.svg"
                                    alt="LinkedIn"
                                    width={18}
                                    height={18}
                                    className="group-hover:scale-110 transition-transform"
                                />
                            </div>
                        </Link>
                        <Link
                            href={siteConfig.links.whatsapp}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group"
                            aria-label="WhatsApp"
                        >
                            <div className="p-2 rounded-lg bg-slate-100 group-hover:bg-green-100 transition-colors">
                                <Image
                                    src="/contacts/whatsapp.svg"
                                    alt="WhatsApp"
                                    width={18}
                                    height={18}
                                    className="group-hover:scale-110 transition-transform"
                                />
                            </div>
                        </Link>
                        <Link
                            href={siteConfig.links.github}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group"
                            aria-label="GitHub"
                        >
                            <div className="p-2 rounded-lg bg-slate-100 group-hover:bg-slate-200 transition-colors">
                                <Image
                                    src="/contacts/github.svg"
                                    alt="GitHub"
                                    width={18}
                                    height={18}
                                    className="group-hover:scale-110 transition-transform"
                                />
                            </div>
                        </Link>
                    </div>
                </div>
            </div>

            {/* Linha inferior */}
            <div className="pt-6 border-t border-slate-200 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-500">
                <p>
                    © {currentYear} {siteConfig.name}. {t.footerCopyright}
                </p>
                <p className="flex items-center gap-1">
                    {t.footerMadeWith} <span className="text-red-500">♥</span>{" "}
                    {t.footerTechStack}
                </p>
            </div>
        </footer>
    );
}
