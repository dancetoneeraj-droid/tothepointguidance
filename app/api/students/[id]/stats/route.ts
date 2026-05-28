import { NextResponse } from "next/server";
import { getStudentDbStats } from "@/lib/db/leaderboard";

export async function GET(
  _request: Request,
  context: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await context.params;
    const stats = getStudentDbStats(id);
    return NextResponse.json({ stats });
  } catch (e) {
    console.error("stats error", e);
    return NextResponse.json({ stats: null });
  }
}
