"use client";

import { useState } from "react";
import { GraduationCap, Lightbulb, PlayCircle } from "lucide-react";
import type { Question } from "@/types";
import { getYouTubeEmbedUrl } from "@/lib/youtube";

type SolutionTab = "text" | "video";

interface QuestionSolutionPanelProps {
  question: Question;
}

export function QuestionSolutionPanel({ question }: QuestionSolutionPanelProps) {
  const hasText = Boolean(question.explanation || question.solution);
  const embedUrl = question.videoUrl ? getYouTubeEmbedUrl(question.videoUrl) : null;
  const hasVideo = Boolean(embedUrl);

  const [tab, setTab] = useState<SolutionTab>("text");
  const [videoLoaded, setVideoLoaded] = useState(false);

  if (!hasText && !hasVideo) {
    return (
      <div className="border-t border-white/10 px-5 py-5 sm:px-6">
        <div className="flex items-center gap-2 text-emerald-300">
          <GraduationCap className="h-4 w-4" />
          <p className="text-sm font-semibold uppercase tracking-[0.18em]">
            Explanation / Solution
          </p>
        </div>
        <div className="mt-3 rounded-2xl border border-white/10 bg-black/20 p-4 sm:p-5">
          <div className="flex items-start gap-3 text-sm text-zinc-400">
            <Lightbulb className="mt-0.5 h-4 w-4 text-amber-300" />
            <p>
              Detailed explanation has not been added for this question yet. The
              correct answer for coaching review is{" "}
              <span className="font-medium text-violet-200">
                {question.correctAnswer}
              </span>
              .
            </p>
          </div>
        </div>
      </div>
    );
  }

  const showVideoPlayer = hasVideo && tab === "video" && videoLoaded;

  return (
    <div className="border-t border-white/10 px-5 py-5 sm:px-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2 text-emerald-300">
          <GraduationCap className="h-4 w-4" />
          <p className="text-sm font-semibold uppercase tracking-[0.18em]">
            Explanation / Solution
          </p>
        </div>
        {hasVideo && hasText ? (
          <div className="inline-flex rounded-xl border border-white/10 bg-black/20 p-1">
            <button
              type="button"
              onClick={() => setTab("text")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                tab === "text"
                  ? "bg-violet-600 text-white"
                  : "text-zinc-400 hover:text-white"
              }`}
            >
              Written
            </button>
            <button
              type="button"
              onClick={() => {
                setTab("video");
                setVideoLoaded(true);
              }}
              className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                tab === "video"
                  ? "bg-violet-600 text-white"
                  : "text-zinc-400 hover:text-white"
              }`}
            >
              <PlayCircle className="h-3.5 w-3.5" />
              Video
            </button>
          </div>
        ) : null}
      </div>

      <div className="mt-3 rounded-2xl border border-white/10 bg-black/20 p-4 sm:p-5">
        {hasVideo && !hasText ? (
          <>
            {!videoLoaded ? (
              <button
                type="button"
                onClick={() => setVideoLoaded(true)}
                className="inline-flex items-center gap-2 rounded-xl border border-violet-500/30 bg-violet-500/10 px-4 py-3 text-sm font-medium text-violet-200 transition-colors hover:bg-violet-500/20"
              >
                <PlayCircle className="h-5 w-5" />
                Watch video solution
              </button>
            ) : (
              <YouTubeEmbed embedUrl={embedUrl!} title={question.id} />
            )}
          </>
        ) : tab === "video" && hasVideo ? (
          showVideoPlayer ? (
            <YouTubeEmbed embedUrl={embedUrl!} title={question.id} />
          ) : (
            <button
              type="button"
              onClick={() => setVideoLoaded(true)}
              className="inline-flex items-center gap-2 rounded-xl border border-violet-500/30 bg-violet-500/10 px-4 py-3 text-sm font-medium text-violet-200 transition-colors hover:bg-violet-500/20"
            >
              <PlayCircle className="h-5 w-5" />
              Watch video solution
            </button>
          )
        ) : (
          <>
            {hasText ? (
              <p className="text-sm leading-7 text-zinc-200 whitespace-pre-wrap">
                {question.explanation ?? question.solution}
              </p>
            ) : null}
            {question.explanationHi ? (
              <p
                className="mt-4 border-t border-white/10 pt-4 text-sm leading-7 text-amber-50/90 whitespace-pre-wrap"
                lang="hi"
              >
                {question.explanationHi}
              </p>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}

function YouTubeEmbed({
  embedUrl,
  title,
}: {
  embedUrl: string;
  title: string;
}) {
  return (
    <div className="overflow-hidden rounded-xl border border-white/10 bg-black/40">
      <div className="relative aspect-video w-full">
        <iframe
          src={embedUrl}
          title={`Video solution for ${title}`}
          className="absolute inset-0 h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
          loading="lazy"
          referrerPolicy="strict-origin-when-cross-origin"
        />
      </div>
    </div>
  );
}
