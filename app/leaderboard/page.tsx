"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Trophy, Zap } from "lucide-react";
import { Card } from "@/components/ui/Card";

interface LeaderboardRow {
  rank: number;
  studentName: string;
  currentDay: number;
  tasksCompleted: number;
  completionPct: number;
  avgAccuracy: number;
}

export default function LeaderboardPage() {
  const [rows, setRows] = useState<LeaderboardRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/leaderboard");
        const data = await res.json();
        setRows(data.rows ?? []);
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, []);

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
              Public Leaderboard
            </span>
          </div>
          <h1 className="text-3xl font-semibold tracking-tight">
            SSC CGL Prep Rankings
          </h1>
          <p className="text-muted mt-2 text-sm max-w-lg mx-auto">
            Rankings use first quiz attempts and overall task completion. Keep
            pushing — every task counts.
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
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-12 text-center text-muted">
                      Loading rankings…
                    </td>
                  </tr>
                ) : rows.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-12 text-center text-muted">
                      No rankings yet. Be the first to complete a quiz!
                    </td>
                  </tr>
                ) : (
                  rows.map((row) => (
                    <tr
                      key={row.rank}
                      className={`border-b border-border/50 hover:bg-surface-hover/30 ${
                        row.rank <= 3 ? "bg-amber-500/5" : ""
                      }`}
                    >
                      <td className="px-4 py-3 font-bold tabular-nums text-amber-400">
                        #{row.rank}
                      </td>
                      <td className="px-4 py-3 font-medium text-foreground">
                        {row.studentName}
                      </td>
                      <td className="px-4 py-3 hidden sm:table-cell text-muted tabular-nums">
                        {row.currentDay}
                      </td>
                      <td className="px-4 py-3 hidden md:table-cell text-muted tabular-nums">
                        {row.tasksCompleted}
                      </td>
                      <td className="px-4 py-3 text-violet-400 font-semibold tabular-nums">
                        {row.completionPct}%
                      </td>
                      <td className="px-4 py-3 hidden sm:table-cell text-emerald-400 tabular-nums">
                        {row.avgAccuracy}%
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </main>
    </div>
  );
}
