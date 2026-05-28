import type { DailyPlan } from "@/types";
import schedule75 from "@/data/schedule-75.json";
import { PROGRAM_DAYS } from "@/lib/maths-topics";

const PLANS: DailyPlan[] = (schedule75 as { plans: DailyPlan[] }).plans;

export const MAX_PUBLISHED_DAY = PROGRAM_DAYS;

export function getDailyPlan(day: number): DailyPlan | null {
  const plan = PLANS.find((p) => p.day === day);
  return plan ?? null;
}

export function getAllPublishedPlans(): DailyPlan[] {
  return PLANS.filter((p) => p.published);
}

export function isDayPublished(day: number): boolean {
  const plan = getDailyPlan(day);
  return plan?.published ?? false;
}

export function getComingSoonDay(): number {
  return MAX_PUBLISHED_DAY + 1;
}
