"use client";

import Link from "next/link";
import { FileText, Brain, CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { QuizTopicCard } from "./QuizTopicCard";
import type { GkConfig } from "@/types";

interface GkSectionProps {
  day: number;
  config: GkConfig;
  materialsCompleted: boolean;
  revisionCompleted: boolean;
  onMarkMaterials: () => void;
  materialsLoading?: boolean;
}

export function GkSection({
  day,
  config,
  materialsCompleted,
  revisionCompleted,
  onMarkMaterials,
  materialsLoading,
}: GkSectionProps) {
  return (
    <section className="space-y-4">
      <h2 className="text-sm font-semibold text-foreground uppercase tracking-wider flex items-center gap-2">
        <Brain className="h-4 w-4 text-violet-400" />
        General Knowledge
      </h2>

      <Card className="p-4 space-y-3">
        <h3 className="font-medium text-foreground">Today&apos;s Topics</h3>
        <div className="flex flex-wrap gap-3 text-xs">
          {config.todayTopicPdf ? (
            <a
              href={config.todayTopicPdf}
              className="flex items-center gap-1 text-muted hover:text-violet-400"
            >
              <FileText className="h-3.5 w-3.5" /> PDF
            </a>
          ) : null}
          {config.todayMindmap ? (
            <a
              href={config.todayMindmap}
              className="flex items-center gap-1 text-muted hover:text-violet-400"
            >
              Mindmap
            </a>
          ) : null}
          {config.todayNotes ? (
            <a
              href={config.todayNotes}
              className="flex items-center gap-1 text-muted hover:text-violet-400"
            >
              Notes
            </a>
          ) : null}
        </div>
        {materialsCompleted ? (
          <span className="flex items-center gap-1 text-xs text-emerald-400">
            <CheckCircle2 className="h-4 w-4" /> Materials reviewed
          </span>
        ) : (
          <Button
            variant="secondary"
            size="sm"
            onClick={onMarkMaterials}
            loading={materialsLoading}
          >
            Mark materials as completed
          </Button>
        )}
      </Card>

      {day > 1 && config.revisionQuiz ? (
        <QuizTopicCard
          topic={config.revisionTopic ?? "revision"}
          questionCount={20}
          durationMinutes={25}
          completed={revisionCompleted}
          href={`/quiz/gk/revision?day=${day}`}
          subjectLabel="GK Revision"
        />
      ) : null}
    </section>
  );
}
