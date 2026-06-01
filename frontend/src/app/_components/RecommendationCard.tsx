/**
 * Recommendation result card for a ranked Marvel Rivals hero.
 */

import type { Recommendation } from "@/types/rivalytics";

type RecommendationCardProps = {
  recommendation: Recommendation;
  rank: number;
};

function formatNumber(value?: number) {
  if (value === undefined || Number.isNaN(value)) return "N/A";
  return value.toFixed(2);
}

export function RecommendationCard({
  recommendation,
  rank,
}: RecommendationCardProps) {
  return (
    <article className="rounded-2xl border border-slate-800 bg-slate-950 p-5 transition hover:border-indigo-500">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-black uppercase tracking-wide text-slate-500">
            Rank #{rank}
          </p>
          <h3 className="mt-1 text-2xl font-black">{recommendation.hero}</h3>
        </div>

        <div className="flex flex-col items-end gap-2">
          <span className="rounded-full bg-indigo-600 px-3 py-1 text-xs font-black">
            {recommendation.role}
          </span>
          <span className="rounded-full border border-slate-700 px-3 py-1 text-xs font-black text-slate-300">
            Tier {recommendation.tier ?? "N/A"}
          </span>
        </div>
      </div>

      <div className="mt-5 rounded-xl bg-slate-900 p-4">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
          Final Score
        </p>
        <p className="mt-1 text-4xl font-black text-indigo-400">
          {formatNumber(recommendation.score)}
        </p>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
        <div className="rounded-xl bg-slate-900 p-3">
          <p className="text-slate-500">Win</p>
          <p className="mt-1 font-black">
            {formatNumber(recommendation.win_rate)}%
          </p>
        </div>
        <div className="rounded-xl bg-slate-900 p-3">
          <p className="text-slate-500">Pick</p>
          <p className="mt-1 font-black">
            {formatNumber(recommendation.pick_rate)}%
          </p>
        </div>
        <div className="rounded-xl bg-slate-900 p-3">
          <p className="text-slate-500">Ban</p>
          <p className="mt-1 font-black">
            {formatNumber(recommendation.ban_rate)}%
          </p>
        </div>
      </div>

      <div className="mt-4 space-y-2 border-t border-slate-800 pt-3 text-xs text-slate-400">
        <div className="flex justify-between">
          <span>Base score</span>
          <span>{formatNumber(recommendation.base_score)}</span>
        </div>
        <div className="flex justify-between">
          <span>Team-up score</span>
          <span>{formatNumber(recommendation.teamup_score)}</span>
        </div>
      </div>
    </article>
  );
}