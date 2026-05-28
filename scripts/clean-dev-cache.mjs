import { rmSync } from "fs";
import { join } from "path";

const nextDir = join(process.cwd(), ".next");

try {
  rmSync(nextDir, { recursive: true, force: true });
  console.log("Removed .next — start dev with: npm run dev");
} catch (err) {
  console.error(
    "Could not remove .next. Stop `npm run dev` first (Ctrl+C), then run: npm run dev:clean"
  );
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
}
