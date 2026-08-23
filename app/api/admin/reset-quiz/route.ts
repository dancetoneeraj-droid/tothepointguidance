import { NextRequest, NextResponse } from "next/server";
import { isAdminEmail } from "@/lib/admin";
import { clearQuizCompletion } from "@/lib/quiz/completion-state";
import { loadStoreFromFirestore, saveStoreToFirestore } from "@/lib/firebase/firestore";

/**
 * POST /api/admin/reset-quiz
 * Body: { adminEmail: string, studentId: string, quizId: string }
 */
export async function POST(req: NextRequest) {
  const body = await req.json() as {
    adminEmail?: string;
    studentId?: string;
    quizId?: string;
  };

  if (!isAdminEmail(body.adminEmail)) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  }

  const { studentId, quizId } = body;
  if (!studentId || !quizId) {
    return NextResponse.json({ error: "Missing studentId or quizId" }, { status: 400 });
  }

  const store = await loadStoreFromFirestore(studentId);
  if (!store) {
    return NextResponse.json({ error: "Student not found in Firestore" }, { status: 404 });
  }

  const updated = clearQuizCompletion(store, quizId);
  await saveStoreToFirestore(updated);

  return NextResponse.json({
    ok: true,
    message: `Quiz "${quizId}" reset for student ${studentId}`,
    quizId,
  });
}

/**
 * GET /api/admin/reset-quiz?adminEmail=...&studentId=...
 */
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const adminEmail = searchParams.get("adminEmail");
  const studentId = searchParams.get("studentId");

  if (!isAdminEmail(adminEmail)) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 403 });
  }
  if (!studentId) {
    return NextResponse.json({ error: "Missing studentId" }, { status: 400 });
  }

  const store = await loadStoreFromFirestore(studentId);
  if (!store) {
    return NextResponse.json({ error: "Student not found in Firestore" }, { status: 404 });
  }

  return NextResponse.json({
    studentId,
    displayName: store.displayName,
    email: store.email,
    completedQuizzes: store.completedQuizzes ?? [],
    updatedAt: store.updatedAt,
  });
}
