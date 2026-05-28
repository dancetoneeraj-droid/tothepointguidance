"use client";

import { BookOpen, CheckCircle2, ExternalLink, FileText } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface EnglishSectionCardProps {
  title: string;
  pdfUrl?: string;
  extraUrl?: string;
  extraLabel?: string;
  completed: boolean;
  onMarkComplete: () => void;
  loading?: boolean;
}

export function EnglishSectionCard({
  title,
  pdfUrl,
  extraUrl,
  extraLabel,
  completed,
  onMarkComplete,
  loading,
}: EnglishSectionCardProps) {
  return (
    <Card className="p-4">
      <div className="flex items-start justify-between gap-3">
        <section>
          <h3 className="font-medium text-foreground flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-violet-400" />
            {title}
          </h3>
          <div className="mt-2 flex flex-wrap gap-2">
            {pdfUrl ? (
              <a
                href={pdfUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-muted hover:text-violet-400 transition-colors"
              >
                <FileText className="h-3.5 w-3.5" />
                PDF Notes
                <ExternalLink className="h-3 w-3" />
              </a>
            ) : null}
            {extraUrl ? (
              <a
                href={extraUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-muted hover:text-violet-400 transition-colors"
              >
                {extraLabel ?? "Resource"}
                <ExternalLink className="h-3 w-3" />
              </a>
            ) : null}
          </div>
        </section>
        {completed ? (
          <span className="flex items-center gap-1 text-xs text-emerald-400 shrink-0">
            <CheckCircle2 className="h-4 w-4" />
            Done
          </span>
        ) : null}
      </div>
      {!completed ? (
        <Button
          variant="secondary"
          size="sm"
          className="mt-4 w-full sm:w-auto"
          onClick={onMarkComplete}
          loading={loading}
        >
          Mark as Completed
        </Button>
      ) : null}
    </Card>
  );
}
