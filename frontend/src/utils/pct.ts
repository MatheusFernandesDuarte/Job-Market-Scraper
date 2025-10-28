export function pct(n?: number) {
    if (n == null) return "—";
    return `${Math.round(n * 100)}%`;
}
