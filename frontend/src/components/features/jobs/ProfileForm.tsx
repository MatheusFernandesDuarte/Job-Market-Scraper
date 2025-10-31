"use client";

import React from "react";
import { TooltipHelpIcon } from "@/components/ui/TooltipHelpIcon";
import { translations } from "@/locales";
import { Language } from "@/config/languages";
import { Alert } from "@/components/ui/Alert";


type ProfileFormProps = {
    techStack: string;
    setTechStack: (v: string) => void;
    location: string;
    setLocation: (v: string) => void;
    seniority: string;
    setSeniority: (v: string) => void;
    loading: boolean;
    error: string | null;
    handleSubmit: (e: React.FormEvent) => void;
    lang: Language;
};

export function ProfileForm({
    lang,
    techStack,
    setTechStack,
    location,
    setLocation,
    seniority,
    setSeniority,
    loading,
    error,
    handleSubmit,
}: ProfileFormProps) {
    const t = translations[lang];

    return (
        <form
            onSubmit={handleSubmit}
            className="bg-white p-6 rounded-2xl shadow-sm space-y-4"
        >
            {/* Tech Stack */}
            <InputField
                id="techStack"
                label={t.stack}
                placeholder={t.placeholderStack}
                value={techStack}
                onChange={(e) => setTechStack(e.target.value)}
                helpText={t.stackHelp}
            />

            {/* Location */}
            <InputField
                id="location"
                label={t.location}
                placeholder={t.placeholderLocation}
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                helpText={t.locationHelp}
            />

            {/* Seniority */}
            <div className="flex flex-col">
                <label
                    htmlFor="seniority"
                    className="text-sm font-medium text-slate-700"
                >
                    {t.seniority}
                </label>
                <select
                    id="seniority"
                    value={seniority}
                    onChange={(e) => setSeniority(e.target.value)}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-sky-300"
                >
                    {t.seniorityOptions.map((opt: { value: string; label: string }) => (
                        <option key={opt.value} value={opt.value}>
                            {opt.label}
                        </option>
                    ))}
                </select>
            </div>

            {/* Submit */}
            <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 bg-sky-600 text-white font-medium rounded-lg hover:bg-sky-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
            >
                {loading ? t.loading : t.button}
            </button>

            {error && (
                <Alert
                    type="error"
                    title={t.errorTitle}
                    message={t.errorAtLeastOne}
                />
            )}

        </form>
    );
}

function InputField({
    id,
    label,
    value,
    onChange,
    placeholder,
    helpText,
}: {
    id: string;
    label: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    placeholder?: string;
    helpText?: string;
}) {
    return (
        <div className="flex flex-col">
            <label
                htmlFor={id}
                className="text-sm font-medium text-slate-700 flex items-center gap-2"
            >
                {label}
                {helpText && <TooltipHelpIcon text={helpText} />}
            </label>
            <input
                id={id}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 shadow-sm focus:ring-2 focus:ring-sky-300"
            />
        </div>
    );
}