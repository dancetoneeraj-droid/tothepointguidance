"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Zap } from "lucide-react";
import { GoogleSignInButton } from "@/components/auth/GoogleSignInButton";
import { AuthForm } from "@/components/auth/AuthForm";
import { useAuth } from "@/components/providers/AuthProvider";
import { Card } from "@/components/ui/Card";

export default function LoginPage() {
  const { isAuthenticated, loading, signIn, authAvailable } = useAuth();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, loading, router]);

  const handleLogin = async (data: {
    fullName: string;
    phone: string;
    email: string;
    password: string;
  }) => {
    setError(null);
    setSubmitting(true);
    try {
      await signIn(data.email, data.password);
      router.replace("/dashboard");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Login failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4">
      <Link href="/" className="flex items-center gap-2 mb-8">
        <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600">
          <Zap className="h-5 w-5 text-white" />
        </span>
        <span className="text-xl font-semibold">ToThePoint</span>
      </Link>

      <Card className="w-full max-w-md p-6 sm:p-8" glow>
        <h1 className="text-xl font-semibold text-foreground">Log in</h1>
        <p className="mt-2 text-sm text-muted leading-relaxed">
          Day 1–3 are free without login. Premium members log in here to unlock
          Day 4 and beyond.
        </p>

        {!authAvailable ? (
          <p className="mt-4 text-sm text-amber-400">
            Configure Firebase in .env.local to enable authentication.
          </p>
        ) : (
          <>
            <div className="mt-6">
              <AuthForm
                mode="login"
                onSubmit={handleLogin}
                loading={submitting}
                error={error}
              />
            </div>
            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-border" />
              <span className="text-xs text-muted">or</span>
              <div className="h-px flex-1 bg-border" />
            </div>
            <GoogleSignInButton />
          </>
        )}

        <p className="mt-6 text-center text-sm text-muted">
          New here?{" "}
          <Link href="/signup" className="text-violet-400 hover:text-violet-300">
            Create an account
          </Link>
          <span className="mx-2 text-border">·</span>
          <Link href="/dashboard" className="text-violet-400 hover:text-violet-300">
            Continue free (Day 1–3)
          </Link>
        </p>
      </Card>

      <Link
        href="/"
        className="mt-6 text-sm text-muted hover:text-foreground transition-colors"
      >
        ← Back to home
      </Link>
    </div>
  );
}
