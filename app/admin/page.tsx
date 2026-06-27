"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AlertTriangle, CheckCircle2, Loader2, RotateCcw, Search, ShieldCheck, User } from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { isAdminEmail } from "@/lib/admin";

interface CompletedQuizInfo {
  quizId: string;
  day: number;
  subject: string;
  topic: string;
}

interface StudentData {
  studentId: string;
  displayName: string;
  email: string;
  completedQuizzes: string[];
  updatedAt: string;
}

function parseQuizId(quizId: string): CompletedQuizInfo {
  // Format: "day4-maths-trigonometry"
  const parts = quizId.split("-");
  const day = parseInt((parts[0] ?? "day0").replace("day", ""), 10);
  const subject = parts[1] ?? "";
  const topic = parts.slice(2).join("-");
  return { quizId, day, subject, topic };
}

export default function AdminPage() {
  const { user } = useAuth();
  const router = useRouter();

  const [searchId, setSearchId] = useState("");
  const [loading, setLoading] = useState(false);
  const [studentData, setStudentData] = useState<StudentData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [resetting, setResetting] = useState<string | null>(null);
  const [resetDone, setResetDone] = useState<string[]>([]);

  // Redirect non-admins
  useEffect(() => {
    if (user !== undefined && !isAdminEmail(user?.email)) {
      router.replace("/");
    }
  }, [user, router]);

  if (user === undefined) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-950">
        <Loader2 className="h-8 w-8 animate-spin text-violet-400" />
      </div>
    );
  }

  if (!isAdminEmail(user?.email)) {
    return null;
  }

  async function loadStudent() {
    const id = searchId.trim();
    if (!id) return;
    setLoading(true);
    setError(null);
    setStudentData(null);
    setResetDone([]);
    try {
      const res = await fetch(
        `/api/admin/reset-quiz?adminEmail=${encodeURIComponent(user!.email!)}&studentId=${encodeURIComponent(id)}`
      );
      const data = await res.json() as StudentData & { error?: string };
      if (!res.ok) throw new Error(data.error ?? "Failed to load student");
      setStudentData(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  async function resetQuiz(quizId: string) {
    if (!studentData) return;
    setResetting(quizId);
    setError(null);
    try {
      const res = await fetch("/api/admin/reset-quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          adminEmail: user!.email,
          studentId: studentData.studentId,
          quizId,
        }),
      });
      const data = await res.json() as { ok?: boolean; error?: string };
      if (!res.ok) throw new Error(data.error ?? "Reset failed");
      setResetDone((prev) => [...prev, quizId]);
      setStudentData((prev) =>
        prev
          ? { ...prev, completedQuizzes: prev.completedQuizzes.filter((q) => q !== quizId) }
          : prev
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "Reset failed");
    } finally {
      setResetting(null);
    }
  }

  const quizzes = (studentData?.completedQuizzes ?? []).map(parseQuizId);
  const byDay = quizzes.reduce<Record<number, CompletedQuizInfo[]>>((acc, q) => {
    (acc[q.day] ??= []).push(q);
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-zinc-950 px-4 py-10 text-white">
      <div className="mx-auto max-w-2xl">
        {/* Header */}
        <div className="mb-8 flex items-center gap-3">
          <ShieldCheck className="h-7 w-7 text-violet-400" />
          <h1 className="text-2xl font-bold text-white">Admin — Reset Quiz</h1>
        </div>
        <p className="mb-6 text-sm text-zinc-400">
          Enter a student&apos;s Firebase UID (find it in Firebase Console → Authentication) to
          view and reset their quiz attempts.
        </p>

        {/* Search */}
        <div className="mb-6 flex gap-2">
          <input
            type="text"
            placeholder="Firebase UID (e.g. abc123xyz)"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && void loadStudent()}
            className="flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white placeholder-zinc-500 outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500"
          />
          <button
            onClick={() => void loadStudent()}
            disabled={loading || !searchId.trim()}
            className="flex items-center gap-2 rounded-xl bg-violet-600 px-4 py-3 text-sm font-medium text-white hover:bg-violet-500 disabled:opacity-50"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
            Load
          </button>
        </div>

        {error && (
          <div className="mb-4 flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
            <AlertTriangle className="h-4 w-4 shrink-0" />
            {error}
          </div>
        )}

        {resetDone.length > 0 && (
          <div className="mb-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300">
            <CheckCircle2 className="mr-2 inline h-4 w-4" />
            {resetDone.length} quiz{resetDone.length > 1 ? "zes" : ""} reset. Student will get
            fresh attempt on next login.
          </div>
        )}

        {/* Student info */}
        {studentData && (
          <>
            <div className="mb-6 flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-5 py-4">
              <User className="h-5 w-5 text-zinc-400" />
              <div>
                <p className="font-medium text-white">{studentData.displayName}</p>
                <p className="text-xs text-zinc-400">{studentData.email}</p>
                <p className="text-xs text-zinc-500">UID: {studentData.studentId}</p>
              </div>
            </div>

            {quizzes.length === 0 ? (
              <p className="text-center text-sm text-zinc-500">No completed quizzes found.</p>
            ) : (
              <div className="space-y-4">
                {Object.keys(byDay)
                  .map(Number)
                  .sort((a, b) => a - b)
                  .map((day) => (
                    <div key={day}>
                      <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-zinc-500">
                        Day {day}
                      </p>
                      <div className="space-y-2">
                        {byDay[day]!.map((q) => (
                          <div
                            key={q.quizId}
                            className="flex items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3"
                          >
                            <div>
                              <p className="text-sm font-medium capitalize text-white">
                                {q.topic.replace(/-/g, " ")}
                              </p>
                              <p className="text-xs capitalize text-zinc-400">{q.subject}</p>
                            </div>
                            <button
                              onClick={() => void resetQuiz(q.quizId)}
                              disabled={resetting === q.quizId}
                              className="flex items-center gap-1.5 rounded-lg border border-orange-500/40 bg-orange-500/10 px-3 py-1.5 text-xs font-medium text-orange-300 hover:bg-orange-500/20 disabled:opacity-50"
                            >
                              {resetting === q.quizId ? (
                                <Loader2 className="h-3 w-3 animate-spin" />
                              ) : (
                                <RotateCcw className="h-3 w-3" />
                              )}
                              Reset
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
