import { premiumUsers } from "@/lib/premiumUsers";

/** Days 1–3 are public (no login). Day 4+ requires whitelisted premium login. */
export const FREE_ACCESS_DAYS = 3;
export const PREMIUM_SUPPORT_NUMBER = "7976395900";
export const PREMIUM_UNLOCK_FEE = 500;
export const PREMIUM_WHATSAPP_URL = `https://wa.me/91${PREMIUM_SUPPORT_NUMBER}`;

const PREMIUM_SET = new Set(
  premiumUsers.map((e) => e.trim().toLowerCase()).filter(Boolean)
);

export function normalizeEmail(email: string | null | undefined): string {
  return (email ?? "").trim().toLowerCase();
}

export function isPremiumEmail(email: string | null | undefined): boolean {
  const normalized = normalizeEmail(email);
  if (!normalized) return false;
  return PREMIUM_SET.has(normalized);
}

/** Public days always allowed; premium days only for whitelisted logged-in email. */
export function canAccessDay(
  day: number,
  email: string | null | undefined
): boolean {
  if (day <= FREE_ACCESS_DAYS) return true;
  return isPremiumEmail(email);
}

export function isPremiumOnlyDay(day: number): boolean {
  return day > FREE_ACCESS_DAYS;
}

export function getMaxAccessibleDay(
  email: string | null | undefined,
  publishedMaxDay: number
): number {
  if (isPremiumEmail(email)) return publishedMaxDay;
  return Math.min(FREE_ACCESS_DAYS, publishedMaxDay);
}
