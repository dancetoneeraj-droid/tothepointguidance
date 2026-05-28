"use client";

import Link from "next/link";
import { CheckCircle2, Clock, HelpCircle, Play } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { formatTopic } from "@/lib/day-system";

interface QuizTopicCardProps {
  topic: string;
  questionCount: number;
  durationMinutes: number;
  completed?: boolean;
  href: string;
  subjectLabel?: string;
}

export function QuizTopicCard({
  topic,
  questionCount,
  durationMinutes,
  completed,
  href,
  subjectLabel,
}: QuizTopicCardProps) {
  return (
    <Card className="p-4 flex flex-col sm:flex-row sm:items-center gap-4">
      <section className="flex-1 min-w-0">
        {subjectLabel ? (
          <p className="text-xs font-medium text-violet-400 uppercase tracking-wider mb-1">
            {subjectLabel}
          </p>
        ) : null}
        <h3 className="font-medium text-foreground">{formatTopic(topic)}</h3>
        <div className="mt-2 flex flex-wrap gap-3 text-xs text-muted">
          <span className="flex items-center gap-1">
            <HelpCircle className="h-3.5 w-3.5" />
            {questionCount} questions
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-3.5 w-3.5" />
            {durationMinutes} min
          </span>
          {completed ? (
            <span className="flex items-center gap-1 text-emerald-400">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Completed
            </span>
          ) : (
            <span className="text-amber-400/90">Pending</span>
          )}
        </div>
      </section>
      <Link href={href} className="shrink-0">
        <Button variant={completed ? "secondary" : "primary"} size="sm">
          <Play className="h-4 w-4" />
          {completed ? "View Result" : "Start"}
        </Button>
      </Link>
    </Card>
  );
}
