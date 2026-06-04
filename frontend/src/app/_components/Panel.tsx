/**
 * Reusable dashboard panel for Rivalytics sections.
 */

import type { ReactNode } from "react";

type PanelProps = {
  title: string;
  subtitle?: string;
  children: ReactNode;
};

export function Panel({ title, subtitle, children }: PanelProps) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/90 p-6 shadow-xl">
      <div className="mb-5">
        <h2 className="text-xl font-black tracking-tight text-white">{title}</h2>
        {subtitle && <p className="mt-1 text-sm text-slate-400">{subtitle}</p>}
      </div>

      {children}
    </section>
  );
}