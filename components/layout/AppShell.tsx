"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  LogOut,
  Menu,
  X,
  Zap,
  Calendar,
  Trophy,
  BarChart3,
} from "lucide-react";
import { useState } from "react";
import { useAuth } from "@/components/providers/AuthProvider";
import { Button } from "@/components/ui/Button";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/schedule", label: "Schedule", icon: BarChart3 },
  { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { progress, isGuest, signOut } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6">
          <Link href="/dashboard" className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-violet-600 to-indigo-600">
              <Zap className="h-4 w-4 text-white" />
            </span>
            <span className="font-semibold text-foreground tracking-tight">
              ToThePoint
            </span>
          </Link>

          <nav className="hidden sm:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors ${
                    active
                      ? "bg-surface-hover text-foreground"
                      : "text-muted hover:text-foreground"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              );
            })}
            {progress ? (
              <Link
                href={`/day/${progress.currentDay}`}
                className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-violet-400 hover:bg-violet-500/10 transition-colors"
              >
                <Calendar className="h-4 w-4" />
                Day {progress.currentDay}
              </Link>
            ) : null}
          </nav>

          <div className="flex items-center gap-2">
            {progress?.photoURL ? (
              <img
                src={progress.photoURL}
                alt=""
                className="hidden sm:block h-8 w-8 rounded-full ring-2 ring-border"
              />
            ) : null}
            {isGuest ? (
              <Link href="/login">
                <Button variant="secondary" size="sm" className="hidden sm:inline-flex">
                  Premium login
                </Button>
              </Link>
            ) : (
              <Button
                variant="ghost"
                size="sm"
                className="hidden sm:inline-flex"
                onClick={() => void handleSignOut()}
              >
                <LogOut className="h-4 w-4" />
                Sign out
              </Button>
            )}
            <button
              className="sm:hidden rounded-lg p-2 text-muted hover:bg-surface-hover"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label="Menu"
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </header>

      {mobileOpen ? (
        <div className="sm:hidden border-b border-border bg-surface-elevated px-4 py-3 space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setMobileOpen(false)}
              className="block rounded-lg px-3 py-2 text-sm text-foreground hover:bg-surface-hover"
            >
              {item.label}
            </Link>
          ))}
          {progress ? (
            <Link
              href={`/day/${progress.currentDay}`}
              onClick={() => setMobileOpen(false)}
              className="block rounded-lg px-3 py-2 text-sm text-violet-400"
            >
              Day {progress.currentDay}
            </Link>
          ) : null}
          {isGuest ? (
            <Link
              href="/login"
              onClick={() => setMobileOpen(false)}
              className="block rounded-lg px-3 py-2 text-sm text-violet-400"
            >
              Premium login
            </Link>
          ) : (
            <button
              onClick={() => void handleSignOut()}
              className="w-full text-left rounded-lg px-3 py-2 text-sm text-muted hover:bg-surface-hover"
            >
              Sign out
            </button>
          )}
        </div>
      ) : null}

      <main className="mx-auto max-w-6xl px-4 sm:px-6 py-6 sm:py-8">{children}</main>
    </div>
  );
}
