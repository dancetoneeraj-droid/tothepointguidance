"use client";

import { useMemo, useState } from "react";
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

const TOTAL_DAYS = 75;

type DashboardDayCard = {
  day: number;
  accessLabel: string;
  statusLabel: string;
  interactive: boolean;
  href: string;
  tone: "free" | "current" | "premium" | "locked" | "coming-soon";
};

export default function DashboardPage() {
  const { progress, user, isPremium } = useAuth();
  const [selectedLockedDay, setSelectedLockedDay] = useState<number | null>(null);

  const dayCards = useMemo<DashboardDayCard[]>(() => {
    if (!progress) return [];

    const userEmail = user?.email ?? progress.email;

    return Array.from({ length: TOTAL_DAYS }, (_, index) => {
      const day = index + 1;
      const published = day <= MAX_PUBLISHED_DAY && isDayPublished(day);
      const premiumDay = isPremiumOnlyDay(day);
      const premiumAccess = canAccessDay(day, userEmail);
      const freeDay = day <= FREE_ACCESS_DAYS;
      const unlocked = published && premiumAccess && day <= progress.unlockedDay;
      const nextUp = published && premiumAccess && day === progress.unlockedDay + 1;
      const current = day === progress.currentDay && (unlocked || nextUp);

      if (!published) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Coming soon",
          interactive: false,
          href: "#",
          tone: "coming-soon",
        };
      }

      if (freeDay) {
        return {
          day,
          accessLabel: "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: current ? "current" : "free",
        };
      }

      if (!premiumAccess) {
        return {
          day,
          accessLabel: "Premium access",
          statusLabel: "Locked",
          interactive: false,
          href: "#",
          tone: "premium",
        };
      }

      if (current) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: "current",
        };
      }

      if (unlocked) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: premiumDay ? "locked" : "free",
        };
      }

      if (nextUp) {
        return {
          day,
          accessLabel: premiumDay ? "Premium access" : "Free access",
          statusLabel: "Unlocked",
          interactive: true,
          href: `/day/${day}`,
          tone: premiumDay ? "locked" : "free",
        };
      }

      return {
        day,
        accessLabel: premiumDay ? "Premium access" : "Free access",
        statusLabel: "Locked",
        interactive: false,
        href: "#",
        tone: "locked",
      };
    });
  }, [progress, user?.email]);

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
    free: "border-emerald-400/20 bg-[linear-gradient(180deg,rgba(16,185,129,0.10),rgba(255,255,255,0.03))] shadow-[0_0_28px_rgba(16,185,129,0.08)] hover:border-emerald-300/35",
    current:
      "border-violet-400/25 bg-[linear-gradient(180deg,rgba(124,58,237,0.16),rgba(255,255,255,0.03))] shadow-[0_0_34px_rgba(124,58,237,0.12)] hover:border-violet-300/40",
    premium:
      "border-amber-500/20 bg-[linear-gradient(180deg,rgba(245,158,11,0.08),rgba(255,255,255,0.02))] opacity-90",
    locked:
      "border-white/10 bg-[linear-gradient(180deg,rgba(255,255,255,0.03),rgba(255,255,255,0.02))] hover:border-white/15",
    "coming-soon":
      "border-dashed border-white/10 bg-[linear-gradient(180deg,rgba(255,255,255,0.02),rgba(255,255,255,0.01))] opacity-70",
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

  const content = (
    <Card
      className={`group h-full rounded-[1.75rem] p-5 transition duration-300 ${
        styles[card.tone]
      } ${card.interactive ? "hover:-translate-y-1" : ""}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-zinc-500">
            Day
          </p>
          <p className="mt-2 text-4xl font-semibold tracking-tight text-white">
            {card.day}
          </p>
        </div>
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
      </div>

      <div className="mt-8 space-y-3">
        <p className="text-sm text-zinc-300">{card.accessLabel}</p>
        <div className="flex items-center justify-between gap-3">
          <span
            className={`rounded-full border px-2.5 py-1 text-xs font-medium ${badgeTone[card.tone]}`}
          >
            {card.statusLabel}
          </span>
          <span className="text-xs uppercase tracking-[0.2em] text-zinc-500">
            {card.interactive ? "Open" : "Locked"}
          </span>
        </div>
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
