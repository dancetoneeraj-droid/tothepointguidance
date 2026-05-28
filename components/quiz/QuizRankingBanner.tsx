"use client";

import { Trophy } from "lucide-react";
import type { QuizRanking } from "@/types";

interface QuizRankingBannerProps {
  ranking: QuizRanking;
}

export function QuizRankingBanner({ ranking }: QuizRankingBannerProps) {
  if (ranking.rank == null) {
    return (
      <div className="rounded-xl border border-white/10 bg-[#121218] px-5 py-4 text-center">
        <p className="text-sm text-zinc-400">
          Practice attempt — does not affect leaderboard rank.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-amber-500/30 bg-gradient-to-br from-amber-500/10 to-violet-500/5 px-5 py-5 text-center">
      <div className="inline-flex items-center gap-2 text-amber-400 mb-2">
        <Trophy className="h-5 w-5" />
        <span className="text-xs font-semibold uppercase tracking-widest">
          Your Rank
        </span>
      </div>
      <p className="text-3xl font-bold text-white tabular-nums">
        {ranking.rank}{" "}
        <span className="text-lg font-normal text-zinc-500">
          / {ranking.totalParticipants}
        </span>
      </p>
      {ranking.percentile != null ? (
        <p className="text-sm text-violet-300 mt-1">
          Top {100 - ranking.percentile}% · {ranking.percentile} percentile
        </p>
      ) : null}
      {ranking.countsForLeaderboard ? (
        <p className="text-xs text-emerald-400/90 mt-2">First attempt recorded</p>
      ) : (
        <p className="text-xs text-zinc-500 mt-2">
          Showing rank from your first attempt
        </p>
      )}
    </div>
  );
}
