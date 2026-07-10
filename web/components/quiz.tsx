'use client';
import { useState } from 'react';
import { cn } from '@/lib/cn';
import { Check, X } from 'lucide-react';

export interface QuizQuestion {
  q: string;
  options: string[];
  answer: number; // index into options
  why?: string;
}

function Question({ q, options, answer, why }: QuizQuestion) {
  const [picked, setPicked] = useState<number | null>(null);
  const correct = picked === answer;

  return (
    <div className="not-prose">
      <p className="font-medium mb-3">{q}</p>
      <div className="flex flex-col gap-2">
        {options.map((opt, i) => (
          <button
            key={i}
            type="button"
            disabled={picked !== null}
            onClick={() => setPicked(i)}
            className={cn(
              'flex items-center gap-2 rounded-lg border px-4 py-2.5 text-start text-sm transition-all',
              picked === null &&
                'cursor-pointer hover:border-fd-primary hover:bg-fd-accent hover:translate-x-0.5',
              picked !== null && i === answer && 'border-green-500 bg-green-500/10',
              picked === i && i !== answer && 'border-red-500 bg-red-500/10',
              picked !== null && picked !== i && i !== answer && 'opacity-50',
            )}
          >
            {picked !== null && i === answer && <Check className="size-4 shrink-0 text-green-500" />}
            {picked === i && i !== answer && <X className="size-4 shrink-0 text-red-500" />}
            {opt}
          </button>
        ))}
      </div>
      {picked !== null && (
        <p
          className={cn(
            'mt-3 text-sm animate-in fade-in slide-in-from-bottom-1',
            correct ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400',
          )}
        >
          {correct ? 'Correct!' : 'Not quite.'}{' '}
          <span className="text-fd-muted-foreground">{why}</span>
        </p>
      )}
    </div>
  );
}

export function Quiz({ questions }: { questions: QuizQuestion[] }) {
  return (
    <div className="my-6 flex flex-col gap-6 rounded-xl border bg-fd-card p-5 shadow-sm">
      <p className="not-prose -mb-2 text-xs font-semibold uppercase tracking-wider text-fd-primary">
        Quick check
      </p>
      {questions.map((q, i) => (
        <Question key={i} {...q} />
      ))}
    </div>
  );
}
