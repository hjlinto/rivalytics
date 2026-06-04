"use client";

/**
 * Hero recommendation card.
 *
 * Displays a hero avatar, recommendation rank, role, tier, and public-facing
 * statistics. Internal scoring values are intentionally hidden from users.
 */

import type { SyntheticEvent } from "react";

import type { Recommendation } from "@/types/rivalytics";

type RecommendationCardProps = {
  recommendation: Recommendation;
  rank: number;
};

function formatPercent(value?: number) {
  if (value === undefined || Number.isNaN(value)) {
    return "N/A";
  }

  return `${value.toFixed(1)}%`;
}

function heroArtPath(heroName: string) {
  const slug = heroName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");

  return `/heroes/${slug}.png`;
}

function hideBrokenImage(event: SyntheticEvent<HTMLImageElement>) {
  event.currentTarget.style.display = "none";
}

export function RecommendationCard({
  recommendation,
  rank,
}: RecommendationCardProps) {
  return (
    <article className="rounded-3xl border border-slate-800 bg-slate-900 p-4 shadow-xl transition hover:-translate-y-0.5 hover:border-indigo-500 hover:shadow-indigo-950/30">
      <div className="flex items-center gap-4">
        <img
          src={heroArtPath(recommendation.hero)}
          alt={`${recommendation.hero} avatar`}
          onError={hideBrokenImage}
          className="h-24 w-24 shrink-0 rounded-xl border border-slate-700 object-cover"
        />

        <div className="min-w-0 flex-1">
          <p className="text-xs font-black uppercase tracking-wide text-indigo-300">
            Rank #{rank}
          </p>

          <h3 className="truncate text-2xl font-black tracking-tight text-white">
            {recommendation.hero}
          </h3>

          <div className="mt-2 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-indigo-600 px-3 py-1 text-xs font-black text-white">
              {recommendation.role}
            </span>

            <span className="rounded-full border border-slate-700 bg-slate-950 px-3 py-1 text-xs font-black text-slate-300">
              Tier {recommendation.tier ?? "N/A"}
            </span>
          </div>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
        <div className="rounded-2xl bg-slate-950 p-3">
          <p className="text-slate-500">Win Rate</p>
          <p className="mt-1 text-base font-black text-white">
            {formatPercent(recommendation.win_rate)}
          </p>
        </div>

        <div className="rounded-2xl bg-slate-950 p-3">
          <p className="text-slate-500">Pick Rate</p>
          <p className="mt-1 text-base font-black text-white">
            {formatPercent(recommendation.pick_rate)}
          </p>
        </div>

        <div className="rounded-2xl bg-slate-950 p-3">
          <p className="text-slate-500">Ban Rate</p>
          <p className="mt-1 text-base font-black text-white">
            {formatPercent(recommendation.ban_rate)}
          </p>
        </div>
      </div>
    </article>
  );
}