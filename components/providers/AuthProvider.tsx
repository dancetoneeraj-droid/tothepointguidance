"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import {
  isFirebaseAuthConfigured,
  signInWithEmailPassword,
  signInWithGooglePopup,
  signOutFirebase,
  signUpWithEmailPassword,
  subscribeToAuthState,
  type AuthProfile,
} from "@/lib/firebase/auth";
import { hydrateFromFirestore, registerPersistOnUnload } from "@/lib/firebase/firestore";
import { isPremiumEmail } from "@/lib/premium-access";
import {
  activateGuestSession,
  activateStudentSession,
  getActiveStudentId,
  getStudentProgress,
  initStudentProgress,
  recordLastLogin,
} from "@/lib/storage";
import { loadStore, writeLocalCache } from "@/lib/storage/client";
import { GUEST_STUDENT_ID } from "@/lib/storage/constants";
import type { StudentProgress } from "@/types";

interface SignUpInput {
  fullName: string;
  phone: string;
  email: string;
  password: string;
}

interface AuthContextValue {
  studentId: string;
  progress: StudentProgress | null;
  user: AuthProfile | null;
  loading: boolean;
  isGuest: boolean;
  isAuthenticated: boolean;
  isPremium: boolean;
  authAvailable: boolean;
  signUp: (input: SignUpInput) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
  refreshProgress: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

async function bindUserProfile(profile: AuthProfile, phone?: string) {
  const p = await initStudentProgress(profile.uid, {
    displayName: profile.displayName ?? "Student",
    email: profile.email ?? "",
    phone,
    photoURL: profile.photoURL ?? undefined,
    isGuest: false,
  });
  activateStudentSession(profile.uid);
  return p;
}

function useGuestSession() {
  const p = activateGuestSession();
  return { studentId: GUEST_STUDENT_ID, progress: p, isGuest: true as const };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [studentId, setStudentId] = useState("");
  const [progress, setProgress] = useState<StudentProgress | null>(null);
  const [user, setUser] = useState<AuthProfile | null>(null);
  const [isGuest, setIsGuest] = useState(true);
  const [loading, setLoading] = useState(true);
  const authAvailable = isFirebaseAuthConfigured();

  const isAuthenticated = Boolean(user?.uid);
  const isPremium = isPremiumEmail(user?.email ?? progress?.email);

  const refreshProgress = useCallback(async () => {
    const id = getActiveStudentId() ?? studentId;
    if (!id) return;
    const p = await getStudentProgress(id);
    if (p) setProgress(p);
  }, [studentId]);

  const applyGuestSession = useCallback(() => {
    const guest = useGuestSession();
    setUser(null);
    setStudentId(guest.studentId);
    setProgress(guest.progress);
    setIsGuest(true);
  }, []);

  const handleAuthUser = useCallback(
    async (profile: AuthProfile | null) => {
      if (!profile) {
        applyGuestSession();
        return;
      }

      setUser(profile);
      setIsGuest(false);

      // Merge local cache with Firestore, persist merged result to cloud.
      try {
        const localStore = loadStore(profile.uid);
        await hydrateFromFirestore(profile.uid, localStore, writeLocalCache);
        registerPersistOnUnload(profile.uid);
      } catch (error) {
        console.error("[Auth] Firestore hydration failed:", error);
      }

      // Load (or create) the student profile from localStorage (now up to date).
      const existing = await getStudentProgress(profile.uid);
      const p = existing
        ? await initStudentProgress(profile.uid, {
            displayName: profile.displayName ?? existing.displayName,
            email: profile.email ?? existing.email,
            phone: existing.phone,
            photoURL: profile.photoURL ?? existing.photoURL,
            isGuest: false,
          })
        : await bindUserProfile(profile);

      activateStudentSession(profile.uid);
      setStudentId(profile.uid);
      setProgress(p);

      // Record login timestamp (triggers a Firestore sync automatically).
      recordLastLogin(profile.uid);
    },
    [applyGuestSession]
  );

  useEffect(() => {
    let cancelled = false;
    let unsubscribe: (() => void) | undefined;

    async function init() {
      try {
        if (!authAvailable) {
          if (!cancelled) {
            applyGuestSession();
            setLoading(false);
          }
          return;
        }

        unsubscribe = await subscribeToAuthState((profile) => {
          if (cancelled) return;
          void handleAuthUser(profile).finally(() => {
            if (!cancelled) setLoading(false);
          });
        });
      } catch {
        if (!cancelled) {
          applyGuestSession();
          setLoading(false);
        }
      }
    }

    void init();

    return () => {
      cancelled = true;
      unsubscribe?.();
    };
  }, [authAvailable, handleAuthUser, applyGuestSession]);

  const signUp = useCallback(async (input: SignUpInput) => {
    const profile = await signUpWithEmailPassword(
      input.email,
      input.password,
      input.fullName
    );
    const p = await bindUserProfile(profile, input.phone);
    setUser(profile);
    setStudentId(profile.uid);
    setProgress(p);
    setIsGuest(false);
    recordLastLogin(profile.uid);
  }, []);

  const signIn = useCallback(
    async (email: string, password: string) => {
      const profile = await signInWithEmailPassword(email, password);
      await handleAuthUser(profile);
    },
    [handleAuthUser]
  );

  const signInWithGoogle = useCallback(async () => {
    const profile = await signInWithGooglePopup();
    await handleAuthUser(profile);
  }, [handleAuthUser]);

  const signOut = useCallback(async () => {
    await signOutFirebase();
    applyGuestSession();
  }, [applyGuestSession]);

  return (
    <AuthContext.Provider
      value={{
        studentId,
        progress,
        user,
        loading,
        isGuest,
        isAuthenticated,
        isPremium,
        authAvailable,
        signUp,
        signIn,
        signInWithGoogle,
        signOut,
        refreshProgress,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
