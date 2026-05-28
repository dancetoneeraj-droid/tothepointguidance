import { NextResponse } from "next/server";
import { getPublicLeaderboard } from "@/lib/db/leaderboard";

export async function GET() {
  try {
    const rows = getPublicLeaderboard(200);
    return NextResponse.json({ rows });
  } catch (e) {
    console.error("leaderboard error", e);
    return NextResponse.json({ rows: [] });
  }
}
