export type PaletteStatus =
  | "current"
  | "answered"
  | "marked"
  | "answered-marked"
  | "unanswered";

export interface QuizSessionMeta {
  sessionId: string;
  subjectLabel: string;
}
