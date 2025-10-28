"use client";

import { useJobSearch } from "@/hooks/useJobSearch";
import { useLanguage } from "@/context/LanguageContext";
import { ProfileForm } from "@/components/ProfileForm";
import { JobResultsTable } from "@/components/JobResultsTable";
import { LanguageSelector } from "@/components/LanguageSelector";
import { translations } from "@/locales/translations";

export default function HomePage() {
  const {
    techStack,
    setTechStack,
    location,
    setLocation,
    seniority,
    setSeniority,
    loading,
    error,
    results,
    handleSubmit,
  } = useJobSearch();

  const { lang } = useLanguage();
  const t = translations[lang];

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white p-8">
      <div className="max-w-5xl mx-auto flex flex-col gap-8">
        <header className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-slate-800">
              {t.headerTitle}
            </h1>
            <p className="text-sm text-slate-600 mt-2">{t.headerSubtitle}</p>
          </div>
          <LanguageSelector />
        </header>
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ProfileForm
            lang={lang}
            techStack={techStack}
            setTechStack={setTechStack}
            location={location}
            setLocation={setLocation}
            seniority={seniority}
            setSeniority={setSeniority}
            loading={loading}
            error={error}
            handleSubmit={handleSubmit}
          />

          <div className="col-span-2 bg-white p-6 rounded-2xl shadow-sm">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">
              {t.resultsTitle}
            </h2>
            <JobResultsTable results={results} techStack={techStack} />
          </div>
        </section>
        <footer className="text-center text-xs text-slate-500 mt-8">
          Job Market Scraper • Matheus Fernandes
        </footer>
      </div>
    </main>
  );
}
