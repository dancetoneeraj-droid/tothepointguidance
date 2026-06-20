"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Medal, Trophy, Zap } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { getLeaderboardEntries, type LeaderboardEntry } from "@/lib/firebase/firestore";

type LeaderboardRow = LeaderboardEntry & { uid: string; rank: number };

export default function LeaderboardPage() {
  const [rows, setRows] = useState<LeaderboardRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const entries = await getLeaderboardEntries();
        setRows(
          entries.map((e, i) => ({ ...e, rank: i + 1 }))
        );
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, []);

  const rankIcon = (rank: number) => {
    if (rank === 1) return <Medal className="h-4 w-4 text-amber-400" />;
    if (rank === 2) return <Medal className="h-4 w-4 text-zinc-300" />;
    if (rank === 3) return <Medal className="h-4 w-4 text-amber-700" />;
    return null;
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-background/80 backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4 sm:px-6">
          <Link href="/" className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-violet-600 to-indigo-600">
              <Zap className="h-4 w-4 text-white" />
            </span>
            <span className="font-semibold">ToThePoint</span>
          </Link>
          <Link href="/dashboard" className="text-sm text-violet-400 hover:text-violet-300">
            Dashboard
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 sm:px-6 py-8 space-y-6">
        <div className="text-center">
          <div className="inline-flex items-center gap-2 text-amber-400 mb-2">
            <Trophy className="h-6 w-6" />
            <span className="text-xs font-semibold uppercase tracking-widest">
              Live Leaderboard
            </span>
          </div>
          <h1 className="text-3xl font-semibold tracking-tight">
            SSC CGL Prep Rankings
          </h1>
          <p className="text-muted mt-2 text-sm max-w-lg mx-auto">
            Rankings update automatically when students visit their dashboard.
            Keep pushing — every task counts.
          </p>
        </div>

        <Card className="overflow-hidden p-0 border-amber-500/20">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-surface-hover/50 text-left text-xs uppercase tracking-wider text-muted">
                  <th className="px-4 py-3">Rank</th>
                  <th className="px-4 py-3">Student</th>
                  <th className="px-4 py-3 hidden sm:table-cell">Day</th>
                  <th className="px-4 py-3 hidden md:table-cell">Tasks</th>
                  <th className="px-4 py-3">Completion</th>
                  <th className="px-4 py-3 hidden sm:table-cell">Accuracy</th>
                  <th className="px-4 py-3 hidden lg:table-cell">Streak</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={7} className="px-4 py-12 text-center text-muted">
                      <div className="flex items-center justify-center gap-2">
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-violet-500 border-t-transparent" />
                        Loading rankings…
                      </div>
                    </td>
                  </tr>
                ) : rows.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-4 py-12 text-center text-muted">
                      No rankings yet. Complete some tasks and visit your dashboard!
                    </td>
                  </tr>
                ) : (
                  rows.map((row) => (
                    <tr
                      key={row.uid}
                      className={`border-b border-border/50 hover:bg-surface-hover/30 ${
                        row.rank <= 3 ? "bg-amber-500/5" : ""
                      }`}
                    >
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1.5 font-bold tabular-nums text-amber-400">
                          {rankIcon(row.rank)}
                          #{row.rank}
                        </div>
                      </td>
                      <td className="px-4 py-3 font-medium text-foreground">
                        {row.displayName}
                      </td>
                      <td className="px-4 py-3 hidden sm:table-cell text-muted tabular-nums">
                        Day {row.currentDay}
                      </td>
                      <td className="px-4 py-3 hidden md:table-cell text-muted tabular-nums">
                        {row.tasksCompleted}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <div className="h-1.5 w-16 overflow-hidden rounded-full bg-white/10">
                            <div
                              className="h-full rounded-full bg-violet-500"
                              style={{ width: `${row.completionPct}%` }}
                            />
                          </div>
                          <span className="text-violet-400 font-semibold tabular-nums text-xs">
                            {row.completionPct}%
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3 hidden sm:table-cell text-emerald-400 tabular-nums">
                        {row.accuracy}%
                      </td>
                      <td className="px-4 py-3 hidden lg:table-cell text-amber-300 tabular-nums">
                        🔥 {row.streak}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>

        <p className="text-center text-xs text-zinc-600">
          Rankings refresh each time a student opens their dashboard.
        </p>
      </main>
    </div>
  );
}
