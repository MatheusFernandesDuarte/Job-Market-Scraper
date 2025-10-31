import { InformationCircleIcon } from "@heroicons/react/24/outline";

type Props = {
    text: string;
    className?: string;
    position?: "top" | "bottom" | "left" | "right";
};

export function TooltipHelpIcon({
    text,
    className = "",
    position = "top",
}: Props) {
    const posClass =
        position === "bottom"
            ? "top-6"
            : position === "left"
                ? "right-full mr-2"
                : position === "right"
                    ? "left-full ml-2"
                    : "-top-9";

    return (
        <span className="relative flex items-center group" role="tooltip">
            <InformationCircleIcon
                className={`w-4 h-4 text-sky-600 cursor-default ${className}`}
            />
            <span
                className={`absolute ${posClass} left-1/2 -translate-x-1/2 pointer-events-none whitespace-nowrap rounded bg-slate-900 px-3 py-1.5 text-xs text-white opacity-0 shadow-lg transition-all duration-200 group-hover:opacity-100 z-20`}
            >
                {text}
            </span>
        </span>
    );
}