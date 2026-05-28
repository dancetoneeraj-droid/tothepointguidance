"use client";

import Link from "next/link";
import { Lock, MessageCircle } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import {
  PREMIUM_SUPPORT_NUMBER,
  PREMIUM_UNLOCK_FEE,
  PREMIUM_WHATSAPP_URL,
} from "@/lib/premium-access";

interface PremiumLockCardProps {
  day?: number;
  showBack?: boolean;
}

export function PremiumLockCard({ day, showBack = true }: PremiumLockCardProps) {
  return (
    <Card className="p-8 text-center max-w-lg mx-auto" glow>
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-amber-500/15">
        <Lock className="h-7 w-7 text-amber-400" />
      </div>
      <h1 className="text-xl font-semibold text-foreground">
        {day ? `Day ${day} — Premium Locked` : "Premium content locked"}
      </h1>
      <p className="mt-3 text-sm text-muted leading-relaxed">
        {day ? `Day ${day} is part of the premium plan.` : "Premium content locked."}
        <br />
        Contact us on WhatsApp to unlock all features.
      </p>
      <div className="mt-5 rounded-2xl border border-amber-500/20 bg-amber-500/10 px-4 py-4">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-amber-300">
          Unlock Premium Access
        </p>
        <p className="mt-2 text-lg font-semibold text-white">
          Fee: Rs. {PREMIUM_UNLOCK_FEE}
        </p>
        <p className="mt-1 text-sm text-amber-100/80">
          Contact {PREMIUM_SUPPORT_NUMBER} to unlock all features.
        </p>
      </div>
      <a
        href={PREMIUM_WHATSAPP_URL}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex mt-6"
      >
        <Button size="lg" className="gap-2">
          <MessageCircle className="h-4 w-4" />
          WhatsApp {PREMIUM_SUPPORT_NUMBER}
        </Button>
      </a>
      <p className="mt-4 text-xs text-muted">
        Already have premium access?{" "}
        <Link href="/login" className="text-violet-400 hover:text-violet-300">
          Log in
        </Link>
      </p>
      {showBack ? (
        <Link
          href="/dashboard"
          className="inline-block mt-4 text-sm text-violet-400 hover:text-violet-300"
        >
          ← Back to dashboard
        </Link>
      ) : null}
    </Card>
  );
}
