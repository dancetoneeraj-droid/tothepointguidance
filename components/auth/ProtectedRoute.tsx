"use client";

import { useAuth } from "@/components/providers/AuthProvider";

/** Ensures study progress is loaded (guest or logged-in). Does not require login. */
export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { progress, loading } = useAuth();

  if (loading || !progress) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-violet-500 border-t-transparent" />
          <p className="text-sm text-muted">Loading your study plan...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
