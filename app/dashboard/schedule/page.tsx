"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Target } from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { DayWiseProgressList } from "@/components/dashboard/DayWiseProgressList";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { syncStudentToServer } from "@/lib/api/ecosystem";
import {
  collectDayProgressMap,
  getCompletedTaskIds,
  getDayWiseProgress,
} from "@/lib/tasks/progress-sync";
import {
  getOverallTaskProgress,
  getTotalProgramTasks,
} from "@/lib/tasks/program-tasks";

export default function SchedulePage() {
  const { studentId, progress, user } = useAuth();
  const [overall, setOverall] = useState({
    completed: 0,
    total: 0,
    percent: 0,
  });
  const [dayRows, setDayRows] = useState<
    ReturnType<typeof getDayWiseProgress>
  >([]);

  useEffect(() => {
    if (!studentId || !progress) return;
    const email = user?.email ?? progress.email;
    const map = collectDayProgressMap(studentId);
    setOverall(getOverallTaskProgress(map, email));
    setDayRows(getDayWiseProgress(studentId, email));

    void syncStudentToServer({
      studentId,
      displayName: progress.displayName,
      email,
      currentDay: progress.currentDay,
      tasksCompleted: getCompletedTaskIds(studentId).length,
      streak: progress.streak,
      completedTaskIds: getCompletedTaskIds(studentId),
    });
  }, [studentId, progress, user?.email]);

  if (!progress) return null;

  return (
    <div className="space-y-8 animate-in">
      <header>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground mb-4"
        >
          <ArrowLeft className="h-4 w-4" />
          Dashboard
        </Link>
        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">
          Schedule & Progress
        </h1>
        <p className="text-sm text-muted mt-1">
          {overall.completed} / {overall.total || getTotalProgramTasks()} tasks
          completed · {overall.percent}% overall
        </p>
      </header>

      <Card className="p-5" glow>
        <div className="flex items-center gap-2 mb-4">
          <Target className="h-5 w-5 text-violet-400" />
          <h2 className="font-semibold text-foreground">Overall Task Completion</h2>
        </div>
        <ProgressBar
          value={overall.percent}
          label={`${overall.completed} of ${overall.total} tasks`}
        />
      </Card>

      <Card className="p-5">
        <h2 className="font-semibold text-foreground mb-4">Day-wise progress</h2>
        <p className="text-xs text-muted mb-4">
          <span className="text-emerald-400">Green</span> = 100% complete ·{" "}
          <span className="text-violet-400">Blue</span> = in progress
        </p>
        <DayWiseProgressList days={dayRows} />
      </Card>
    </div>
  );
}
