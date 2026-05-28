"use client";

interface RingProps {
  label: string;
  value: string | number;
  percent: number;
  color: string;
}

function Ring({ label, value, percent, color }: RingProps) {
  const p = Math.min(100, Math.max(0, percent));
  const r = 36;
  const c = 2 * Math.PI * r;
  const offset = c - (p / 100) * c;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative h-24 w-24">
        <svg className="h-24 w-24 -rotate-90" viewBox="0 0 96 96">
          <circle
            cx="48"
            cy="48"
            r={r}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-white/10"
          />
          <circle
            cx="48"
            cy="48"
            r={r}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={c}
            strokeDashoffset={offset}
            className={color}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-sm font-bold text-white tabular-nums">{value}</span>
        </div>
      </div>
      <span className="text-[10px] uppercase tracking-wider text-zinc-500 text-center">
        {label}
      </span>
    </div>
  );
}

interface QuizStatsRingsProps {
  accuracy: number;
  attempted: number;
  total: number;
  percentile: number | null;
}

export function QuizStatsRings({
  accuracy,
  attempted,
  total,
  percentile,
}: QuizStatsRingsProps) {
  const attemptPct = total > 0 ? Math.round((attempted / total) * 100) : 0;

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 justify-items-center py-2">
      <Ring label="Accuracy" value={`${accuracy}%`} percent={accuracy} color="text-violet-400" />
      <Ring
        label="Attempted"
        value={`${attempted}/${total}`}
        percent={attemptPct}
        color="text-emerald-400"
      />
      <Ring
        label="Score"
        value={attempted}
        percent={total > 0 ? Math.round((attempted / total) * 100) : 0}
        color="text-sky-400"
      />
      <Ring
        label="Percentile"
        value={percentile != null ? `${percentile}%` : "—"}
        percent={percentile ?? 0}
        color="text-amber-400"
      />
    </div>
  );
}
