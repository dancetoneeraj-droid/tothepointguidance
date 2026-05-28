# Maths question banks (SSC CGL)

**Program:** 75 days · **4 quizzes/day** · **25 questions / 25 minutes** each  
**Per topic target:** ~275 questions (11 quizzes × 25) — banks hold **300** slots.

## 17 topics

**Arithmetic:** percentage, ratio-proportion, profit-loss, time-work, time-speed-distance, average, partnership, mixture-alligation, simple-interest, compound-interest  

**Advance:** trigonometry, di, mensuration-3d, algebra, mensuration-2d, geometry, number-system

## Add questions

1. Put JSON array in `datas/maths/{topic-slug}.json`
2. Run:

```bash
npm run import:maths -- percentage
```

## Regenerate 75-day plan

```bash
npm run generate:schedule
```

Rules baked in:
- 4 random topics per day (deterministic shuffle)
- If a topic appears on Day *n*, it **must** appear again on Day *n+2* (Average: Day *n+3*)
- ~11 sessions per topic across 75 days

## Placeholder banks

```bash
npm run generate:maths-banks
```
