"use client";

import { SkillSummary } from "./SkillSummary";
import { Job } from "@/types/Job";
import { pct } from "@/utils/pct";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales";

type Props = {
    results: Job[];
    techStack: string;
};

export function JobResultsTable({ results, techStack }: Props) {
    const { lang } = useLanguage();
    const t = translations[lang];

    if (results.length === 0) {
        return (
            <div className="text-sm text-slate-500">{t.noResultsMessage}</div>
        );
    }

    return (
        <div className="overflow-x-auto mt-2">
            <table className="min-w-full divide-y divide-slate-100">
                <thead className="bg-slate-50">
                    <tr>
                        {[
                            t.match,
                            t.jobTitle,
                            "Skills",
                            t.salary,
                            t.experience,
                            t.date,
                        ].map((label) => (
                            <th
                                key={label}
                                scope="col"
                                className="px-4 py-2 text-left text-xs font-medium text-slate-500"
                            >
                                {label}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-100">
                    {results.map((job, i) => (
                        <tr key={job.id || i} className="hover:bg-slate-50 transition">
                            <td className="px-4 py-3 align-top font-semibold text-slate-800 text-sm">
                                {pct(job.match_score)}
                            </td>
                            <td className="px-4 py-3 align-top">
                                <div className="text-sm font-medium text-slate-800">
                                    {job.title}
                                </div>
                                {job.company && (
                                    <div className="text-xs text-slate-500">{job.company}</div>
                                )}
                                {job.url && (
                                    <a
                                        href={job.url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="text-xs text-sky-600 hover:underline"
                                        aria-label={t.viewOnSite}
                                    >
                                        {t.viewOnSite}
                                    </a>
                                )}
                            </td>
                            <td className="px-4 py-3 align-top text-sm">
                                <SkillSummary job={job} techStack={techStack} />
                            </td>
                            <td className="px-4 py-3 align-top text-sm">
                                {job.salary ?? "—"}
                            </td>
                            <td className="px-4 py-3 align-top text-sm">
                                {job.experience ?? "—"}
                            </td>
                            <td className="px-4 py-3 align-top text-sm">
                                {job.date_posted ?? "—"}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}