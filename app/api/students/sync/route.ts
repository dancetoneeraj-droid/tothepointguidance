import { NextResponse } from "next/server";
import { getTotalProgramTasks } from "@/lib/tasks/program-tasks";
import { updateLeaderboardEntry } from "@/lib/firebase/firestore";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const studentId = String(body.studentId ?? "");
    if (!studentId) {
      return NextResponse.json({ error: "studentId required" }, { status: 400 });
    }

    const tasksCompleted = Number(body.tasksCompleted ?? 0);
    const totalTasks = getTotalProgramTasks();
    const completionPct =
      totalTasks > 0 ? Math.round((tasksCompleted / totalTasks) * 100) : 0;

    await updateLeaderboardEntry(studentId, {
      displayName: String(body.displayName ?? "Student"),
      currentDay: Number(body.currentDay ?? 1),
      tasksCompleted,
      completionPct,
      accuracy: Number(body.accuracy ?? 0),
      streak: Number(body.streak ?? 0),
      updatedAt: new Date().toISOString(),
    });

    return NextResponse.json({ ok: true });
  } catch (e) {
    console.error("student sync error", e);
    return NextResponse.json({ error: "Sync failed" }, { status: 500 });
  }
}
