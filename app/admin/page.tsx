"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  AlertTriangle,
  CheckCircle2,
  Loader2,
  RotateCcw,
  Search,
  ShieldCheck,
  User,
} from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { isAdminEmail } from "@/lib/admin";
import { resetStudentDayRange } from "@/lib/admin/reset-days";
import { clearQuizCompletion, reconcileProgressWithCompletions } from "@/lib/quiz/completion-state";
import { loadStoreFromFirestore, saveStoreToFirestore } from "@/lib/firebase/firestore";
import { writeLocalCache } from "@/lib/storage/client";
import type { LocalStudentStore } from "@/lib/storage/types";

interface CompletedQuizInfo {
  quizId: string;
  day: number;
  subject: string;
  topic: string;
}

function parseQuizId(quizId: string): CompletedQuizInfo {
  const parts = quizId.split("-");
  const day = parseInt((parts[0] ?? "day0").replace("day", ""), 10);
  const subject = parts[1] ?? "";
  const topic = parts.slice(2).join("-");
  return { quizId, day, subject, topic };
}

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [searchId, setSearchId] = useState("");
  const [loading, setLoading] = useState(false);
  const [store, setStore] = useState<LocalStudentStore | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [resetting, setResetting] = useState<string | null>(null);
  const [resettingDays, setResettingDays] = useState<string | null>(null);
  const [resetDone, setResetDone] = useState<string[]>([]);

  useEffect(() => {
    if (!authLoading && !isAdminEmail(user?.email)) {
      router.replace("/");
    }
  }, [user, authLoading, router]);

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-950">
        <Loader2 className="h-8 w-8 animate-spin text-violet-400" />
      </div>
    );
  }

  if (!isAdminEmail(user?.email)) return null;

  async function loadStudent() {
    const id = searchId.trim();
    if (!id) return;
    setLoading(true);
    setError(null);
    setStore(null);
    setResetDone([]);
    try {
      const data = await loadStoreFromFirestore(id);
      if (!data) {
        setError(
          "Student not found. Make sure you pasted the correct Firebase UID and that Firestore rules allow admin access (see instructions below)."
        );
        return;
      }
      setStore(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load student");
    } finally {
      setLoading(false);
    }
  }

  async function resetDayRange(fromDay: number, toDay: number) {
    if (!store) return;
    const label = `days-${fromDay}-${toDay}`;
    setResettingDays(label);
    setError(null);
    try {
      const updated = reconcileProgressWithCompletions(
        resetStudentDayRange(store, fromDay, toDay)
      );
      await saveStoreToFirestore(updated);
      setStore(updated);
      if (user?.uid === updated.uid) {
        writeLocalCache(updated);
      }
      setResetDone((prev) => [...prev, label]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Day range reset failed");
    } finally {
      setResettingDays(null);
    }
  }

  async function resetQuiz(quizId: string) {
    if (!store) return;
    setResetting(quizId);
    setError(null);
    try {
      const updated = clearQuizCompletion(store, quizId);
      await saveStoreToFirestore(updated);
      setStore(updated);
      if (user?.uid === updated.uid) {
        writeLocalCache(updated);
      }
      setResetDone((prev) => [...prev, quizId]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Reset failed");
    } finally {
      setResetting(null);
    }
  }

  const quizzes = (store?.completedQuizzes ?? []).map(parseQuizId);
  const byDay = quizzes.reduce<Record<number, CompletedQuizInfo[]>>((acc, q) => {
    (acc[q.day] ??= []).push(q);
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-zinc-950 px-4 py-10 text-white">
      <div className="mx-auto max-w-2xl space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <ShieldCheck className="h-7 w-7 text-violet-400" />
          <h1 className="text-2xl font-bold">Admin — Reset Quiz</h1>
        </div>

        {/* Firestore rules notice */}
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-200">
          <p className="font-semibold">One-time setup required</p>
          <p className="mt-1 text-amber-300/80">
            Students must be able to write their own doc. In Firebase Console → Firestore →
            Rules, use something like:
          </p>
          <pre className="mt-2 overflow-x-auto rounded bg-black/40 p-2 text-xs text-emerald-300">
            {`match /students/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
  allow read, write: if request.auth.token.email == 'dancetoneeraj@gmail.com';
  match /quizReviews/{reviewId} {
    allow read, write: if request.auth != null && request.auth.uid == userId;
    allow read, write: if request.auth.token.email == 'dancetoneeraj@gmail.com';
  }
}`}
          </pre>
        </div>

        {/* Search */}
        <div>
          <p className="mb-2 text-sm text-zinc-400">
            Enter a student&apos;s Firebase UID (Firebase Console → Authentication → find the
            student → copy UID).
          </p>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Firebase UID"
              value={searchId}
              onChange={(e) => setSearchId(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && void loadStudent()}
              className="flex-1 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white placeholder-zinc-500 outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500"
            />
            <button
              onClick={() => void loadStudent()}
              disabled={loading || !searchId.trim()}
              className="flex items-center gap-2 rounded-xl bg-violet-600 px-4 py-3 text-sm font-medium hover:bg-violet-500 disabled:opacity-50"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
              Load
            </button>
          </div>
        </div>

        {error && (
          <div className="flex items-start gap-2 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {resetDone.length > 0 && (
          <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-300">
            <CheckCircle2 className="mr-2 inline h-4 w-4" />
            {resetDone.length} reset{resetDone.length > 1 ? "s" : ""} saved to cloud.
            Student should open the dashboard once to refresh (same browser).
          </div>
        )}

        {/* Student info */}
        {store && (
          <>
            <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-5 py-4">
              <User className="h-5 w-5 text-zinc-400" />
              <div className="flex-1">
                <p className="font-medium">{store.displayName}</p>
                <p className="text-xs text-zinc-400">{store.email}</p>
                <p className="text-xs text-zinc-500">UID: {store.uid}</p>
              </div>
            </div>

            <div className="rounded-xl border border-orange-500/30 bg-orange-500/10 px-4 py-4">
              <p className="text-sm font-semibold text-orange-200">
                Full day reset (retake from scratch)
              </p>
              <p className="mt-1 text-xs text-orange-200/80">
                Clears quizzes, comprehension, vocabulary, and day flags for the
                range. Student opens the dashboard once on their device to sync.
              </p>
              <button
                type="button"
                onClick={() => void resetDayRange(1, 5)}
                disabled={resettingDays === "days-1-5"}
                className="mt-3 flex items-center gap-1.5 rounded-lg border border-orange-500/40 bg-orange-500/15 px-3 py-2 text-xs font-medium text-orange-200 hover:bg-orange-500/25 disabled:opacity-50"
              >
                {resettingDays === "days-1-5" ? (
                  <Loader2 className="h-3 w-3 animate-spin" />
                ) : (
                  <RotateCcw className="h-3 w-3" />
                )}
                Reset days 1–5 completely
              </button>
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
