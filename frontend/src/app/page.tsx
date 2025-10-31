"use client";

import { useJobSearch } from "@/hooks/useJobSearch";
import { useLanguage } from "@/context/LanguageContext";
import { ProfileForm } from "@/components/features/jobs/ProfileForm";
import { JobResultsTable } from "@/components/features/jobs/JobResultsTable";
import { translations } from "@/locales";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";

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
    clearResults,
  } = useJobSearch();

  const { lang } = useLanguage();
  const t = translations[lang];

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white p-8">
      <div className="max-w-7xl mx-auto flex flex-col gap-8">
        <Header />

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
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
          </div>
          <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">
              {t.resultsTitle}
            </h2>
            {results.length > 0 && (
              <button
                onClick={clearResults}
                className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors flex items-center gap-2"
              >
                <span className="text-lg">🗑️</span>
                {t.clearResults}
              </button>
            )}
            <JobResultsTable results={results} techStack={techStack} />
          </div>
        </section>

        <Footer />
      </div>
    </main>
  );
}
