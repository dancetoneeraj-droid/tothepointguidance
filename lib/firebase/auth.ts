/**
 * Firebase Authentication (no Firestore).
 */

export function isFirebaseAuthConfigured(): boolean {
  return Boolean(
    process.env.NEXT_PUBLIC_FIREBASE_API_KEY &&
      process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID
  );
}

function getFirebaseConfig() {
  return {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
    authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
    projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
    storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  };
}

export async function getFirebaseAuth() {
  if (!isFirebaseAuthConfigured()) {
    throw new Error(
      "Firebase is not configured. Add NEXT_PUBLIC_FIREBASE_* keys to .env.local"
    );
  }

  const { initializeApp, getApps } = await import("firebase/app");
  const { getAuth } = await import("firebase/auth");

  const app =
    getApps().length > 0 ? getApps()[0]! : initializeApp(getFirebaseConfig());
  return getAuth(app);
}

export type AuthProfile = {
  uid: string;
  displayName: string | null;
  email: string | null;
  photoURL: string | null;
};

function mapUser(user: {
  uid: string;
  displayName: string | null;
  email: string | null;
  photoURL: string | null;
}): AuthProfile {
  return {
    uid: user.uid,
    displayName: user.displayName,
    email: user.email,
    photoURL: user.photoURL,
  };
}

export async function signUpWithEmailPassword(
  email: string,
  password: string,
  displayName: string
): Promise<AuthProfile> {
  const auth = await getFirebaseAuth();
  const { createUserWithEmailAndPassword, updateProfile } = await import(
    "firebase/auth"
  );

  const result = await createUserWithEmailAndPassword(
    auth,
    email.trim(),
    password
  );

  if (displayName.trim()) {
    await updateProfile(result.user, { displayName: displayName.trim() });
  }

  return mapUser(result.user);
}

export async function signInWithEmailPassword(
  email: string,
  password: string
): Promise<AuthProfile> {
  const auth = await getFirebaseAuth();
  const { signInWithEmailAndPassword } = await import("firebase/auth");
  const result = await signInWithEmailAndPassword(
    auth,
    email.trim(),
    password
  );
  return mapUser(result.user);
}

export async function signInWithGooglePopup(): Promise<AuthProfile> {
  const auth = await getFirebaseAuth();
  const { GoogleAuthProvider, signInWithPopup } = await import("firebase/auth");
  const result = await signInWithPopup(auth, new GoogleAuthProvider());
  return mapUser(result.user);
}

export async function signOutFirebase(): Promise<void> {
  if (!isFirebaseAuthConfigured()) return;
  try {
    const auth = await getFirebaseAuth();
    const { signOut } = await import("firebase/auth");
    await signOut(auth);
  } catch {
    // ignore
  }
}

export async function subscribeToAuthState(
  onUser: (user: AuthProfile | null) => void
): Promise<() => void> {
  if (!isFirebaseAuthConfigured()) {
    onUser(null);
    return () => {};
  }

  const auth = await getFirebaseAuth();
  const { onAuthStateChanged } = await import("firebase/auth");

  return onAuthStateChanged(auth, (user) => {
    onUser(user ? mapUser(user) : null);
  });
}
