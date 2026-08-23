"use client";

import { use, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  BookOpen,
  Brain,
  Calculator,
  CheckCircle2,
  Circle,
  FileText,
  Play,
  Target,
  type LucideIcon,
} from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { OverrideModal } from "@/components/ui/Modal";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { PremiumLockCard } from "@/components/auth/PremiumLockCard";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppShell } from "@/components/layout/AppShell";
import { getDailyPlan, isDayPublished } from "@/lib/daily-plans";
import { hasAnyDeckForDay, hasDeckForDay } from "@/lib/study-decks";
import { hasComprehensionForDay } from "@/lib/comprehension";
import {
  formatEnglishGrammarQuizLabel,
  formatReasoningQuizLabel,
  formatTopic,
  getDayAccess,
  getReasoningQuizLabel,
  isDayFullyComplete,
} from "@/lib/day-system";
import {
  getDayProgress,
  isQuizCompletedInView,
  markEnglishSection,
  markGkMaterials,
  readCompletionView,
  recordOverride,
  unlockNextDay,
} from "@/lib/storage/progress";
import { syncStudentProgress } from "@/lib/storage/cloud-pull";
import { Button } from "@/components/ui/Button";

type SubjectKey = "maths" | "reasoning" | "english" | "gk";

type ResourceAction = {
  id: string;
  label: string;
  onClick: () => void;
  loading?: boolean;
};

type ExecutionTask = {
  id: string;
  label: string;
  subtitle: string;
  kind: "quiz" | "reading" | "revision";
  subject: SubjectKey;
  completed: boolean;
  actions: ResourceAction[];
};

const subjectMeta: Record<
  SubjectKey,
  {
    title: string;
    description: string;
    icon: LucideIcon;
  }
> = {
  maths: {
    title: "Maths",
    description: "Topic-wise quiz execution for the day.",
    icon: Calculator,
  },
  reasoning: {
    title: "Reasoning",
    description: "Logical practice and reasoning quiz flow.",
    icon: Brain,
  },
  english: {
    title: "English",
    description: "Grammar, vocabulary, and reading material.",
    icon: BookOpen,
  },
  gk: {
    title: "GK",
    description: "PDFs, notes, revision, and current topics.",
    icon: FileText,
  },
};

export default function DayPage({
  params,
}: {
  params: Promise<{ day: string }>;
}) {
  const { day: dayParam } = use(params);
  const dayNum = parseInt(dayParam, 10);
  const router = useRouter();
  const { studentId, progress, refreshProgress, user } = useAuth();
  const resolvedStudentId = studentId ?? "";
  const [dayProgress, setDayProgress] = useState<Awaited<
    ReturnType<typeof getDayProgress>
  > | null>(null);
  const [pageLoading, setPageLoading] = useState(true);
  const [showOverride, setShowOverride] = useState(false);
  const [overrideGranted, setOverrideGranted] = useState(false);
  const [loadingSection, setLoadingSection] = useState<string | null>(null);
  const [unlocking, setUnlocking] = useState(false);
  const [showStudyFlow, setShowStudyFlow] = useState(false);
  const [selectedSubject, setSelectedSubject] = useState<SubjectKey>("maths");

  const plan = getDailyPlan(dayNum);

  useEffect(() => {
    if (!studentId || !progress) return;
    const currentProgress = progress;
    let cancelled = false;

    async function init() {
      setPageLoading(true);
      try {
        void syncStudentProgress(studentId);

        const access = getDayAccess(dayNum, currentProgress, null, {
          userEmail: user?.email ?? currentProgress.email,
        });

        if (!access.canAccess && access.status === "coming_soon") return;
        if (!access.canAccess && access.status === "premium_locked") return;

        if (!access.canAccess && access.status === "locked_future") {
          router.replace(`/day/${currentProgress.unlockedDay}`);
          return;
        }

        if (access.requiresOverride && !overrideGranted) {
          setShowOverride(true);
        }

        const dp = await getDayProgress(studentId, dayNum);
        if (cancelled) return;
        setDayProgress(dp);
      } finally {
        if (!cancelled) setPageLoading(false);
      }
    }

    void init();
    return () => {
      cancelled = true;
    };
  }, [dayNum, overrideGranted, router, studentId, user?.email]);

  const refreshDayState = useCallback(async () => {
    const dp = await getDayProgress(resolvedStudentId, dayNum);
    setDayProgress(dp);
  }, [dayNum, resolvedStudentId]);

  const handleUnlockNext = async () => {
    setUnlocking(true);
    await unlockNextDay(resolvedStudentId, dayNum);
    await refreshProgress();
    setUnlocking(false);
    router.push(`/day/${dayNum + 1}`);
  };

  const handleOverride = async () => {
    await recordOverride(resolvedStudentId, {
      fromDay: dayNum - 1,
      toDay: dayNum,
      timestamp: new Date().toISOString(),
    });
    setOverrideGranted(true);
    setShowOverride(false);
    await refreshProgress();
  };

  const markEnglish = useCallback(
    async (section: "grammar" | "vocabulary" | "comprehension") => {
      setLoadingSection(`english-${section}`);
      await markEnglishSection(resolvedStudentId, dayNum, section);
      await refreshDayState();
      setLoadingSection(null);
    },
    [dayNum, refreshDayState, resolvedStudentId]
  );

  const markGk = useCallback(async () => {
    setLoadingSection("gk-materials");
    await markGkMaterials(resolvedStudentId, dayNum);
    await refreshDayState();
    setLoadingSection(null);
  }, [dayNum, refreshDayState, resolvedStudentId]);

  const openEnglishResource = useCallback(
    async (
      section: "grammar" | "vocabulary" | "comprehension",
      url?: string
    ) => {
      if (!url) return;
      const isExternal = /^https?:\/\//i.test(url);
      if (!isExternal) {
        const response = await fetch(url, { method: "HEAD" }).catch(() => null);
        if (!response?.ok) {
          window.alert(
            "This PDF is not uploaded yet. Please use the available study resource for now."
          );
          return;
        }
      }
      window.open(url, "_blank", "noopener,noreferrer");
      await markEnglish(section);
    },
    [markEnglish]
  );

  const openGkResource = useCallback(
    async (url?: string) => {
      if (!url) return;
      const isExternal = /^https?:\/\//i.test(url);
      if (!isExternal) {
        const response = await fetch(url, { method: "HEAD" }).catch(() => null);
        if (!response?.ok) {
          window.alert(
            "This file is not uploaded yet. Please use available notes for now."
          );
          return;
        }
      }
      window.open(url, "_blank", "noopener,noreferrer");
      await markGk();
    },
    [markGk]
  );

  const tasks = useMemo<ExecutionTask[]>(() => {
    if (!plan || !dayProgress) return [];

    const completionView = readCompletionView(studentId);
    const quizDone = (
      subject: "maths" | "reasoning" | "gk" | "english",
      topic: string,
      from?: number
    ) =>
      completionView
        ? isQuizCompletedInView(completionView, dayNum, subject, topic, from)
        : false;

    const isDay1NounFlow = dayNum === 1 && plan.english.grammarQuiz === "noun";
    const hasInlineGrammarQuiz = !!plan.english.grammarQuiz;
    const grammarQuizLabel = formatEnglishGrammarQuizLabel(
      plan.english.grammarQuizLabel
    );
    const grammarQuizQuestions = plan.english.grammarQuizQuestions ?? 25;
    const grammarQuizDuration = plan.english.grammarQuizDuration ?? 10;

    return [
      ...plan.maths.map((mathTopic, index) => {
        const done = quizDone("maths", mathTopic.topic, mathTopic.from);
        return {
        id: `maths-${mathTopic.topic}`,
        label: `Maths Quiz ${index + 1}`,
        subtitle: `${formatTopic(mathTopic.topic)} · ${mathTopic.questions} questions · ${mathTopic.duration} min`,
        kind: "quiz" as const,
        subject: "maths" as const,
        completed: done,
        actions: [
          {
            id: `maths-action-${mathTopic.topic}`,
            label: done ? "View result" : "Start quiz",
            onClick: () =>
              router.push(
                `/quiz/maths/${mathTopic.topic}?day=${dayNum}${
                  mathTopic.from !== undefined ? `&from=${mathTopic.from}` : ""
                }`
              ),
          },
        ],
      };
      }),
      ...(plan.reasoning
        ? [
            {
              id: "reasoning",
              label: formatReasoningQuizLabel(
                plan.reasoning.topic,
                plan.reasoning.label
              ),
              subtitle: `${formatReasoningQuizLabel(plan.reasoning.topic, plan.reasoning.label)} · ${plan.reasoning.questions} questions · ${plan.reasoning.duration} min`,
              kind: "quiz" as const,
              subject: "reasoning" as const,
              completed: quizDone(
                "reasoning",
                plan.reasoning.topic,
                plan.reasoning.from
              ),
              actions: [
                {
                  id: "reasoning-action",
                  label: quizDone(
                    "reasoning",
                    plan.reasoning.topic,
                    plan.reasoning.from
                  )
                    ? "View result"
                    : "Start quiz",
                  onClick: () =>
                    router.push(
                      `/quiz/reasoning/${plan.reasoning!.topic}?day=${dayNum}`
                    ),
                },
              ],
            },
          ]
        : []),
      // Extra reasoning quizzes (e.g. Number Series) — each gets its own card.
      ...(plan.reasoningQuizzes ?? []).map((rq) => {
        const done = quizDone("reasoning", rq.topic, rq.from);
        return {
          id: `reasoning-${rq.topic}`,
          label: rq.label ?? formatTopic(rq.topic),
          subtitle: `${rq.questions} questions · ${rq.duration} min`,
          kind: "quiz" as const,
          subject: "reasoning" as const,
          completed: done,
          actions: [
            {
              id: `reasoning-${rq.topic}-action`,
              label: done ? "View result" : "Start quiz",
              onClick: () =>
                router.push(`/quiz/reasoning/${rq.topic}?day=${dayNum}`),
            },
          ],
        };
      }),
      ...(plan.english.grammarPdf ||
      plan.english.grammarQuiz ||
      plan.english.grammarMindmap
        ? [
            {
              id: "english-grammar",
              label: "English Grammar",
              subtitle: isDay1NounFlow
                ? "NOUN basic PDF reading · 20-30 min read time"
                : hasInlineGrammarQuiz
                  ? `Grammar PDF + Quiz · ${grammarQuizQuestions} questions · ${grammarQuizDuration} min`
                  : plan.english.grammarMindmap
                    ? "Grammar PDF + mind map revision"
                    : "Grammar PDF notes",
              kind: "reading" as const,
              subject: "english" as const,
              completed: dayProgress.english.grammar,
              actions: [
                ...(plan.english.grammarPdf
                  ? [
                      {
                        id: "english-grammar-pdf",
                        label: isDay1NounFlow ? "Noun PDF" : "Open PDF",
                        onClick: () =>
                          void openEnglishResource(
                            "grammar",
                            plan.english.grammarPdf
                          ),
                        loading: loadingSection === "english-grammar",
                      },
                    ]
                  : []),
                ...(hasInlineGrammarQuiz && plan.english.grammarQuiz
                  ? [
                      {
                        id: `english-grammar-quiz-action-${plan.english.grammarQuiz}`,
                        label: dayProgress.english.grammar
                          ? `View ${grammarQuizLabel} Quiz`
                          : `${grammarQuizLabel} Quiz`,
                        onClick: () =>
                          router.push(
                            `/quiz/english/${plan.english.grammarQuiz}?day=${dayNum}${
                              plan.english.grammarQuizFrom !== undefined
                                ? `&from=${plan.english.grammarQuizFrom}`
                                : ""
                            }`
                          ),
                      },
                    ]
                  : []),
                ...(!isDay1NounFlow && plan.english.grammarMindmap
                  ? [
                      {
                        id: "english-grammar-mindmap",
                        label: "Open Mindmap",
                        onClick: () =>
                          void openEnglishResource(
                            "grammar",
                            plan.english.grammarMindmap
                          ),
                        loading: loadingSection === "english-grammar",
                      },
                    ]
                  : []),
              ],
            },
          ]
        : []),
      // Extra English grammar quizzes (e.g. two Voice sets on the same bank).
      ...(plan.english.grammarQuizzes ?? []).map((eq) => {
        const done = quizDone("english", eq.topic, eq.from);
        const label = formatEnglishGrammarQuizLabel(eq.label);
        const fromQs =
          eq.from !== undefined ? `&from=${eq.from}` : "";
        return {
          id: `english-quiz-${eq.topic}-f${eq.from ?? "x"}`,
          label,
          subtitle: `${eq.questions} questions · ${eq.duration} min`,
          kind: "quiz" as const,
          subject: "english" as const,
          completed: done,
          actions: [
            {
              id: `english-quiz-${eq.topic}-f${eq.from ?? "x"}-action`,
              label: done ? `View ${label}` : `Start ${label}`,
              onClick: () =>
                router.push(
                  `/quiz/english/${eq.topic}?day=${dayNum}${fromQs}`
                ),
            },
          ],
        };
      }),
      {
        id: "english-vocabulary",
        label: "English Vocabulary",
        subtitle: hasAnyDeckForDay(dayNum)
          ? "30 words, idioms & one-word — revise circled cards daily"
          : "Vocabulary cards for this day are being added",
        kind: "reading" as const,
        subject: "english" as const,
        completed: dayProgress.english.vocabulary,
        // Vocabulary is split into three spaced-repetition decks. No PDF or
        // mindmap here — only the three card decks.
        actions: [
          ...(hasDeckForDay("vocab", dayNum)
            ? [
                {
                  id: "english-vocab-words",
                  label: "View Vocab",
                  onClick: () => router.push(`/vocab/${dayNum}?type=vocab`),
                },
              ]
            : []),
          ...(hasDeckForDay("idiom", dayNum)
            ? [
                {
                  id: "english-vocab-idiom",
                  label: "View Idiom",
                  onClick: () => router.push(`/vocab/${dayNum}?type=idiom`),
                },
              ]
            : []),
          ...(hasDeckForDay("ows", dayNum)
            ? [
                {
                  id: "english-vocab-ows",
                  label: "View One Word",
                  onClick: () => router.push(`/vocab/${dayNum}?type=ows`),
                },
              ]
            : []),
        ],
      },
      {
        id: "english-comprehension",
        label: "English Comprehension",
        subtitle: hasComprehensionForDay(dayNum)
          ? "RC + Cloze test + Para jumbles · one attempt · 5 min"
          : isDay1NounFlow
            ? "NOUN basic PDF reading · 20-30 min read time"
            : "Comprehension reading and practice material",
        kind: "reading" as const,
        subject: "english" as const,
        completed: dayProgress.english.comprehension,
        actions: [
          ...(hasComprehensionForDay(dayNum)
            ? [
                {
                  id: "english-comprehension-practice",
                  label: dayProgress.english.comprehension
                    ? "View Comprehension Result"
                    : "Start Comprehension Quiz",
                  onClick: () => router.push(`/comprehension/${dayNum}`),
                },
              ]
            : []),
          ...(plan.english.comprehensionPdf
            ? [
                {
                  id: "english-comprehension-pdf",
                  label: "Open PDF",
                  onClick: () =>
                    void openEnglishResource(
                      "comprehension",
                      plan.english.comprehensionPdf
                    ),
                  loading: loadingSection === "english-comprehension",
                },
              ]
            : []),
        ],
      },
      ...(false // grammar quiz is now inline inside the grammar card
        ? [
            {
              id: `english-quiz-placeholder`,
              label: "English Quiz",
              subtitle: "",
              kind: "quiz" as const,
              subject: "english" as const,
              completed: false,
              actions: [],
            },
          ]
        : []),
      {
        id: "gk-materials",
        label: plan.gk.materialsNote ? "GK — Polity Revision" : "GK Revision PDF",
        subtitle:
          plan.gk.materialsNote ??
          [
            plan.gk.todayTopicPdf ? "Lecture 1" : null,
            plan.gk.todayTopicPdf2 ? "Lecture 2" : null,
            plan.gk.todayTopicPdf3 ? "Lecture 3" : null,
            plan.gk.todayTopicPdf4 ? "Lecture 4" : null,
            plan.gk.todayMindmap ? "Mindmap" : null,
            plan.gk.todayNotes ? "Notes" : null,
          ]
            .filter(Boolean)
            .join(" + "),
        kind: "reading" as const,
        subject: "gk" as const,
        completed: dayProgress.gk.materialsCompleted,
        actions: [
          ...(plan.gk.todayTopicPdf
            ? [
                {
                  id: "gk-pdf",
                  label: plan.gk.materialsNote ? "Polity PDF 1" : "Lecture 1",
                  onClick: () => void openGkResource(plan.gk.todayTopicPdf),
                  loading: loadingSection === "gk-materials",
                },
              ]
            : []),
          ...(plan.gk.todayTopicPdf2
            ? [
                {
                  id: "gk-pdf2",
                  label: plan.gk.materialsNote ? "Polity PDF 2" : "Lecture 2",
                  onClick: () => void openGkResource(plan.gk.todayTopicPdf2),
                  loading: loadingSection === "gk-materials",
                },
              ]
            : []),
          ...(plan.gk.todayTopicPdf3
            ? [
                {
                  id: "gk-pdf3",
                  label: plan.gk.materialsNote ? "Polity PDF 3" : "Lecture 3",
                  onClick: () => void openGkResource(plan.gk.todayTopicPdf3),
                  loading: loadingSection === "gk-materials",
                },
              ]
            : []),
          ...(plan.gk.todayTopicPdf4
            ? [
                {
                  id: "gk-pdf4",
                  label: plan.gk.materialsNote ? "Polity PDF 4" : "Lecture 4",
                  onClick: () => void openGkResource(plan.gk.todayTopicPdf4),
                  loading: loadingSection === "gk-materials",
                },
              ]
            : []),
          ...(plan.gk.todayMindmap
            ? [
                {
                  id: "gk-mindmap",
                  label: "Open Mindmap",
                  onClick: () => void openGkResource(plan.gk.todayMindmap),
                  loading: loadingSection === "gk-materials",
                },
              ]
            : []),
          ...(plan.gk.todayNotes
            ? [
                {
                  id: "gk-notes",
                  label: "Open Notes",
                  onClick: () => void openGkResource(plan.gk.todayNotes),
                  loading: loadingSection === "gk-materials",
                },
              ]
            : []),
        ],
      },
      ...(dayNum > 1 && !!plan.gk.revisionQuiz
        ? [
            {
              id: "gk-revision",
              label: "GK Revision Quiz",
              subtitle: `${formatTopic(plan.gk.revisionTopic ?? "revision")} · 20 questions · 25 min`,
              kind: "revision" as const,
              subject: "gk" as const,
              completed: quizDone("gk", plan.gk.revisionQuiz, plan.gk.from),
              actions: [
                {
                  id: "gk-revision-action",
                  label: quizDone("gk", plan.gk.revisionQuiz, plan.gk.from)
                    ? "View result"
                    : "Start quiz",
                  onClick: () =>
                    router.push(`/quiz/gk/revision?day=${dayNum}`),
                },
              ],
            },
          ]
        : []),
    ].filter((task) => task.actions.length > 0);
  }, [
    dayNum,
    dayProgress,
    loadingSection,
    openEnglishResource,
    openGkResource,
    plan,
    router,
    studentId,
  ]);

  const pendingTasks = useMemo(
    () => tasks.filter((task) => !task.completed),
    [tasks]
  );
  const completedTasks = useMemo(
    () => tasks.filter((task) => task.completed),
    [tasks]
  );

  const totalTasks = tasks.length;
  const completedCount = completedTasks.length;
  const completionPercent =
    totalTasks > 0 ? Math.round((completedCount / totalTasks) * 100) : 0;
  const dayComplete = dayProgress ? isDayFullyComplete(dayProgress) : false;
  const currentUnlockedDay = progress?.unlockedDay ?? 0;
  const canUnlockNext =
    dayComplete &&
    dayNum === currentUnlockedDay &&
    isDayPublished(dayNum + 1);

  const openStudyFlow = () => {
    setShowStudyFlow(true);
    setSelectedSubject(pendingTasks[0]?.subject ?? "maths");
    requestAnimationFrame(() => {
      document
        .getElementById("study-flow")
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  };

  const handlePrimaryAction = async () => {
    if (canUnlockNext) {
      await handleUnlockNext();
      return;
    }
    if (showStudyFlow) {
      document
        .getElementById("study-flow")
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    openStudyFlow();
  };

  const selectedSubjectTasks = tasks.filter(
    (task) => task.subject === selectedSubject
  );
  const isDay1NounFlow = dayNum === 1 && plan?.english.grammarQuiz === "noun";

  if (!progress || !studentId) return null;

  const dayAccess = getDayAccess(dayNum, progress, null, {
    userEmail: user?.email ?? progress.email,
  });

  if (dayAccess.status === "premium_locked") {
    return (
      <ProtectedRoute>
        <AppShell>
          <PremiumLockCard day={dayNum} />
        </AppShell>
      </ProtectedRoute>
    );
  }

  if (!isDayPublished(dayNum) || !plan) {
    return (
      <ProtectedRoute>
        <AppShell>
          <Card className="mx-auto max-w-md p-8 text-center">
            <h1 className="text-xl font-semibold">Day {dayNum}</h1>
            <p className="mt-2 text-muted">Coming Soon</p>
            <p className="mt-1 text-sm text-muted">
              This day&apos;s content is not published yet.
            </p>
            <Link
              href="/dashboard"
              className="mt-6 inline-block text-sm text-violet-400"
            >
              ← Back to dashboard
            </Link>
          </Card>
        </AppShell>
      </ProtectedRoute>
    );
  }

  if (pageLoading || !dayProgress) {
    return (
      <ProtectedRoute>
        <AppShell>
          <div className="flex items-center justify-center py-20">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-violet-500 border-t-transparent" />
          </div>
        </AppShell>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <AppShell>
        <OverrideModal
          open={showOverride}
          onGoBack={() => router.push(`/day/${dayNum - 1}`)}
          onOverride={() => void handleOverride()}
          previousDay={dayNum - 1}
        />

        <div key={dayNum} className="space-y-8 animate-in">
          <header className="space-y-5">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground"
            >
              <ArrowLeft className="h-4 w-4" />
              Dashboard
            </Link>

            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs text-violet-200">
                <Target className="h-3.5 w-3.5" />
                Today&apos;s mission dashboard
              </div>
              <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                Day {dayNum} Execution Plan
              </h1>
              <p className="mt-2 text-sm leading-6 text-zinc-400">
                Complete all tasks sequentially.
              </p>
            </div>

            <Card glow className="border-white/10 bg-white/[0.03] p-5 sm:p-6">
              <div className="grid gap-3 text-sm sm:grid-cols-3">
                <div className="rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-zinc-500">
                    Total Tasks
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-white">
                    {totalTasks}
                  </p>
                </div>
                <div className="rounded-2xl border border-emerald-500/15 bg-emerald-500/[0.06] px-4 py-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-emerald-300/80">
                    Completed
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-white">
                    {completedCount}
                  </p>
                </div>
                <div className="rounded-2xl border border-violet-500/15 bg-violet-500/[0.06] px-4 py-3">
                  <p className="text-xs uppercase tracking-[0.2em] text-violet-300/80">
                    Completion
                  </p>
                  <p className="mt-2 text-2xl font-semibold text-white">
                    {completionPercent}%
                  </p>
                </div>
              </div>

              <ProgressBar
                value={completionPercent}
                className="mt-5"
                label="Day progress"
              />
            </Card>
          </header>

          <section className="grid gap-6 xl:grid-cols-2">
            <TaskTableCard
              title="Today's Targets"
              tasks={pendingTasks}
              emptyMessage="All targets are completed for today."
              completed={false}
            />
            <TaskTableCard
              title="Completed Targets"
              tasks={completedTasks}
              emptyMessage="Completed targets will appear here automatically."
              completed
            />
          </section>

          <div className="rounded-[2rem] border border-violet-500/20 bg-[linear-gradient(180deg,rgba(124,58,237,0.10),rgba(255,255,255,0.03))] p-4 shadow-[0_0_40px_rgba(124,58,237,0.10)] sm:p-5">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-sm font-medium text-violet-300">
                  Start execution flow
                </p>
                <p className="mt-1 text-sm leading-6 text-zinc-400">
                  Open the subject workflow below. Quiz submissions and resource
                  opens are tracked automatically into completed targets.
                </p>
              </div>
              <Button
                size="lg"
                className="w-full justify-center py-4 text-base lg:w-auto lg:min-w-[260px]"
                onClick={() => void handlePrimaryAction()}
                loading={unlocking}
              >
                {canUnlockNext
                  ? `Complete Day ${dayNum} & Unlock Day ${dayNum + 1}`
                  : `Let's Start Day ${dayNum}`}
              </Button>
            </div>
          </div>

          {showStudyFlow ? (
            <section id="study-flow" className="space-y-6">
              <div>
                <p className="text-sm font-medium text-violet-300">
                  Subject Execution Flow
                </p>
                <h2 className="mt-1 text-2xl font-semibold tracking-tight text-white">
                  Select a subject and continue today&apos;s execution
                </h2>
                <p className="mt-2 text-sm leading-6 text-zinc-400">
                  Open one subject at a time. Completed quizzes, PDFs, notes,
                  and mind maps move automatically into the completed list above.
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {(Object.keys(subjectMeta) as SubjectKey[]).map((subject) => (
                  <SubjectCard
                    key={subject}
                    subject={subject}
                    selected={selectedSubject === subject}
                    tasks={tasks.filter((task) => task.subject === subject)}
                    onSelect={() => setSelectedSubject(subject)}
                  />
                ))}
              </div>

              <Card glow className="border-white/10 bg-white/[0.03] p-6 sm:p-7">
                <div className="flex flex-col gap-3 border-b border-white/10 pb-5 sm:flex-row sm:items-end sm:justify-between">
                  <div>
                    <p className="text-sm font-medium text-violet-300">
                      {subjectMeta[selectedSubject].title}
                    </p>
                    <h3 className="mt-1 text-2xl font-semibold tracking-tight text-white">
                      {subjectMeta[selectedSubject].title} execution targets
                    </h3>
                    <p className="mt-2 text-sm leading-6 text-zinc-400">
                      {subjectMeta[selectedSubject].description}
                    </p>
                  </div>
                  <div className="rounded-full border border-white/10 bg-white/[0.03] px-4 py-2 text-sm text-zinc-400">
                    {selectedSubjectTasks.filter((task) => task.completed).length} /{" "}
                    {selectedSubjectTasks.length} completed
                  </div>
                </div>

                <div className="mt-5 space-y-3">
                  {selectedSubjectTasks.map((task) => (
                    <SubjectTaskRow key={task.id} task={task} />
                  ))}
                </div>
                {selectedSubject === "english" && isDay1NounFlow ? (
                  <div className="mt-4 rounded-2xl border border-violet-400/20 bg-violet-500/10 px-4 py-3 text-sm text-violet-100/90">
                    Note: the pdf is for basic, you can read your own notes too.
                    Expected read time: 20-30 minutes.
                  </div>
                ) : null}
              </Card>
            </section>
          ) : null}
        </div>
      </AppShell>
    </ProtectedRoute>
  );
}

function TaskTableCard({
  title,
  tasks,
  emptyMessage,
  completed,
}: {
  title: string;
  tasks: ExecutionTask[];
  emptyMessage: string;
  completed: boolean;
}) {
  return (
    <Card glow className="border-white/10 bg-white/[0.03] p-6 sm:p-7">
      <div className="flex items-center justify-between gap-3 border-b border-white/10 pb-4">
        <div>
          <h2 className="text-xl font-semibold tracking-tight text-white">
            {title}
          </h2>
          <p className="mt-1 text-sm text-zinc-400">
            {tasks.length} task{tasks.length === 1 ? "" : "s"}
          </p>
        </div>
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-2xl border ${
            completed
              ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300"
              : "border-white/10 bg-white/[0.03] text-zinc-400"
          }`}
        >
          {completed ? (
            <CheckCircle2 className="h-5 w-5" />
          ) : (
            <Target className="h-5 w-5" />
          )}
        </div>
      </div>

      <div className="mt-4 space-y-2">
        {tasks.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-white/10 bg-white/[0.02] px-4 py-6 text-sm text-zinc-500">
            {emptyMessage}
          </div>
        ) : (
          tasks.map((task) => (
            <TaskListRow key={task.id} task={task} completed={completed} />
          ))
        )}
      </div>
    </Card>
  );
}

function TaskListRow({
  task,
  completed,
}: {
  task: ExecutionTask;
  completed: boolean;
}) {
  return (
    <div
      className={`flex items-start gap-3 rounded-2xl border px-4 py-3 transition-all duration-300 ${
        completed
          ? "border-emerald-500/20 bg-emerald-500/[0.07] shadow-[0_0_24px_rgba(16,185,129,0.08)]"
          : "border-white/10 bg-white/[0.03]"
      }`}
    >
      <div
        className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border ${
          completed
            ? "border-emerald-400/40 bg-emerald-500/15 text-emerald-300"
            : "border-white/10 bg-white/[0.03] text-zinc-500"
        }`}
      >
        {completed ? (
          <CheckCircle2 className="h-4 w-4" />
        ) : (
          <Circle className="h-4 w-4" />
        )}
      </div>

      <div className="min-w-0">
        <p
          className={`text-sm font-medium ${
            completed ? "text-emerald-50" : "text-white"
          }`}
        >
          {task.label}
        </p>
        <p
          className={`mt-1 text-xs ${
            completed ? "text-emerald-100/70" : "text-zinc-500"
          }`}
        >
          {task.subtitle}
        </p>
      </div>
    </div>
  );
}

function SubjectCard({
  subject,
  tasks,
  selected,
  onSelect,
}: {
  subject: SubjectKey;
  tasks: ExecutionTask[];
  selected: boolean;
  onSelect: () => void;
}) {
  const meta = subjectMeta[subject];
  const Icon = meta.icon;
  const completedCount = tasks.filter((task) => task.completed).length;

  return (
    <button
      type="button"
      onClick={onSelect}
      className={`rounded-[1.5rem] border p-5 text-left transition-all duration-300 ${
        selected
          ? "border-violet-400/30 bg-violet-500/[0.10] shadow-[0_0_32px_rgba(124,58,237,0.12)]"
          : "border-white/10 bg-white/[0.03] hover:border-white/15 hover:bg-white/[0.05]"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div
          className={`flex h-12 w-12 items-center justify-center rounded-2xl border ${
            selected
              ? "border-violet-400/30 bg-violet-500/15 text-violet-300"
              : "border-white/10 bg-white/[0.03] text-zinc-300"
          }`}
        >
          <Icon className="h-5 w-5" />
        </div>
        <span className="rounded-full border border-white/10 bg-white/[0.03] px-2.5 py-1 text-xs text-zinc-400">
          {completedCount}/{tasks.length}
        </span>
      </div>

      <h3 className="mt-5 text-xl font-semibold text-white">{meta.title}</h3>
      <p className="mt-2 text-sm leading-6 text-zinc-400">{meta.description}</p>
    </button>
  );
}

function SubjectTaskRow({ task }: { task: ExecutionTask }) {
  return (
    <div
      className={`rounded-2xl border p-4 transition-all duration-300 ${
        task.completed
          ? "border-emerald-500/20 bg-emerald-500/[0.08] shadow-[0_0_24px_rgba(16,185,129,0.08)]"
          : "border-white/10 bg-white/[0.03]"
      }`}
    >
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <p
              className={`text-base font-semibold ${
                task.completed ? "text-emerald-50" : "text-white"
              }`}
            >
              {task.label}
            </p>
            <span className="rounded-full border border-white/10 bg-white/[0.03] px-2.5 py-1 text-[11px] font-medium text-zinc-400">
              {task.kind === "quiz"
                ? "Quiz"
                : task.kind === "revision"
                  ? "Revision"
                  : "Study"}
            </span>
          </div>
          <p
            className={`mt-1 text-sm leading-6 ${
              task.completed ? "text-emerald-100/70" : "text-zinc-400"
            }`}
          >
            {task.subtitle}
          </p>
        </div>

        <div className="flex flex-wrap gap-2 lg:justify-end">
          {task.actions.length > 0 ? (
            task.actions.map((action) => (
              <Button
                key={action.id}
                variant={task.completed ? "secondary" : "primary"}
                size="sm"
                onClick={action.onClick}
                loading={action.loading}
              >
                {task.kind === "quiz" || task.kind === "revision" ? (
                  <Play className="h-4 w-4" />
                ) : (
                  <BookOpen className="h-4 w-4" />
                )}
                {action.label}
              </Button>
            ))
          ) : (
            <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-2 text-xs text-zinc-500">
              Resource unavailable
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
