import Link from "next/link";
import {
  BarChart3,
  CalendarDays,
  FileText,
  Map,
  ShieldCheck,
  Sparkles,
  Trophy,
  Zap,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { HeroScrollButton } from "@/components/landing/HeroScrollButton";
import { Button } from "@/components/ui/Button";
import { FREE_ACCESS_DAYS } from "@/lib/premium-access";

const features = [
  {
    icon: CalendarDays,
    title: "Daily Guided Plans",
    desc: "Structured day-wise execution system.",
  },
  {
    icon: Trophy,
    title: "Live Rankings & Leaderboards",
    desc: "Compete with aspirants across India.",
  },
  {
    icon: FileText,
    title: "Expert Curated PDFs & Notes",
    desc: "Concise exam-focused study material.",
  },
  {
    icon: Map,
    title: "Mind Maps & Revision",
    desc: "Visual learning and fast revision tools.",
  },
  {
    icon: BarChart3,
    title: "Performance Analytics",
    desc: "Track accuracy, ranks, and progress.",
  },
  {
    icon: ShieldCheck,
    title: "Discipline Tracking",
    desc: "Build consistency and execution habits.",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen overflow-hidden">
      <header className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-5 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 shadow-lg shadow-violet-500/20">
            <Zap className="h-5 w-5 text-white" />
          </span>
          <div>
            <p className="text-base font-semibold tracking-tight text-white">
              ToThePoint
            </p>
            <p className="text-xs text-zinc-500">SSC CGL Guided Preparation</p>
          </div>
        </Link>

        <div className="flex items-center gap-2">
          <Link href="/leaderboard">
            <Button variant="ghost" size="sm">
              Leaderboard
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="secondary" size="sm">
              Premium login
            </Button>
          </Link>
        </div>
      </header>

      <main className="mx-auto flex min-h-[calc(100vh-5.5rem)] w-full max-w-7xl items-center px-4 pb-6 sm:px-6 lg:px-8">
        <section className="relative w-full overflow-hidden rounded-[2rem] border border-white/10 bg-[#111113]/85 px-6 py-8 shadow-[0_0_60px_rgba(124,58,237,0.10)] sm:px-8 sm:py-10 lg:px-12 lg:py-12">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(124,58,237,0.18),transparent_32%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.12),transparent_28%)]" />
          <div className="relative grid gap-10 lg:grid-cols-[minmax(0,1.1fr)_minmax(360px,0.9fr)] lg:items-center">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs text-violet-200">
                <Sparkles className="h-3.5 w-3.5" />
                Premium execution system for serious SSC aspirants
              </div>

              <h1 className="mt-6 text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl lg:leading-[1.05]">
                ToThePoint — SSC CGL 2026
              </h1>

              <p className="mt-4 text-xl text-zinc-200 sm:text-2xl">
                Your final destination for clearing SSC CGL 2026.
              </p>

              <p className="mt-6 max-w-2xl text-base leading-7 text-zinc-400 sm:text-lg">
                Structured daily execution system with quizzes, PDF notes, mind
                maps, analysis, rankings, and discipline tracking — all in one
                place.
              </p>

              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <HeroScrollButton />
              </div>

              <div className="mt-8 grid gap-2 text-sm text-zinc-400 sm:max-w-xl">
                <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2">
                  {FREE_ACCESS_DAYS} days free access
                </span>
                <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2">
                  75-day guided roadmap
                </span>
                <span className="rounded-full border border-white/10 bg-white/5 px-3 py-2">
                  First-attempt ranking system
                </span>
              </div>
            </div>

            <Card className="relative overflow-hidden border-white/10 bg-white/[0.03] p-6">
              <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-violet-400/60 to-transparent" />
              <div className="grid gap-4">
                <div>
                  <p className="text-sm font-medium text-violet-300">
                    Core Features
                  </p>
                  <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white">
                    Built for disciplined SSC execution.
                  </h2>
                </div>

                <div className="grid gap-3 sm:grid-cols-2">
                  {features.map((feature) => (
                    <div
                      key={feature.title}
                      className="group rounded-2xl border border-white/10 bg-white/[0.04] p-4 backdrop-blur-sm transition duration-300 hover:-translate-y-1 hover:border-violet-400/30 hover:bg-white/[0.06] hover:shadow-[0_0_30px_rgba(124,58,237,0.12)]"
                    >
                      <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-violet-500/20 bg-violet-500/10 text-violet-300 transition duration-300 group-hover:scale-105 group-hover:bg-violet-500/15">
                        <feature.icon className="h-4 w-4" />
                      </div>
                      <h3 className="mt-4 text-sm font-semibold leading-6 text-white">
                        {feature.title}
                      </h3>
                      <p className="mt-1 text-sm leading-6 text-zinc-400">
                        {feature.desc}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          </div>
        </section>
      </main>
    </div>
  );
}
