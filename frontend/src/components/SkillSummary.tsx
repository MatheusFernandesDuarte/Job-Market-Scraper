import { Job } from "@/types/Job";
import { useLanguage } from "@/context/LanguageContext";
import { translations } from "@/locales/translations";

type Props = {
    job: Job;
    techStack: string;
};

export function SkillSummary({ job, techStack }: Props) {
    const { lang } = useLanguage();
    const t = translations[lang];

    const matched = job.skills_matched?.length
        ? job.skills_matched
        : deriveMatches(job, techStack).matched;
    const missing = job.skills_missing?.length
        ? job.skills_missing
        : deriveMatches(job, techStack).missing;

    return (
        <div className="text-sm">
            <span className="font-medium">{t.matched}:</span>{" "}
            {matched.length ? matched.join(", ") : "—"}
            <span className="ml-3 text-gray-500">
                | {t.missing}: {missing.length ? missing.join(", ") : "—"}
            </span>
        </div>
    );
}

function deriveMatches(job: Job, techStack: string) {
    const userSet = new Set(
        techStack
            .split(",")
            .map((s) => s.trim().toLowerCase())
            .filter(Boolean)
    );
    const tags = (job.tags || []).map((t) => t.toLowerCase());
    return {
        matched: tags.filter((t) => userSet.has(t)),
        missing: tags.filter((t) => !userSet.has(t)),
    };
}
