export type Job = {
    id?: string;
    title: string;
    company?: string;
    url?: string;
    match_score?: number;
    skills_matched?: string[];
    skills_missing?: string[];
    salary?: string | null;
    experience?: string | null;
    date_posted?: string | null;
    tags?: string[];
}
