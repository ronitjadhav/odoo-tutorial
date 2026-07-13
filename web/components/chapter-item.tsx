'use client';
import { usePathname } from 'next/navigation';
import { SidebarItem } from 'fumadocs-ui/components/sidebar/base';
import type * as PageTree from 'fumadocs-core/page-tree';
import { CheckCircle2 } from 'lucide-react';
import { useProgress } from '@/lib/progress';

/** Sidebar item that shows a checkmark once the chapter is marked complete. */
export function ChapterItem({ item }: { item: PageTree.Item }) {
  const pathname = usePathname();
  const progress = useProgress();
  const chapter = String(item.url).match(/\/(\d{2})-[^/]+\/?$/)?.[1];
  const done = !!(chapter && progress?.done[chapter]);

  return (
    <SidebarItem
      href={item.url}
      external={item.external}
      active={pathname === item.url}
      icon={item.icon}
    >
      <span className="min-w-0 flex-1 truncate">{item.name}</span>
      {done && (
        <CheckCircle2
          aria-label="Chapter complete"
          className="size-3.5 shrink-0 text-green-500"
        />
      )}
    </SidebarItem>
  );
}
