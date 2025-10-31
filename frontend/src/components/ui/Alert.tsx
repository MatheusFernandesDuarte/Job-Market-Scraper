type AlertProps = {
    type: "error" | "warning" | "info" | "success";
    title?: string;
    message: string;
    onClose?: () => void;
};

const alertConfig = {
    error: {
        bg: "bg-red-50",
        border: "border-red-200",
        icon: "text-red-500",
        title: "text-red-800",
        text: "text-red-700",
        iconComponent: () => (
            <span className="text-2xl">❌</span>
        )
    },
    warning: {
        bg: "bg-yellow-50",
        border: "border-yellow-200",
        icon: "text-yellow-500",
        title: "text-yellow-800",
        text: "text-yellow-700",
        iconComponent: () => (
            <span className="text-2xl">⚠️</span>
        )
    },
    info: {
        bg: "bg-blue-50",
        border: "border-blue-200",
        icon: "text-blue-500",
        title: "text-blue-800",
        text: "text-blue-700",
        iconComponent: () => (
            <span className="text-2xl">ℹ️</span>
        )
    },
    success: {
        bg: "bg-green-50",
        border: "border-green-200",
        icon: "text-green-500",
        title: "text-green-800",
        text: "text-green-700",
        iconComponent: () => (
            <span className="text-2xl">✅</span>
        )
    }
};

export function Alert({ type, title, message, onClose }: AlertProps) {
    const config = alertConfig[type];
    const IconComponent = config.iconComponent;

    return (
        <div className={`rounded-lg border ${config.border} ${config.bg} p-4 shadow-sm animate-fade-in`}>
            <div className="flex items-start gap-3">
                <div className={`flex-shrink-0 ${config.icon}`}>
                    <IconComponent />
                </div>
                <div className="flex-1">
                    {title && (
                        <h3 className={`text-sm font-semibold ${config.title} mb-1`}>
                            {title}
                        </h3>
                    )}
                    <p className={`text-sm ${config.text}`}>{message}</p>
                </div>
                {onClose && (
                    <button
                        onClick={onClose}
                        className={`flex-shrink-0 ${config.icon} hover:opacity-70 transition-opacity text-xl`}
                        aria-label="Fechar"
                    >
                        ✕
                    </button>
                )}
            </div>
        </div>
    );
}
