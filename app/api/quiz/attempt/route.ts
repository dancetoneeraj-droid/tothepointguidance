import { NextResponse } from "next/server";
import { submitQuizAttempt } from "@/lib/db/quiz-ranking";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const result = submitQuizAttempt({
      studentId: String(body.studentId ?? ""),
      displayName: String(body.displayName ?? "Student"),
      email: body.email ? String(body.email) : undefined,
      day: Number(body.day),
      subject: String(body.subject),
      topic: String(body.topic),
      correct: Number(body.correct),
      total: Number(body.total),
      accuracy: Number(body.accuracy),
      scoreMarks: Number(body.scoreMarks ?? body.score ?? 0),
      timeSeconds: Number(body.timeSeconds),
      isRetry: Boolean(body.isRetry),
    });
    return NextResponse.json(result);
  } catch (e) {
    console.error("quiz attempt error", e);
    return NextResponse.json(
      { error: "Failed to record attempt" },
      { status: 500 }
    );
  }
}
