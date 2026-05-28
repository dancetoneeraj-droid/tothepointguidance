import { NextResponse } from "next/server";
import {
  recordTaskCompletion,
  syncStudentProgress,
} from "@/lib/db/leaderboard";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const studentId = String(body.studentId ?? "");
    if (!studentId) {
      return NextResponse.json({ error: "studentId required" }, { status: 400 });
    }

    syncStudentProgress(studentId, String(body.displayName ?? "Student"), {
      email: body.email ? String(body.email) : undefined,
      currentDay: Number(body.currentDay ?? 1),
      tasksCompleted: Number(body.tasksCompleted ?? 0),
      streak: Number(body.streak ?? 0),
    });

    const taskIds = Array.isArray(body.completedTaskIds)
      ? (body.completedTaskIds as string[])
      : [];
    for (const taskId of taskIds) {
      const dayMatch = taskId.match(/^d(\d+)_/);
      const day = dayMatch ? Number(dayMatch[1]) : 1;
      recordTaskCompletion(studentId, taskId, day);
    }

    return NextResponse.json({ ok: true });
  } catch (e) {
    console.error("student sync error", e);
    return NextResponse.json({ error: "Sync failed" }, { status: 500 });
  }
}
