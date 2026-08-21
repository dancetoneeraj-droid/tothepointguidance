/** Shared Firestore database accessor. */
export async function getDb() {
  try {
    const { initializeApp, getApps } = await import("firebase/app");
    const apiKey = process.env.NEXT_PUBLIC_FIREBASE_API_KEY;
    const projectId = process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID;
    if (!apiKey || !projectId) return null;

    const app =
      getApps().length > 0
        ? getApps()[0]!
        : initializeApp({
            apiKey,
            authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
            projectId,
            storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
            messagingSenderId:
              process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
            appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
          });

    const { getFirestore } = await import("firebase/firestore");
    return getFirestore(app);
  } catch {
    return null;
  }
}
