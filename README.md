# ToThePoint

SSC CGL guided daily preparation — **local-first MVP** (no Firestore, no cloud billing).

## Local MVP (default)

- All progress stored in **browser `localStorage`**
- Works **fully offline** after first load
- **Guest mode** by default — no Firebase required
- Google sign-in is **optional** (auth only, no database)

### Run

```bash
npm install
npm run dev
```

Open [http://localhost:3000/dashboard](http://localhost:3000/dashboard) — guest session starts automatically.

### What is stored locally

Per student profile (`guest` or Google `uid`):

- `currentDay`, `unlockedDay`, `completedQuizzes`, `overrideHistory`
- `mathsProgress`, `reasoningProgress`, `englishProgress`, `gkProgress`
- Quiz scores, accuracy, streak, day completion

Storage keys: `tothepoint:activeStudentId`, `tothepoint:v1:student:{id}`

## Optional Google sign-in

Add Firebase **Auth only** credentials to `.env.local` (see `.env.example`).  
Do **not** enable Firestore for this MVP.

## Project structure

```
lib/storage/     # localStorage (MVP) — swap for Firebase adapter later
lib/firebase/    # optional auth only
data/            # daily plans + question JSON
```

## Re-adding Firebase later

1. Implement `lib/firebase/firestore-adapter.ts` mirroring `lib/storage/progress.ts` APIs
2. Toggle via env `NEXT_PUBLIC_USE_FIRESTORE=true`
3. Keep `LocalStudentStore` shape as sync contract

## Scripts

```bash
npm run dev
npm run build
npm run generate:questions
```
