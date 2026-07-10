'use client';
import { useEffect } from 'react';
import { Flame } from 'lucide-react';
import { recordVisit, streak, useProgress } from '@/lib/progress';
import { TOTAL_CHAPTERS } from '@/lib/shared';

export function ProgressPill() {
  const progress = useProgress();
  useEffect(recordVisit, []);
  if (!progress) return null;

  const done = Object.keys(progress.done).length;
  const s = streak(progress.days);
  const pct = Math.round((done / TOTAL_CHAPTERS) * 100);

  return (
    <div
      className="fixed bottom-4 right-4 z-40 flex items-center gap-2 rounded-full border bg-fd-background/80 px-3 py-1.5 text-xs font-medium shadow-lg backdrop-blur"
      title={`${done} of ${TOTAL_CHAPTERS} chapters complete`}
    >
      <span className="relative h-1.5 w-16 overflow-hidden rounded-full bg-fd-muted">
        <span
          className="absolute inset-y-0 left-0 rounded-full bg-fd-primary transition-all"
          style={{ width: `${pct}%` }}
        />
      </span>
      {done}/{TOTAL_CHAPTERS}
      {s > 1 && (
        <span className="flex items-center gap-0.5 text-orange-500">
          <Flame className="size-3.5" />
          {s}
        </span>
      )}
    </div>
  );
}
