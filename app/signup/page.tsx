"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Zap } from "lucide-react";
import { AuthForm } from "@/components/auth/AuthForm";
import { useAuth } from "@/components/providers/AuthProvider";
import { Card } from "@/components/ui/Card";

export default function SignupPage() {
  const { isAuthenticated, loading, signUp, authAvailable } = useAuth();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, loading, router]);

  const handleSignup = async (data: {
    fullName: string;
    phone: string;
    email: string;
    password: string;
  }) => {
    if (!data.fullName.trim() || !data.phone.trim()) {
      setError("Full name and phone number are required.");
      return;
    }
    setError(null);
    setSubmitting(true);
    try {
      await signUp({
        fullName: data.fullName.trim(),
        phone: data.phone.trim(),
        email: data.email.trim(),
        password: data.password,
      });
      router.replace("/dashboard");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Signup failed");
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
        <h1 className="text-xl font-semibold text-foreground">Sign up</h1>
        <p className="mt-2 text-sm text-muted leading-relaxed">
          Create a premium account. Your email must be approved in the premium
          list to access Day 4+.
        </p>

        {!authAvailable ? (
          <p className="mt-4 text-sm text-amber-400">
            Configure Firebase in .env.local to enable authentication.
          </p>
        ) : (
          <div className="mt-6">
            <AuthForm
              mode="signup"
              onSubmit={handleSignup}
              loading={submitting}
              error={error}
            />
          </div>
        )}

        <p className="mt-6 text-center text-sm text-muted">
          Already have an account?{" "}
          <Link href="/login" className="text-violet-400 hover:text-violet-300">
            Log in
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
