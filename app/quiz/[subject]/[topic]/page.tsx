"use client";

import { use, useCallback, useMemo, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { QuizEngine } from "@/components/quiz/QuizEngine";
import { QuizResultScreen } from "@/components/quiz/QuizResultScreen";
import { PremiumLockCard } from "@/components/auth/PremiumLockCard";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { Card } from "@/components/ui/Card";
import { canAccessDay, resolveStudentEmail } from "@/lib/premium-access";
import {
  clearActivePausedQuiz,
  getActivePausedQuiz,
  loadQuizDraft,
  setActivePausedQuiz,
  unpauseQuizDraft,
} from "@/lib/quiz/session-persistence";
import { getDailyPlan } from "@/lib/daily-plans";
import { formatQuizTitle, getEnglishQuizLabel, getReasoningQuizLabel } from "@/lib/day-system";
import { MATHS_QUIZ_DURATION, MATHS_QUIZ_QUESTIONS } from "@/lib/maths-topics";
import {
  getQuizReviewRecord,
  getTopicIndex,
  hasCompletedQuiz,
  quizCompletionId,
  recordQuizCompletion,
  saveQuizReviewRecord,
} from "@/lib/storage";
import { getQuestionBank } from "@/lib/quiz-loader";
import {
  loadQuizAnalytics,
  saveQuizAnalytics,
  submitQuizToServer,
} from "@/lib/api/ecosystem";
import { updateLeaderboardEntry } from "@/lib/firebase/firestore";
import { getCompletedTaskIds } from "@/lib/tasks/progress-sync";
import { getTotalProgramTasks } from "@/lib/tasks/program-tasks";
import type { QuizResult } from "@/types";
import { buildSessionId, computeNextIndex, resolveQuizSlice } from "@/lib/quiz/session";
import { getReviewQuestions } from "@/lib/quiz/review";

const ENGLISH_QUIZ_QUESTIONS = 25;
const ENGLISH_QUIZ_DURATION = 10;

export default function QuizPage({
  params,
}: {
  params: Promise<{ subject: string; topic: string }>;
}) {
  const { subject: subjectParam, topic } = use(params);
  const searchParams = useSearchParams();
  const day = parseInt(searchParams.get("day") ?? "1", 10);
  const fromParamRaw = searchParams.get("from");
  const fromParam =
    fromParamRaw != null && fromParamRaw !== ""
      ? parseInt(fromParamRaw, 10)
      : undefined;
  const fromParamValid =
    fromParam !== undefined && Number.isFinite(fromParam) ? fromParam : undefined;
  const router = useRouter();
  const { studentId, progress, refreshProgress, user } = useAuth();

  const subject = subjectParam as "maths" | "reasoning" | "gk" | "english";
  const plan = getDailyPlan(day);
  const hasProgress = Boolean(progress);

  /** Bank offset for this day's quiz config (if any) — used in completion / session ids. */
  const quizFrom = useMemo(() => {
    if (fromParamValid !== undefined) return fromParamValid;
    if (!plan) return undefined;
    if (subject === "maths") {
      return plan.maths.find((m) => m.topic === topic)?.from;
    }
    if (subject === "english") {
      const matched = (plan.english.grammarQuizzes ?? []).find(
        (q) => q.topic === topic
      );
      return matched?.from ?? plan.english.grammarQuizFrom;
    }
    if (subject === "reasoning") {
      const extra = plan.reasoningQuizzes?.find((q) => q.topic === topic);
      const cfg =
        plan.reasoning && topic === plan.reasoning.topic
          ? plan.reasoning
          : extra ?? plan.reasoning;
      return cfg?.from;
    }
    if (subject === "gk") {
      return plan.gk.from;
    }
    return undefined;
  }, [plan, subject, topic, fromParamValid]);

  /** Stable for one visit — progress refresh after submit must not load the next 25 Q. */
  const sessionLockKey = `${studentId ?? "none"}:${day}:${subject}:${topic}:f${quizFrom ?? "x"}:official`;

  type FrozenQuizConfig = {
    questions: ReturnType<typeof resolveQuizSlice>["questions"];
    duration: number;
    count: number;
    setStart: number;
    storedIndex: number;
    sessionId: string;
    subjectLabel: string;
    isPartial: boolean;
  };

  const frozenQuiz = useMemo(() => {
    if (!progress || !plan) return null;

    const bank = getQuestionBank(subject, topic);
    const storedIndex = getTopicIndex(progress, subject, topic);

    let questionCount = MATHS_QUIZ_QUESTIONS;
    let durationMinutes = MATHS_QUIZ_DURATION;

    if (subject === "maths") {
      const cfg = plan.maths.find((m) => m.topic === topic);
      questionCount = cfg?.questions ?? MATHS_QUIZ_QUESTIONS;
      durationMinutes = cfg?.duration ?? MATHS_QUIZ_DURATION;
      if (cfg?.from !== undefined) {
        const slice = resolveQuizSlice(bank, cfg.from, questionCount);
        return {
          questions: slice.questions,
          duration: durationMinutes,
          count: questionCount,
          setStart: slice.setStart,
          storedIndex: cfg.from,
          sessionId: buildSessionId(subject, topic, day, slice.setStart),
          subjectLabel: "Mathematics",
          isPartial: slice.isPartial,
        };
      }
    } else if (subject === "english") {
      const matchedQuiz = (plan.english.grammarQuizzes ?? []).find(
        (q) =>
          q.topic === topic &&
          (quizFrom === undefined || q.from === quizFrom)
      );
      questionCount = Math.min(
        matchedQuiz?.questions ??
          plan.english.grammarQuizQuestions ??
          ENGLISH_QUIZ_QUESTIONS,
        bank.length
      );
      durationMinutes =
        matchedQuiz?.duration ??
        plan.english.grammarQuizDuration ??
        ENGLISH_QUIZ_DURATION;
      const from =
        quizFrom ?? matchedQuiz?.from ?? plan.english.grammarQuizFrom;
      if (from !== undefined) {
        const slice = resolveQuizSlice(bank, from, questionCount);
        return {
          questions: slice.questions,
          duration: durationMinutes,
          count: questionCount,
          setStart: slice.setStart,
          storedIndex: from,
          sessionId: buildSessionId(subject, topic, day, slice.setStart),
          subjectLabel: "English",
          isPartial: slice.isPartial,
        };
      }
    } else if (subject === "reasoning") {
      // Primary reasoning topic OR any extra quiz from reasoningQuizzes[].
      const extraCfg = plan.reasoningQuizzes?.find((q) => q.topic === topic);
      const cfg =
        plan.reasoning && topic === plan.reasoning.topic
          ? plan.reasoning
          : extraCfg ?? plan.reasoning;
      if (!cfg) return null;
      questionCount = cfg.questions;
      durationMinutes = cfg.duration;
      const from = cfg.from ?? 0;
      const slice = resolveQuizSlice(bank, from, questionCount);
      return {
        questions: slice.questions,
        duration: durationMinutes,
        count: questionCount,
        setStart: slice.setStart,
        storedIndex: from,
        sessionId: buildSessionId(subject, topic, day, slice.setStart),
        subjectLabel: "Reasoning",
        isPartial: slice.isPartial,
      };
    } else if (subject === "gk") {
      questionCount = 25;
      durationMinutes = 20;
      if (plan.gk.from !== undefined) {
        const slice = resolveQuizSlice(bank, plan.gk.from, questionCount);
        return {
          questions: slice.questions,
          duration: durationMinutes,
          count: questionCount,
          setStart: slice.setStart,
          storedIndex: plan.gk.from,
          sessionId: buildSessionId(subject, topic, day, slice.setStart),
          subjectLabel: "General Knowledge",
          isPartial: slice.isPartial,
        };
      }
    }

    const slice = resolveQuizSlice(bank, storedIndex, questionCount);

    return {
      questions: slice.questions,
      duration: durationMinutes,
      count: questionCount,
      setStart: slice.setStart,
      storedIndex,
      sessionId: buildSessionId(subject, topic, day, slice.setStart),
      subjectLabel:
        subject === "maths"
          ? "Mathematics"
          : subject === "english"
            ? "English"
          : subject === "reasoning"
            ? "Reasoning"
            : "General Knowledge",
      isPartial: slice.isPartial,
    };
    // Intentionally omit `progress` — refresh after submit must not advance the slice.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionLockKey, plan, subject, topic, day, hasProgress, quizFrom]);

  const quizConfig = useMemo(() => {
    if (frozenQuiz) return frozenQuiz;
    return {
      questions: [] as FrozenQuizConfig["questions"],
      duration: MATHS_QUIZ_DURATION,
      count: MATHS_QUIZ_QUESTIONS,
      setStart: 0,
      storedIndex: 0,
      sessionId: "loading",
      subjectLabel: subject.toUpperCase(),
      isPartial: false,
    };
  }, [frozenQuiz, subject]);

  const title = formatQuizTitle(subject, topic, day, {
    englishLabel: getEnglishQuizLabel(plan, topic, quizFrom),
    reasoningLabel: getReasoningQuizLabel(plan, topic),
  });
  const fromQs =
    quizFrom !== undefined ? `&from=${quizFrom}` : "";
  const analysisPath = `/quiz/${subject}/${topic}/analysis?day=${day}${fromQs}`;
  const solutionsPath = `/quiz/${subject}/${topic}/solutions?day=${day}${fromQs}`;
  const returnPath = `/day/${day}`;
  const hasOfficialAttempt = useMemo(
    () =>
      studentId
        ? hasCompletedQuiz(studentId, day, subject, topic, quizFrom)
        : false,
    [studentId, day, subject, topic, quizFrom]
  );
  const storedReview = useMemo(() => {
    if (!studentId) return null;

    const saved = getQuizReviewRecord(studentId, day, subject, topic, quizFrom);
    if (saved) return saved;

    const recent = loadQuizAnalytics();
    if (
      recent &&
      recent.day === day &&
      recent.subject === subject &&
      recent.topic === topic
    ) {
      return recent;
    }

    return null;
  }, [studentId, day, subject, topic, quizFrom]);
  const reviewQuestions = useMemo(() => {
    if (!storedReview) return [];
    const bank = getQuestionBank(subject, topic);
    return getReviewQuestions(bank, storedReview.questionIds);
  }, [storedReview, subject, topic]);

  // If this quiz has a paused draft, resume it in place instead of bouncing
  // the student back to the dashboard. Done before the engine hydrates so it
  // loads in an active (un-paused) state.
  const resumedSessionRef = useRef<string | null>(null);
  if (
    typeof window !== "undefined" &&
    frozenQuiz &&
    frozenQuiz.sessionId !== "loading" &&
    !hasOfficialAttempt &&
    resumedSessionRef.current !== frozenQuiz.sessionId
  ) {
    const draft = loadQuizDraft(
      frozenQuiz.sessionId,
      frozenQuiz.questions.map((q) => q.id)
    );
    if (draft?.isPaused) {
      unpauseQuizDraft(frozenQuiz.sessionId);
    }
    const active = getActivePausedQuiz();
    if (active?.sessionId === frozenQuiz.sessionId) {
      clearActivePausedQuiz();
    }
    resumedSessionRef.current = frozenQuiz.sessionId;
  }

  const handleComplete = useCallback(
    async (result: QuizResult, answers: Record<string, string>) => {
      if (!studentId || !progress) return null;

      const bank = getQuestionBank(subject, topic);
      const newIndex = computeNextIndex(
        quizConfig.storedIndex,
        quizConfig.setStart,
        result.total,
        bank.length,
        true
      );

      await recordQuizCompletion(
        studentId,
        day,
        subject,
        topic,
        {
          correct: result.correct,
          total: result.total,
          newIndex,
          score: result.score,
          accuracy: result.accuracy,
        },
        { from: quizFrom }
      );

      const ranking = await submitQuizToServer({
        studentId,
        displayName: progress.displayName,
        email: user?.email ?? progress.email,
        day,
        subject,
        topic,
        correct: result.correct,
        total: result.total,
        accuracy: result.accuracy,
        scoreMarks: result.score,
        timeSeconds: result.timeTakenSeconds,
        isRetry: false,
      });

      const reviewRecord = {
        quizId: quizCompletionId(day, subject, topic, quizFrom),
        title,
        subject,
        topic,
        day,
        questionIds: quizConfig.questions.map((question) => question.id),
        answers,
        result,
        ranking,
        returnPath,
        analysisPath,
        solutionsPath,
        completedAt: new Date().toISOString(),
      };

      saveQuizReviewRecord(studentId, reviewRecord);
      saveQuizAnalytics(reviewRecord);

      await refreshProgress();

      // Update leaderboard immediately after quiz — don't wait for dashboard visit
      try {
        const completedTaskIds = getCompletedTaskIds(studentId);
        const totalTasks = getTotalProgramTasks();
        const completionPct =
          totalTasks > 0
            ? Math.round((completedTaskIds.length / totalTasks) * 100)
            : 0;
        void updateLeaderboardEntry(studentId, {
          displayName: progress.displayName,
          currentDay: progress.currentDay,
          tasksCompleted: completedTaskIds.length,
          completionPct,
          accuracy: result.accuracy,
          streak: progress.streak,
          updatedAt: new Date().toISOString(),
        });
      } catch {
        // Non-critical — leaderboard will update on next dashboard visit
      }

      return ranking;
    },
    [
      studentId,
      progress,
      user?.email,
      subject,
      topic,
      day,
      quizConfig.setStart,
      quizConfig.storedIndex,
      quizConfig.questions,
      quizFrom,
      refreshProgress,
      title,
      returnPath,
      analysisPath,
      solutionsPath,
    ]
  );

  const handlePauseExit = useCallback(() => {
    if (quizConfig.sessionId === "loading") return;
    setActivePausedQuiz({
      sessionId: quizConfig.sessionId,
      title,
      subjectLabel: quizConfig.subjectLabel,
      resumePath: `/quiz/${subject}/${topic}?day=${day}`,
      pausedAt: new Date().toISOString(),
    });
    router.push("/dashboard");
  }, [
    quizConfig.sessionId,
    quizConfig.subjectLabel,
    title,
    subject,
    topic,
    day,
    router,
  ]);

  if (!studentId || !progress) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#08080a]">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-violet-500 border-t-transparent" />
      </div>
    );
  }

  if (!canAccessDay(day, resolveStudentEmail(user?.email, progress.email))) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#08080a] py-12 px-4">
          <PremiumLockCard day={day} />
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#08080a]">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 pt-4">
          <Link
            href={`/day/${day}`}
            className="inline-flex items-center gap-1 text-sm text-zinc-500 hover:text-white transition-colors mb-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Exit to Day {day}
          </Link>
        </div>
        {hasOfficialAttempt ? (
          <div className="mx-auto max-w-7xl px-4 pb-10 pt-6 sm:px-6">
            {storedReview ? (
              <QuizResultScreen
                title={storedReview.title}
                result={storedReview.result}
                ranking={storedReview.ranking}
                questions={reviewQuestions}
                answers={storedReview.answers}
                solutionsPath={solutionsPath}
                analysisPath={analysisPath}
              />
            ) : (
              <Card className="mx-auto max-w-2xl border-white/10 bg-[#121218]/90 p-8 text-center">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-violet-300">
                  Official Attempt Locked
                </p>
                <h1 className="mt-3 text-2xl font-semibold text-white">
                  This quiz has already been submitted.
                </h1>
                <p className="mt-3 text-sm leading-6 text-zinc-400">
                  Only the first attempt is allowed for this test. Detailed
                  review data is not available for this older submission in the
                  current session.
                </p>
              </Card>
            )}
          </div>
        ) : (
          <>
            {quizConfig.isPartial && quizConfig.questions.length > 0 ? (
              <p className="mx-auto mb-2 max-w-7xl px-4 text-xs text-amber-400/90 sm:px-6">
                Showing {quizConfig.questions.length} of {quizConfig.count} questions
                — add more to datas/maths/{topic}.json and run import.
              </p>
            ) : null}
            <QuizEngine
              key={sessionLockKey}
              questions={quizConfig.questions}
              durationMinutes={quizConfig.duration}
              title={title}
              subjectLabel={quizConfig.subjectLabel}
              sessionId={quizConfig.sessionId}
              solutionsPath={solutionsPath}
              analysisPath={analysisPath}
              onComplete={handleComplete}
              onPauseExit={handlePauseExit}
            />
          </>
        )}
      </div>
    </ProtectedRoute>
  );
}
