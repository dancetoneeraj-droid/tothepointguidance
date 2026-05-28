import { getDb, buildQuizKey } from "@/lib/db/init";

export interface QuizAttemptInput {
  studentId: string;
  displayName: string;
  email?: string;
  day: number;
  subject: string;
  topic: string;
  correct: number;
  total: number;
  accuracy: number;
  scoreMarks: number;
  timeSeconds: number;
  isRetry: boolean;
}

export interface QuizRankingResult {
  rank: number | null;
  totalParticipants: number;
  percentile: number | null;
  countsForLeaderboard: boolean;
  isFirstAttempt: boolean;
  score: number;
  accuracy: number;
  timeSeconds: number;
}

function upsertStudent(
  studentId: string,
  displayName: string,
  email?: string
) {
  const database = getDb();
  const now = new Date().toISOString();
  database
    .prepare(
      `INSERT INTO students (id, display_name, email, updated_at)
       VALUES (?, ?, ?, ?)
       ON CONFLICT(id) DO UPDATE SET
         display_name = excluded.display_name,
         email = COALESCE(excluded.email, students.email),
         updated_at = excluded.updated_at`
    )
    .run(studentId, displayName, email ?? null, now);
}

function computeRank(
  quizKey: string,
  scoreMarks: number,
  timeSeconds: number
): { rank: number; total: number } {
  const database = getDb();
  const total = (
    database
      .prepare(
        `SELECT COUNT(*) as c FROM quiz_first_attempts WHERE quiz_key = ?`
      )
      .get(quizKey) as { c: number }
  ).c;

  const better = (
    database
      .prepare(
        `SELECT COUNT(*) as c FROM quiz_first_attempts
         WHERE quiz_key = ?
         AND (
           score_marks > ?
           OR (score_marks = ? AND time_seconds < ?)
         )`
      )
      .get(quizKey, scoreMarks, scoreMarks, timeSeconds) as { c: number }
  ).c;

  return { rank: better + 1, total };
}

export function submitQuizAttempt(
  input: QuizAttemptInput
): QuizRankingResult {
  const database = getDb();
  const quizKey = buildQuizKey(input.day, input.subject, input.topic);
  const now = new Date().toISOString();

  upsertStudent(input.studentId, input.displayName, input.email);

  const existing = database
    .prepare(
      `SELECT * FROM quiz_first_attempts WHERE student_id = ? AND quiz_key = ?`
    )
    .get(input.studentId, quizKey) as
    | {
        correct: number;
        total: number;
        accuracy: number;
        score_marks: number;
        time_seconds: number;
      }
    | undefined;

  if (input.isRetry || existing) {
    database
      .prepare(
        `INSERT INTO quiz_practice_attempts
         (student_id, quiz_key, day, subject, topic, correct, total, accuracy, score_marks, time_seconds, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        input.studentId,
        quizKey,
        input.day,
        input.subject,
        input.topic,
        input.correct,
        input.total,
        input.accuracy,
        input.scoreMarks,
        input.timeSeconds,
        now
      );

    if (existing) {
      const { rank, total } = computeRank(
        quizKey,
        existing.score_marks,
        existing.time_seconds
      );
      const percentile =
        total > 1
          ? Math.round(((total - rank) / (total - 1)) * 100)
          : 100;

      return {
        rank,
        totalParticipants: total,
        percentile,
        countsForLeaderboard: false,
        isFirstAttempt: false,
        score: input.scoreMarks,
        accuracy: input.accuracy,
        timeSeconds: input.timeSeconds,
      };
    }

    return {
      rank: null,
      totalParticipants: 0,
      percentile: null,
      countsForLeaderboard: false,
      isFirstAttempt: false,
      score: input.scoreMarks,
      accuracy: input.accuracy,
      timeSeconds: input.timeSeconds,
    };
  }

  database
    .prepare(
      `INSERT INTO quiz_first_attempts
       (student_id, quiz_key, day, subject, topic, correct, total, accuracy, score_marks, time_seconds, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .run(
      input.studentId,
      quizKey,
      input.day,
      input.subject,
      input.topic,
      input.correct,
      input.total,
      input.accuracy,
      input.scoreMarks,
      input.timeSeconds,
      now
    );

  const { rank, total } = computeRank(
    quizKey,
    input.scoreMarks,
    input.timeSeconds
  );
  const percentile =
    total > 1 ? Math.round(((total - rank) / (total - 1)) * 100) : 100;

  database
    .prepare(
      `UPDATE students SET
        quizzes_attempted = quizzes_attempted + 1,
        avg_accuracy = (
          SELECT ROUND(AVG(accuracy)) FROM quiz_first_attempts WHERE student_id = ?
        ),
        best_rank = CASE
          WHEN best_rank IS NULL THEN ?
          WHEN ? < best_rank THEN ?
          ELSE best_rank
        END,
        updated_at = ?
      WHERE id = ?`
    )
    .run(
      input.studentId,
      rank,
      rank,
      rank,
      now,
      input.studentId
    );

  return {
    rank,
    totalParticipants: total,
    percentile,
    countsForLeaderboard: true,
    isFirstAttempt: true,
    score: input.scoreMarks,
    accuracy: input.accuracy,
    timeSeconds: input.timeSeconds,
  };
}
