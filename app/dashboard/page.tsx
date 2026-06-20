"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  Crown,
  Lock,
  MessageCircle,
  Sparkles,
} from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { Modal } from "@/components/ui/Modal";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import {
  FREE_ACCESS_DAYS,
  canAccessDay,
  isPremiumOnlyDay,
  PREMIUM_SUPPORT_NUMBER,
  PREMIUM_UNLOCK_FEE,
  PREMIUM_WHATSAPP_URL,
} from "@/lib/premium-access";
import { isDayPublished, MAX_PUBLISHED_DAY } from "@/lib/daily-plans";
import { syncStudentToServer } from "@/lib/api/ecosystem";
import {
  getCompletedTaskIds,
  getDayWiseProgress,
} from "@/lib/tasks/progress-sync";

const TOTAL_DAYS = 75;

type DashboardDayCard = {
  day: number;
  accessLabel: string;
  statusLabel: string;
  interactive: boolean;
  href: string;
  tone: "free" | "current" | "premium" | "locked" | "coming-soon";
  completionPct: number;
};

export default function DashboardPage() {
  const { progress, user, isPremium, studentId } = useAuth();
  const [selectedLockedDay, setSelectedLockedDay] = useState<number | null>(null);

  // Sync to leaderboard server whenever dashboard loads
  useEffect(() => {
    if (!studentId || !progress) return;
    const completedTaskIds = getCompletedTaskIds(studentId);
    void syncStudentToServer({
      studentId,
      displayName: progress.displayName,
      email: user?.email ?? progress.email ?? undefined,
      currentDay: progress.currentDay,
      tasksCompleted: completedTaskIds.length,
      streak: progress.streak,
      completedTaskIds,
    });
  }, [studentId, progress, user?.email]);

  // Per-day completion percentages
  const dayProgressMap = useMemo<Record<number, number>>(() => {
    if (!studentId) return {};
    const rows = getDayWiseProgress(studentId, user?.email ?? progress?.email);
    return Object.fromEntries(rows.map((r) => [r.day, r.percent]));
  }, [studentId, user?.email, progress?.email]);

  const dayCards = useMemo<DashboardDayCard[]>(() => {
    if (!progress) return [];

    const userEmail = user?.email ?? progress.email;

    return Array.from({ length: TOTAL_DAYS }, (_, index) => {
      const day = index + 1;
      const published = day <= MAX_PUBLISHED_DAY && isDayPublished(day);
      const premiumDay = isPremiumOnlyDay(day);
      const premiumAccess = canAccessDay(day, userEmail);
      const freeDay = day <= FREE_ACCESS_DAYS;
      // Premium users bypass sequential unlock — all published days are accessible.
      const unlocked = published && premiumAccess && (isPremium || day <= progress.unlockedDay);
      const nextUp = published && premiumAccess && !isPremium && day === progress.unlockedDay + 1;
      const current = day === progress.currentDay && (unlocked || nextUp);
      const completionPct = dayProgressMap[day] ?? 0;

      if (!published) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Coming soon",
          interactive: false,
          href: "#",
          tone: "coming-soon" as const,
          completionPct: 0,
        };
      }

      if (freeDay) {
        return {
          day,
          accessLabel: "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: (current ? "current" : "free") as DashboardDayCard["tone"],
          completionPct,
        };
      }

      if (!premiumAccess) {
        return {
          day,
          accessLabel: "Premium access",
          statusLabel: "Locked",
          interactive: false,
          href: "#",
          tone: "premium" as const,
          completionPct: 0,
        };
      }

      if (current) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: "current" as const,
          completionPct,
        };
      }

      if (unlocked) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: (premiumDay ? "locked" : "free") as DashboardDayCard["tone"],
          completionPct,
        };
      }

      if (nextUp) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: (premiumDay ? "locked" : "free") as DashboardDayCard["tone"],
          completionPct,
        };
      }

      return {
        day,
        accessLabel: premiumDay ? "Premium access" : "Free access",
        statusLabel: "Locked",
        interactive: false,
        href: "#",
        tone: "locked" as const,
        completionPct: 0,
      };
    });
  }, [progress, user?.email, dayProgressMap]);

  if (!progress) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-violet-500 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-in">
      <header className="space-y-4">
        <div className="inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs text-violet-200">
          <Sparkles className="h-3.5 w-3.5" />
          Disciplined execution dashboard
        </div>
        <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
              Day Selection Dashboard
        </h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-400">
              Pick your day and move straight into execution. No extra analytics,
              no clutter, only the roadmap.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-2 text-sm text-zinc-300">
              {FREE_ACCESS_DAYS} days free access
            </span>
            <span className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-2 text-sm text-zinc-300">
              75-day execution roadmap
            </span>
            <span
              className={`rounded-full border px-3 py-2 text-sm ${
                isPremium
                  ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300"
                  : "border-amber-500/20 bg-amber-500/10 text-amber-300"
              }`}
            >
              {isPremium ? "Premium unlocked" : "Day 4 onwards premium"}
            </span>
          </div>
        </div>
      </header>

      <Modal
        open={selectedLockedDay != null}
        onClose={() => setSelectedLockedDay(null)}
        title={`Day ${selectedLockedDay ?? 4} — Premium Locked`}
        footer={
          <>
            <Button
              variant="secondary"
              className="flex-1"
              onClick={() => setSelectedLockedDay(null)}
            >
              Maybe Later
            </Button>
            <Button
              className="flex-1 gap-2"
              onClick={() =>
                window.open(PREMIUM_WHATSAPP_URL, "_blank", "noopener,noreferrer")
              }
            >
              <MessageCircle className="h-4 w-4" />
              Contact on WhatsApp
            </Button>
          </>
        }
      >
        <div className="space-y-3">
          <p>
            Day {selectedLockedDay ?? 4} and all features after the first{" "}
            {FREE_ACCESS_DAYS} days are part of the premium access plan.
          </p>
          <div className="rounded-2xl border border-amber-500/20 bg-amber-500/10 px-4 py-4">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-amber-300">
              Unlock Details
            </p>
            <p className="mt-2 text-lg font-semibold text-white">
              Fee: Rs. {PREMIUM_UNLOCK_FEE}
            </p>
            <p className="mt-1 text-sm text-amber-100/80">
              Contact {PREMIUM_SUPPORT_NUMBER} to unlock all features.
            </p>
          </div>
                </div>
      </Modal>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {dayCards.map((card) => (
          <DayAccessCard
            key={card.day}
            card={card}
            onPremiumLockedClick={() => setSelectedLockedDay(card.day)}
              />
            ))}
      </section>
    </div>
  );
}

function DayAccessCard({
  card,
  onPremiumLockedClick,
}: {
  card: DashboardDayCard;
  onPremiumLockedClick: () => void;
}) {
  const styles = {
    free: "border-emerald-400/20 shadow-[0_0_28px_rgba(16,185,129,0.08)] hover:border-emerald-300/35",
    current: "border-violet-400/25 shadow-[0_0_34px_rgba(124,58,237,0.12)] hover:border-violet-300/40",
    premium: "border-amber-500/20 opacity-90",
    locked: "border-white/10 hover:border-white/15",
    "coming-soon": "border-dashed border-white/10 opacity-70",
  };

  const fillColor = {
    free: "bg-emerald-500/25",
    current: "bg-violet-500/25",
    premium: "bg-amber-500/15",
    locked: "bg-white/[0.05]",
    "coming-soon": "bg-white/[0.03]",
  };

  const iconTone = {
    free: "border-emerald-400/20 bg-emerald-500/10 text-emerald-300",
    current: "border-violet-400/20 bg-violet-500/10 text-violet-300",
    premium: "border-amber-500/20 bg-amber-500/10 text-amber-300",
    locked: "border-white/10 bg-white/[0.03] text-zinc-400",
    "coming-soon": "border-white/10 bg-white/[0.03] text-zinc-500",
  };

  const badgeTone = {
    free: "border-emerald-400/20 bg-emerald-500/10 text-emerald-200",
    current: "border-violet-400/20 bg-violet-500/10 text-violet-200",
    premium: "border-amber-500/20 bg-amber-500/10 text-amber-200",
    locked: "border-white/10 bg-white/[0.03] text-zinc-300",
    "coming-soon": "border-white/10 bg-white/[0.03] text-zinc-500",
  };

  const pct = card.completionPct;
  const showFill = card.interactive && pct > 0;

  const content = (
    <Card
      className={`group relative h-full overflow-hidden rounded-[1.75rem] p-5 transition duration-300 bg-[#0d0d12] ${
        styles[card.tone]
      } ${card.interactive ? "hover:-translate-y-1" : ""}`}
    >
      {/* Bottle fill — rises from bottom based on completion % */}
      {showFill && (
        <div
          className={`pointer-events-none absolute inset-x-0 bottom-0 transition-all duration-700 ${fillColor[card.tone]}`}
          style={{ height: `${pct}%` }}
        />
      )}

      {/* Completion % ring/label */}
      {showFill && (
        <div className="absolute right-3 top-3 flex h-8 w-8 items-center justify-center rounded-full border border-white/10 bg-black/40 text-[10px] font-bold tabular-nums text-white/70">
          {pct}%
        </div>
      )}

      <div className="relative flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-zinc-500">
            Day
          </p>
          <p className="mt-2 text-4xl font-semibold tracking-tight text-white">
            {card.day}
          </p>
        </div>
        {!showFill && (
          <div
            className={`flex h-11 w-11 items-center justify-center rounded-2xl border ${iconTone[card.tone]}`}
          >
            {card.tone === "premium" || card.tone === "locked" ? (
              <Lock className="h-4 w-4" />
            ) : card.tone === "coming-soon" ? (
              <Crown className="h-4 w-4" />
            ) : (
              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-0.5" />
            )}
          </div>
        )}
      </div>

      <div className="relative mt-8 space-y-3">
        <p className="text-sm text-zinc-300">{card.accessLabel}</p>
        <div className="flex items-center justify-between gap-3">
          <span
            className={`rounded-full border px-2.5 py-1 text-xs font-medium ${badgeTone[card.tone]}`}
          >
            {pct === 100 ? "✓ Done" : card.statusLabel}
          </span>
          <span className="text-xs uppercase tracking-[0.2em] text-zinc-500">
            {card.interactive ? "Open" : "Locked"}
          </span>
        </div>
        {/* Thin progress bar at bottom */}
        {showFill && (
          <div className="h-1 w-full overflow-hidden rounded-full bg-white/[0.06]">
            <div
              className={`h-full rounded-full transition-all duration-700 ${
                pct === 100
                  ? "bg-emerald-400"
                  : card.tone === "current"
                    ? "bg-violet-400"
                    : "bg-emerald-500/70"
              }`}
              style={{ width: `${pct}%` }}
            />
          </div>
        )}
      </div>
    </Card>
  );

  if (!card.interactive) {
    if (card.tone === "premium") {
      return (
        <button type="button" className="w-full text-left" onClick={onPremiumLockedClick}>
          {content}
        </button>
      );
    }
    return content;
  }

  return <Link href={card.href}>{content}</Link>;
}
