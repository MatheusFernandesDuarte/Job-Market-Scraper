"use client";

import { useState } from "react";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";

export default function DocsPage() {
    const { lang } = useLanguage();
    const t = translations[lang];

    const [testData, setTestData] = useState({
        tech_stack: ["Python", "FastAPI"],
        location: ["Remote"],
        seniority: "senior",
    });
    const [testResults, setTestResults] = useState<any[] | null>(null);
    const [testLoading, setTestLoading] = useState(false);
    const [testError, setTestError] = useState<string | null>(null);

    const handleTest = async () => {
        setTestLoading(true);
        setTestError(null);
        setTestResults(null);

        try {
            const response = await fetch("http://localhost:8000/api/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(testData),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            setTestResults(data);
        } catch (error) {
            setTestError(error instanceof Error ? error.message : "Unknown error");
        } finally {
            setTestLoading(false);
        }
    };

    return (
        <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white p-8">
            <div className="max-w-5xl mx-auto flex flex-col gap-8">
                <Header />

                <section className="bg-white rounded-2xl shadow-sm p-8">
                    <h2 className="text-3xl font-bold text-slate-800 mb-2">
                        {t.docsTitle}
                    </h2>
                    <p className="text-slate-600 mb-8">{t.docsSubtitle}</p>

                    {/* Introdução */}
                    <div className="mb-8 p-4 bg-sky-50 border-l-4 border-sky-500 rounded">
                        <p className="text-sm text-slate-700">{t.docsIntro}</p>
                    </div>

                    {/* Base URL */}
                    <Section title={t.docsBaseUrl}>
                        <CodeBlock code="http://localhost:8000" />
                    </Section>

                    {/* Autenticação */}
                    <Section title={t.docsAuthentication}>
                        <p className="text-sm text-slate-600">{t.docsAuthDesc}</p>
                    </Section>

                    {/* Endpoints */}
                    <Section title={t.docsEndpoints}>
                        {/* POST /api/search */}
                        <div className="border border-slate-200 rounded-lg p-6 mb-6">
                            <div className="flex items-center gap-3 mb-4">
                                <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded">
                                    POST
                                </span>
                                <code className="text-lg font-mono text-slate-800">
                                    /api/search
                                </code>
                            </div>
                            <p className="text-sm text-slate-600 mb-6">
                                {t.docsSearchDesc}
                            </p>

                            {/* Request Body */}
                            <h4 className="font-semibold text-slate-800 mb-3">
                                {t.docsRequestBody}
                            </h4>
                            <div className="overflow-x-auto mb-6">
                                <table className="w-full text-sm border-collapse">
                                    <thead>
                                        <tr className="bg-slate-100">
                                            <th className="border border-slate-300 px-4 py-2 text-left font-semibold text-slate-800">
                                                {t.docsParameters}
                                            </th>
                                            <th className="border border-slate-300 px-4 py-2 text-left font-semibold text-slate-800">
                                                {t.docsType}
                                            </th>
                                            <th className="border border-slate-300 px-4 py-2 text-left font-semibold text-slate-800">
                                                {t.docsDescription}
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-slate-700">
                                        <tr>
                                            <td className="border border-slate-300 px-4 py-2">
                                                <code className="text-sky-600 font-semibold">tech_stack</code>
                                                <br />
                                                <span className="text-xs text-slate-600 font-medium">
                                                    {t.docsRequired}
                                                </span>
                                            </td>
                                            <td className="border border-slate-300 px-4 py-2">
                                                <code className="text-slate-700 font-mono">string[]</code>
                                            </td>
                                            <td className="border border-slate-300 px-4 py-2 text-slate-700">
                                                {t.docsParamTechStack}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="border border-slate-300 px-4 py-2">
                                                <code className="text-sky-600 font-semibold">location</code>
                                                <br />
                                                <span className="text-xs text-slate-600 font-medium">
                                                    {t.docsRequired}
                                                </span>
                                            </td>
                                            <td className="border border-slate-300 px-4 py-2">
                                                <code className="text-slate-700 font-mono">string[]</code>
                                            </td>
                                            <td className="border border-slate-300 px-4 py-2 text-slate-700">
                                                {t.docsParamLocation}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="border border-slate-300 px-4 py-2">
                                                <code className="text-sky-600 font-semibold">seniority</code>
                                                <br />
                                                <span className="text-xs text-slate-600 font-medium">
                                                    {t.docsOptional}
                                                </span>
                                            </td>
                                            <td className="border border-slate-300 px-4 py-2">
                                                <code className="text-slate-700 font-mono">string | null</code>
                                            </td>
                                            <td className="border border-slate-300 px-4 py-2 text-slate-700">
                                                {t.docsParamSeniority}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>


                            {/* Request Example */}
                            <h4 className="font-semibold text-slate-800 mb-3">
                                {t.docsExample} - {t.docsRequestBody}
                            </h4>
                            <CodeBlock
                                code={`{
  "tech_stack": ["Python", "FastAPI", "Docker"],
  "location": ["Remote", "Brazil"],
  "seniority": "senior"
}`}
                                language="json"
                            />

                            {/* Response Body */}
                            <h4 className="font-semibold text-slate-800 mb-3 mt-6">
                                {t.docsResponseBody}
                            </h4>
                            <CodeBlock
                                code={`[
  {
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "url": "https://example.com/job/123",
    "match_score": 85.5,
    "skills_matched": ["Python", "FastAPI"],
    "skills_missing": ["Kubernetes"],
    "salary": "R$ 15.000 - R$ 20.000",
    "experience": "5+ years",
    "date_posted": "2025-10-30",
    "tags": ["remote", "full-time"]
  }
]`}
                                language="json"
                            />
                        </div>
                    </Section>

                    {/* Error Codes */}
                    <Section title={t.docsErrorCodes}>
                        <div className="space-y-2 text-sm">
                            <div className="flex gap-3">
                                <code className="font-bold text-red-600">400</code>
                                <span className="text-slate-600">{t.docsError400}</span>
                            </div>
                            <div className="flex gap-3">
                                <code className="font-bold text-red-600">500</code>
                                <span className="text-slate-600">{t.docsError500}</span>
                            </div>
                        </div>
                    </Section>

                    {/* Rate Limits */}
                    <Section title={t.docsRateLimits}>
                        <p className="text-sm text-slate-600">{t.docsRateLimitsDesc}</p>
                    </Section>

                    {/* Try It Out */}
                    <Section title={`🧪 ${t.docsTryItOut}`}>
                        <div className="border border-slate-200 rounded-lg p-6 bg-slate-50">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Tech Stack (comma separated)
                                    </label>
                                    <input
                                        type="text"
                                        value={testData.tech_stack.join(", ")}
                                        onChange={(e) =>
                                            setTestData({
                                                ...testData,
                                                tech_stack: e.target.value.split(",").map((s) => s.trim()),
                                            })
                                        }
                                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 bg-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
                                        placeholder="Python, FastAPI, Docker"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Location (comma separated)
                                    </label>
                                    <input
                                        type="text"
                                        value={testData.location.join(", ")}
                                        onChange={(e) =>
                                            setTestData({
                                                ...testData,
                                                location: e.target.value.split(",").map((s) => s.trim()),
                                            })
                                        }
                                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 bg-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
                                        placeholder="Remote, Brazil"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Seniority
                                    </label>
                                    <input
                                        type="text"
                                        value={testData.seniority}
                                        onChange={(e) =>
                                            setTestData({ ...testData, seniority: e.target.value })
                                        }
                                        className="w-full px-3 py-2 border border-slate-300 rounded-md text-sm text-slate-900 bg-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500"
                                        placeholder="senior"
                                    />
                                </div>
                            </div>

                            <button
                                onClick={handleTest}
                                disabled={testLoading}
                                className="w-full px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {testLoading ? t.docsLoading : t.docsSend}
                            </button>

                            {testError && (
                                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                                    Error: {testError}
                                </div>
                            )}

                            {testResults && (
                                <div className="mt-4">
                                    <p className="text-sm text-slate-600 mb-2">
                                        {testResults.length} {t.docsResultsFound}
                                    </p>
                                    <CodeBlock
                                        code={JSON.stringify(testResults, null, 2)}
                                        language="json"
                                    />
                                </div>
                            )}
                        </div>
                    </Section>
                </section>

                <Footer />
            </div>
        </main>
    );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
    return (
        <div className="mb-8">
            <h3 className="text-xl font-semibold text-slate-800 mb-4 pb-2 border-b border-slate-200">
                {title}
            </h3>
            {children}
        </div>
    );
}

function CodeBlock({ code, language = "bash" }: { code: string; language?: string }) {
    return (
        <div className="relative">
            <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-sm">
                <code className={`language-${language}`}>{code}</code>
            </pre>
        </div>
    );
}
