'use client';
import { useSyncExternalStore } from 'react';

// All learner state lives in localStorage — no accounts, no backend.
const KEY = 'z2oe-progress';

export interface Progress {
  done: Record<string, string>; // chapter id ("09") -> ISO date completed
  days: string[]; // ISO dates with activity, for the streak
}

const EMPTY: Progress = { done: {}, days: [] };
let cache: Progress | null = null;
const listeners = new Set<() => void>();

function load(): Progress {
  if (cache) return cache;
  try {
    cache = { ...EMPTY, ...JSON.parse(localStorage.getItem(KEY) ?? '{}') };
  } catch {
    cache = EMPTY;
  }
  return cache!;
}

function save(next: Progress) {
  cache = next;
  localStorage.setItem(KEY, JSON.stringify(next));
  listeners.forEach((fn) => fn());
}

export function today(): string {
  return new Date().toISOString().slice(0, 10);
}

export function recordVisit() {
  const s = load();
  if (!s.days.includes(today())) {
    save({ ...s, days: [...s.days, today()].slice(-366) });
  }
}

export function toggleDone(chapter: string) {
  const s = load();
  const done = { ...s.done };
  if (done[chapter]) delete done[chapter];
  else done[chapter] = today();
  save({ ...s, done });
}

export function streak(days: string[], from = today()): number {
  let n = 0;
  const d = new Date(from + 'T12:00:00Z');
  while (days.includes(d.toISOString().slice(0, 10))) {
    n++;
    d.setUTCDate(d.getUTCDate() - 1);
  }
  return n;
}

export function useProgress(): Progress | null {
  // null on the server / first paint, so SSG markup never mismatches
  return useSyncExternalStore(
    (fn) => {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
    () => load(),
    () => null,
  );
}
