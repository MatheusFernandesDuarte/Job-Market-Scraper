import { useState, useReducer, useCallback } from "react";
import { Job } from "@/types/Job";

/** Helper — transforma "React, Node" → ["react", "node"] */
function parseCSV(value: string): string[] {
    return value
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean)
        .map((s) => s.toLowerCase());
}

type State = {
    techStack: string;
    location: string;
    seniority: string;
    loading: boolean;
    error: string | null;
    results: Job[];
};

type Action =
    | { type: "SET_FIELD"; field: keyof State; value: string }
    | { type: "SET_RESULTS"; results: Job[] }
    | { type: "SET_ERROR"; error: string | null }
    | { type: "SET_LOADING"; loading: boolean };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case "SET_FIELD":
            return { ...state, [action.field]: action.value };
        case "SET_RESULTS":
            return { ...state, results: action.results };
        case "SET_ERROR":
            return { ...state, error: action.error };
        case "SET_LOADING":
            return { ...state, loading: action.loading };
        default:
            return state;
    }
}

export function useJobSearch() {
    const [state, dispatch] = useReducer(reducer, {
        techStack: "",
        location: "",
        seniority: "",
        loading: false,
        error: null,
        results: [],
    });

    const setField = useCallback(
        (field: keyof State, value: string) =>
            dispatch({ type: "SET_FIELD", field, value }),
        []
    );

    const handleSubmit = useCallback(
        async (e: React.FormEvent) => {
            e.preventDefault();
            dispatch({ type: "SET_ERROR", error: null });
            dispatch({ type: "SET_LOADING", loading: true });

            try {
                const payload = {
                    tech_stack: parseCSV(state.techStack),
                    location: parseCSV(state.location),
                    seniority: state.seniority,
                };

                const res = await fetch("/api/search", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                });

                if (!res.ok) {
                    const text = await res.text();
                    throw new Error(`Backend error: ${res.status} ${text}`);
                }

                const data = (await res.json()) as unknown;
                if (!Array.isArray(data)) throw new Error("Invalid API response format");

                dispatch({ type: "SET_RESULTS", results: data });
            } catch (err) {
                const message =
                    err instanceof Error
                        ? err.message.includes("Failed to fetch")
                            ? "A API está desligada ou inacessível. Verifique o servidor."
                            : err.message
                        : "Erro desconhecido";
                dispatch({ type: "SET_ERROR", error: message });
            } finally {
                dispatch({ type: "SET_LOADING", loading: false });
            }
        },
        [state.techStack, state.location, state.seniority]
    );

    return {
        ...state,
        setTechStack: (v: string) => setField("techStack", v),
        setLocation: (v: string) => setField("location", v),
        setSeniority: (v: string) => setField("seniority", v),
        handleSubmit,
    };
}
