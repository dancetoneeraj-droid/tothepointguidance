interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  size?: "sm" | "md";
  className?: string;
}

export function ProgressBar({
  value,
  max = 100,
  label,
  size = "md",
  className = "",
}: ProgressBarProps) {
  const percent = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div className={`w-full ${className}`}>
      {label ? (
        <div className="flex justify-between text-xs text-muted mb-1.5">
          <span>{label}</span>
          <span>{Math.round(percent)}%</span>
        </div>
      ) : null}
      <div
        className={`w-full rounded-full bg-surface-hover overflow-hidden ${
          size === "sm" ? "h-1.5" : "h-2"
        }`}
      >
        <div
          className="h-full rounded-full bg-gradient-to-r from-violet-500 to-indigo-500 transition-all duration-500 ease-out"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
