'use client';
import { useEffect, useId, useState } from 'react';

// ponytail: theme read once at render; toggling dark mode mid-page won't
// restyle an already-drawn diagram until navigation. Revisit if it annoys.
export function Mermaid({ chart }: { chart: string }) {
  const id = useId().replace(/[^a-zA-Z0-9]/g, '');
  const [svg, setSvg] = useState('');

  useEffect(() => {
    let active = true;
    void (async () => {
      const { default: mermaid } = await import('mermaid');
      mermaid.initialize({
        startOnLoad: false,
        theme: document.documentElement.classList.contains('dark') ? 'dark' : 'default',
        fontFamily: 'inherit',
      });
      const out = await mermaid.render(`m${id}`, chart.trim());
      if (active) setSvg(out.svg);
    })();
    return () => {
      active = false;
    };
  }, [chart, id]);

  return (
    <div
      className="my-6 flex justify-center overflow-x-auto [&_svg]:max-w-full"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}
