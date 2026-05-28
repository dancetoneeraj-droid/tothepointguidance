const DRAFT_PREFIX = "tothepoint:quiz-draft:";
const DRAFT_VERSION = 1;
const ACTIVE_PAUSE_KEY = "tothepoint:active-paused-quiz";

export interface QuizSessionDraft {
  version: typeof DRAFT_VERSION;
  sessionId: string;
  questionIds: string[];
  currentIndex: number;
  answers: Record<string, string>;
  marked: number[];
  visited: number[];
  secondsLeft: number;
  isPaused: boolean;
}

export interface PausedQuizMeta {
  sessionId: string;
  title: string;
  subjectLabel: string;
  resumePath: string;
  pausedAt: string;
}

function draftKey(sessionId: string): string {
  return `${DRAFT_PREFIX}${sessionId}`;
}

function sameQuestionSet(a: string[], b: string[]): boolean {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

export function loadQuizDraft(
  sessionId: string,
  questionIds: string[]
): QuizSessionDraft | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(draftKey(sessionId));
    if (!raw) return null;
    const parsed = JSON.parse(raw) as QuizSessionDraft;
    if (parsed.version !== DRAFT_VERSION) return null;
    if (parsed.sessionId !== sessionId) return null;
    if (!sameQuestionSet(parsed.questionIds, questionIds)) return null;
    if (!Number.isFinite(parsed.secondsLeft) || parsed.secondsLeft < 0) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function saveQuizDraft(draft: QuizSessionDraft): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(draftKey(draft.sessionId), JSON.stringify(draft));
  } catch {
    // quota / private mode — ignore
  }
}

export function clearQuizDraft(sessionId: string): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(draftKey(sessionId));
  } catch {
    // ignore
  }
}

export function setActivePausedQuiz(meta: PausedQuizMeta): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(ACTIVE_PAUSE_KEY, JSON.stringify(meta));
  } catch {
    // ignore
  }
}

export function getActivePausedQuiz(): PausedQuizMeta | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(ACTIVE_PAUSE_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as PausedQuizMeta;
  } catch {
    return null;
  }
}

export function clearActivePausedQuiz(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(ACTIVE_PAUSE_KEY);
  } catch {
    // ignore
  }
}

export function clearPausedQuizSession(sessionId: string): void {
  clearQuizDraft(sessionId);
  const active = getActivePausedQuiz();
  if (active?.sessionId === sessionId) {
    clearActivePausedQuiz();
  }
}

/** Call before navigating back to a paused quiz from the dashboard. */
export function unpauseQuizDraft(sessionId: string): void {
  if (typeof window === "undefined") return;
  try {
    const raw = localStorage.getItem(draftKey(sessionId));
    if (!raw) return;
    const parsed = JSON.parse(raw) as QuizSessionDraft;
    saveQuizDraft({ ...parsed, isPaused: false });
  } catch {
    // ignore
  }
}
