import Database from "better-sqlite3";
import { existsSync, mkdirSync } from "fs";
import { join } from "path";

const DB_DIR = join(process.cwd(), "data");
const DB_PATH = join(DB_DIR, "tothepoint.db");

let db: Database.Database | null = null;

function migrate(database: Database.Database) {
  database.exec(`
    CREATE TABLE IF NOT EXISTS students (
      id TEXT PRIMARY KEY,
      display_name TEXT NOT NULL,
      email TEXT,
      phone TEXT,
      current_day INTEGER NOT NULL DEFAULT 1,
      tasks_completed INTEGER NOT NULL DEFAULT 0,
      total_tasks INTEGER NOT NULL DEFAULT 0,
      completion_pct INTEGER NOT NULL DEFAULT 0,
      avg_accuracy INTEGER NOT NULL DEFAULT 0,
      quizzes_attempted INTEGER NOT NULL DEFAULT 0,
      best_rank INTEGER,
      streak INTEGER NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS quiz_first_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      student_id TEXT NOT NULL,
      quiz_key TEXT NOT NULL,
      day INTEGER NOT NULL,
      subject TEXT NOT NULL,
      topic TEXT NOT NULL,
      correct INTEGER NOT NULL,
      total INTEGER NOT NULL,
      accuracy INTEGER NOT NULL,
      score_marks REAL NOT NULL DEFAULT 0,
      time_seconds INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      UNIQUE(student_id, quiz_key)
    );

    CREATE INDEX IF NOT EXISTS idx_quiz_first_key ON quiz_first_attempts(quiz_key);
    CREATE INDEX IF NOT EXISTS idx_quiz_first_student ON quiz_first_attempts(student_id);

    CREATE TABLE IF NOT EXISTS quiz_practice_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      student_id TEXT NOT NULL,
      quiz_key TEXT NOT NULL,
      day INTEGER NOT NULL,
      subject TEXT NOT NULL,
      topic TEXT NOT NULL,
      correct INTEGER NOT NULL,
      total INTEGER NOT NULL,
      accuracy INTEGER NOT NULL,
      score_marks REAL NOT NULL DEFAULT 0,
      time_seconds INTEGER NOT NULL,
      created_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_practice_student ON quiz_practice_attempts(student_id);

    CREATE TABLE IF NOT EXISTS task_completions (
      student_id TEXT NOT NULL,
      task_id TEXT NOT NULL,
      day INTEGER NOT NULL,
      completed_at TEXT NOT NULL,
      PRIMARY KEY (student_id, task_id)
    );
  `);
}

export function getDb(): Database.Database {
  if (db) return db;
  if (!existsSync(DB_DIR)) {
    mkdirSync(DB_DIR, { recursive: true });
  }
  db = new Database(DB_PATH);
  db.pragma("journal_mode = WAL");
  migrate(db);
  ensureScoreMarksColumn(db);
  return db;
}

function ensureScoreMarksColumn(database: Database.Database) {
  const addCol = (table: string) => {
    try {
      database.exec(
        `ALTER TABLE ${table} ADD COLUMN score_marks REAL NOT NULL DEFAULT 0`
      );
    } catch {
      // column already exists
    }
  };
  addCol("quiz_first_attempts");
  addCol("quiz_practice_attempts");
}

export function buildQuizKey(
  day: number,
  subject: string,
  topic: string
): string {
  return `${day}:${subject}:${topic}`;
}
