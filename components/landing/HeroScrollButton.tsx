"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/Button";

export function HeroScrollButton() {
  return (
    <Link href="/dashboard">
      <Button size="lg" className="w-full sm:w-auto">
        Start Your Journey
        <ArrowRight className="h-4 w-4" />
      </Button>
    </Link>
  );
}
