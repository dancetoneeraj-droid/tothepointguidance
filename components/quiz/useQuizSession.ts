"use client";



import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { computeQuizMarks } from "@/lib/quiz/scoring";
import type { Question, QuizRanking, QuizResult } from "@/types";

import type { SubmitSummary } from "./QuizSubmitModal";

import type { PaletteStatus } from "./types";

import {

  clearActivePausedQuiz,
  clearQuizDraft,
  loadQuizDraft,
  saveQuizDraft,

} from "@/lib/quiz/session-persistence";



function clampIndex(index: number, total: number): number {

  if (total <= 0) return 0;

  return Math.min(Math.max(0, index), total - 1);

}



export function useQuizSession(

  questions: Question[],

  durationMinutes: number,

  sessionId: string,

  onComplete: (
    result: QuizResult,
    answers: Record<string, string>
  ) => Promise<QuizRanking | null | void>
) {

  const total = questions.length;

  const questionIds = useMemo(

    () => questions.map((q) => q.id),

    [questions]

  );

  const startTimeRef = useRef(Date.now());

  const submittingRef = useRef(false);



  const [currentIndex, setCurrentIndex] = useState(0);

  const [answers, setAnswers] = useState<Record<string, string>>({});

  const [marked, setMarked] = useState<Set<number>>(new Set());

  const [visited, setVisited] = useState<Set<number>>(new Set());

  const [secondsLeft, setSecondsLeft] = useState(durationMinutes * 60);

  const [isPaused, setIsPaused] = useState(false);

  const [timeExpired, setTimeExpired] = useState(false);

  const [showSubmitModal, setShowSubmitModal] = useState(false);

  const [showPauseConfirm, setShowPauseConfirm] = useState(false);

  const [finished, setFinished] = useState(false);

  const [submitting, setSubmitting] = useState(false);

  const [result, setResult] = useState<QuizResult | null>(null);

  const [ranking, setRanking] = useState<QuizRanking | null>(null);

  const [ready, setReady] = useState(false);



  const interactionsDisabled = isPaused || submitting;



  const hydrateSession = useCallback(() => {

    const draft = loadQuizDraft(sessionId, questionIds);

    const fullDuration = durationMinutes * 60;



    if (draft) {

      setCurrentIndex(clampIndex(draft.currentIndex, total));

      setAnswers(draft.answers);

      setMarked(new Set(draft.marked));

      setVisited(

        new Set(draft.visited.length > 0 ? draft.visited : [draft.currentIndex])

      );

      setSecondsLeft(Math.min(draft.secondsLeft, fullDuration));

      setIsPaused(draft.isPaused);

      const elapsed = fullDuration - Math.min(draft.secondsLeft, fullDuration);

      startTimeRef.current = Date.now() - elapsed * 1000;

      const expired = draft.secondsLeft <= 0;
      setTimeExpired(expired);
      if (expired) setShowSubmitModal(true);

    } else {

      setCurrentIndex(0);

      setAnswers({});

      setMarked(new Set());

      setVisited(new Set([0]));

      setSecondsLeft(fullDuration);

      setIsPaused(false);

      setTimeExpired(false);

      setShowSubmitModal(false);

      startTimeRef.current = Date.now();

    }



    setShowPauseConfirm(false);

    setFinished(false);

    setSubmitting(false);

    setResult(null);

    setRanking(null);

    submittingRef.current = false;

    setReady(true);

  }, [sessionId, questionIds, durationMinutes, total]);



  useEffect(() => {

    if (finished) return;

    setReady(false);

    hydrateSession();

  }, [sessionId, hydrateSession, finished]);



  const safeIndex = useMemo(

    () => clampIndex(currentIndex, total),

    [currentIndex, total]

  );



  useEffect(() => {

    if (safeIndex !== currentIndex && total > 0) {

      setCurrentIndex(safeIndex);

    }

  }, [safeIndex, currentIndex, total]);



  useEffect(() => {

    if (!ready || finished || total === 0) return;

    setVisited((prev) => {

      if (prev.has(safeIndex)) return prev;

      const next = new Set(prev);

      next.add(safeIndex);

      return next;

    });

  }, [safeIndex, ready, finished, total]);



  const current = total > 0 ? questions[safeIndex] : undefined;



  const submitQuiz = useCallback(async () => {

    if (submittingRef.current || finished || total === 0) return;

    submittingRef.current = true;

    setSubmitting(true);

    setShowSubmitModal(false);

    setShowPauseConfirm(false);

    setIsPaused(false);



    const marks = computeQuizMarks(questions, answers);

    const quizResult: QuizResult = {
      correct: marks.correct,
      wrong: marks.wrong,
      unanswered: marks.unanswered,
      total: marks.total,
      score: marks.score,
      maxScore: marks.maxScore,
      accuracy: marks.accuracy,
      timeTakenSeconds: Math.floor((Date.now() - startTimeRef.current) / 1000),
    };



    setResult(quizResult);

    setFinished(true);

    clearQuizDraft(sessionId);
    clearActivePausedQuiz();

    const rankingResult = await onComplete(quizResult, answers);

    setRanking(rankingResult ?? null);

    setSubmitting(false);

    submittingRef.current = false;

  }, [answers, questions, total, finished, onComplete, sessionId]);



  const requestSubmit = useCallback(() => {

    if (submittingRef.current || finished || total === 0) return;

    setShowPauseConfirm(false);

    setShowSubmitModal(true);

  }, [finished, total]);



  const dismissSubmitModal = useCallback(() => {

    if (submitting || timeExpired) return;

    setShowSubmitModal(false);

  }, [submitting, timeExpired]);



  const confirmSubmit = useCallback(() => {

    void submitQuiz();

  }, [submitQuiz]);



  const requestPause = useCallback(() => {

    if (finished || submitting || isPaused) return;

    setShowSubmitModal(false);

    setShowPauseConfirm(true);

  }, [finished, submitting, isPaused]);



  const dismissPauseConfirm = useCallback(() => {

    setShowPauseConfirm(false);

  }, []);



  const pauseAndSave = useCallback(() => {
    setShowPauseConfirm(false);
    setIsPaused(true);
    if (total === 0) return;
    saveQuizDraft({
      version: 1,
      sessionId,
      questionIds,
      currentIndex: safeIndex,
      answers,
      marked: [...marked],
      visited: [...visited],
      secondsLeft,
      isPaused: true,
    });
  }, [
    total,
    sessionId,
    questionIds,
    safeIndex,
    answers,
    marked,
    visited,
    secondsLeft,
  ]);



  useEffect(() => {

    if (!ready || finished || isPaused || showSubmitModal || total === 0) return;



    const interval = setInterval(() => {

      setSecondsLeft((s) => {

        if (s <= 1) {

          clearInterval(interval);

          setTimeExpired(true);

          setShowSubmitModal(true);

          return 0;

        }

        return s - 1;

      });

    }, 1000);



    return () => clearInterval(interval);

  }, [ready, finished, isPaused, showSubmitModal, total]);



  useEffect(() => {

    if (!ready || finished || total === 0) return;

    if (currentIndex >= total) {

      requestSubmit();

    }

  }, [currentIndex, total, finished, ready, requestSubmit]);



  useEffect(() => {

    if (!ready || finished || total === 0) return;



    saveQuizDraft({

      version: 1,

      sessionId,

      questionIds,

      currentIndex: safeIndex,

      answers,

      marked: [...marked],

      visited: [...visited],

      secondsLeft,

      isPaused,

    });

  }, [

    ready,

    finished,

    sessionId,

    questionIds,

    safeIndex,

    answers,

    marked,

    visited,

    secondsLeft,

    isPaused,

    total,

  ]);



  const getPaletteStatus = useCallback(

    (index: number): PaletteStatus => {

      const q = questions[index];

      if (!q) return "unanswered";

      const isAnswered = Boolean(answers[q.id]);

      const isMarked = marked.has(index);

      if (index === safeIndex) return "current";

      if (isAnswered && isMarked) return "answered-marked";

      if (isAnswered) return "answered";

      if (isMarked) return "marked";

      return "unanswered";

    },

    [questions, answers, marked, safeIndex]

  );



  const stats = useMemo(() => {

    let answered = 0;

    let markedCount = 0;

    questions.forEach((q, i) => {

      if (answers[q.id]) answered++;

      if (marked.has(i)) markedCount++;

    });

    return {

      answered,

      unanswered: total - answered,

      marked: markedCount,

    };

  }, [questions, answers, marked, total]);



  const submitSummary: SubmitSummary = useMemo(() => {

    const visitedCount = visited.size;

    return {

      total,

      answered: stats.answered,

      notAnswered: stats.unanswered,

      visited: visitedCount,

      notVisited: Math.max(0, total - visitedCount),

    };

  }, [total, stats.answered, stats.unanswered, visited]);



  const selectAnswer = useCallback(

    (option: string) => {

      if (interactionsDisabled || finished) return;

      const q = questions[safeIndex];

      if (!q) return;

      setAnswers((prev) => {
        if (prev[q.id] === option) {
          const next = { ...prev };
          delete next[q.id];
          return next;
        }
        return { ...prev, [q.id]: option };
      });

    },

    [questions, safeIndex, interactionsDisabled, finished]

  );



  const toggleMark = useCallback(() => {

    if (interactionsDisabled || finished) return;

    setMarked((prev) => {

      const next = new Set(prev);

      if (next.has(safeIndex)) next.delete(safeIndex);

      else next.add(safeIndex);

      return next;

    });

  }, [safeIndex, interactionsDisabled, finished]);



  const goTo = useCallback(

    (index: number) => {

      if (interactionsDisabled || finished) return;

      setCurrentIndex(clampIndex(index, total));

    },

    [total, interactionsDisabled, finished]

  );



  const goNext = useCallback(() => {

    if (interactionsDisabled || finished) return;

    if (safeIndex >= total - 1) {

      requestSubmit();

      return;

    }

    setCurrentIndex((i) => clampIndex(i + 1, total));

  }, [safeIndex, total, requestSubmit, interactionsDisabled, finished]);



  const goPrev = useCallback(() => {

    if (interactionsDisabled || finished) return;

    setCurrentIndex((i) => clampIndex(i - 1, total));

  }, [total, interactionsDisabled, finished]);



  const saveAndNext = useCallback(() => {

    goNext();

  }, [goNext]);



  const progressPercent = total > 0 ? Math.round((stats.answered / total) * 100) : 0;



  return {

    ready,

    total,

    safeIndex,

    current,

    answers,

    marked,

    secondsLeft,

    isPaused,

    timeExpired,

    finished,

    submitting,

    result,

    ranking,

    stats,

    progressPercent,

    submitSummary,

    showSubmitModal,

    showPauseConfirm,

    interactionsDisabled,

    getPaletteStatus,

    selectAnswer,

    toggleMark,

    goTo,

    goNext,

    goPrev,

    saveAndNext,

    requestSubmit,

    confirmSubmit,

    dismissSubmitModal,

    requestPause,

    pauseAndSave,

    dismissPauseConfirm,

  };

}


