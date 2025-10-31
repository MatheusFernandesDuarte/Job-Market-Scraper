import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";

export function useTranslations() {
    const { lang } = useLanguage();
    return translations[lang];
}
