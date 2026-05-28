import { getDb } from "@/lib/db/init";
import { getTotalProgramTasks } from "@/lib/tasks/program-tasks";

export interface LeaderboardRow {
  rank: number;
  studentId: string;
  studentName: string;
  currentDay: number;
  tasksCompleted: number;
  completionPct: number;
  avgAccuracy: number;
}

export function syncStudentProgress(
  studentId: string,
  displayName: string,
  data: {
    email?: string;
    currentDay: number;
    tasksCompleted: number;
    streak: number;
  }
) {
  const database = getDb();
  const totalTasks = getTotalProgramTasks();
  const completionPct =
    totalTasks > 0
      ? Math.round((data.tasksCompleted / totalTasks) * 100)
      : 0;
  const now = new Date().toISOString();

  database
    .prepare(
      `INSERT INTO students
       (id, display_name, email, current_day, tasks_completed, total_tasks, completion_pct, streak, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
       ON CONFLICT(id) DO UPDATE SET
         display_name = excluded.display_name,
         email = COALESCE(excluded.email, students.email),
         current_day = excluded.current_day,
         tasks_completed = excluded.tasks_completed,
         total_tasks = excluded.total_tasks,
         completion_pct = excluded.completion_pct,
         streak = excluded.streak,
         updated_at = excluded.updated_at`
    )
    .run(
      studentId,
      displayName,
      data.email ?? null,
      data.currentDay,
      data.tasksCompleted,
      totalTasks,
      completionPct,
      data.streak,
      now
    );
}

export function recordTaskCompletion(
  studentId: string,
  taskId: string,
  day: number
) {
  const database = getDb();
  database
    .prepare(
      `INSERT OR IGNORE INTO task_completions (student_id, task_id, day, completed_at)
       VALUES (?, ?, ?, ?)`
    )
    .run(studentId, taskId, day, new Date().toISOString());
}

export function getPublicLeaderboard(limit = 100): LeaderboardRow[] {
  const database = getDb();
  const rows = database
    .prepare(
      `SELECT
        s.id,
        s.display_name,
        s.current_day,
        s.tasks_completed,
        s.completion_pct,
        COALESCE(s.avg_accuracy, 0) as avg_accuracy
       FROM students s
       WHERE s.quizzes_attempted > 0 OR s.tasks_completed > 0
       ORDER BY s.completion_pct DESC, s.avg_accuracy DESC, s.tasks_completed DESC
       LIMIT ?`
    )
    .all(limit) as Array<{
      id: string;
      display_name: string;
      current_day: number;
      tasks_completed: number;
      completion_pct: number;
      avg_accuracy: number;
    }>;

  return rows.map((r, i) => ({
    rank: i + 1,
    studentId: r.id,
    studentName: r.display_name,
    currentDay: r.current_day,
    tasksCompleted: r.tasks_completed,
    completionPct: r.completion_pct,
    avgAccuracy: r.avg_accuracy,
  }));
}

export interface StudentDbStats {
  tasksCompleted: number;
  totalTasks: number;
  completionPct: number;
  avgAccuracy: number;
  quizzesAttempted: number;
  bestRank: number | null;
  streak: number;
  currentDay: number;
}

export function getStudentDbStats(studentId: string): StudentDbStats | null {
  const database = getDb();
  const row = database
    .prepare(`SELECT * FROM students WHERE id = ?`)
    .get(studentId) as
    | {
        tasks_completed: number;
        total_tasks: number;
        completion_pct: number;
        avg_accuracy: number;
        quizzes_attempted: number;
        best_rank: number | null;
        streak: number;
        current_day: number;
      }
    | undefined;

  if (!row) return null;

  return {
    tasksCompleted: row.tasks_completed,
    totalTasks: row.total_tasks || getTotalProgramTasks(),
    completionPct: row.completion_pct,
    avgAccuracy: row.avg_accuracy,
    quizzesAttempted: row.quizzes_attempted,
    bestRank: row.best_rank,
    streak: row.streak,
    currentDay: row.current_day,
  };
}
