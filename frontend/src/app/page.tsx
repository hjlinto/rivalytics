"use client";

/**
 * Rivalytics home page.
 *
 * This page owns the recommendation workflow:
 * - loading hero data from the backend
 * - tracking draft selections
 * - submitting recommendation requests
 * - rendering the composed dashboard layout
 */

import { useEffect, useState } from "react";
import type { Dispatch, SetStateAction } from "react";

import { HeroInput } from "./_components/HeroInput";
import { Panel } from "./_components/Panel";
import { RecommendationCard } from "./_components/RecommendationCard";
import { StatPill } from "./_components/StatPill";
import type { Hero, Recommendation } from "@/types/rivalytics";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

function updateSlot(
  setter: Dispatch<SetStateAction<string[]>>,
  index: number,
  value: string
) {
  setter((current) => {
    const copy = [...current];
    copy[index] = value;
    return copy;
  });
}

export default function Home() {
  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [myTeam, setMyTeam] = useState<string[]>(["", "", "", "", ""]);
  const [enemyTeam, setEnemyTeam] = useState<string[]>(["", "", "", "", "", ""]);
  const [bans, setBans] = useState<string[]>(["", "", "", ""]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loadingHeroes, setLoadingHeroes] = useState(false);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchHeroes() {
      try {
        setLoadingHeroes(true);
        setError("");

        const response = await fetch(`${API_BASE_URL}/heroes`);

        if (!response.ok) {
          throw new Error("Failed to fetch heroes.");
        }

        const data = await response.json();
        setHeroes(data.heroes ?? []);
      } catch {
        setError("Could not load heroes. Make sure the backend is running.");
        setHeroes([]);
      } finally {
        setLoadingHeroes(false);
      }
    }

    fetchHeroes();
  }, []);

  const heroNames = heroes.map((hero) => hero.name);

  function cleanTeam(values: string[]) {
    return values.filter((name) => name.trim() !== "" && heroNames.includes(name));
  }

  async function getRecommendations() {
    try {
      setLoadingRecommendations(true);
      setError("");

      const payload = {
        my_team: cleanTeam(myTeam),
        enemy_team: cleanTeam(enemyTeam),
        bans: cleanTeam(bans),
        role_needed: null,
        top_n: 5,
      };

      const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch recommendations.");
      }

      const data = await response.json();
      setRecommendations(data.recommendations ?? []);
    } catch {
      setError("Could not fetch recommendations.");
      setRecommendations([]);
    } finally {
      setLoadingRecommendations(false);
    }
  }

  function clearDraft() {
    setMyTeam(["", "", "", "", ""]);
    setEnemyTeam(["", "", "", "", "", ""]);
    setBans(["", "", "", ""]);
    setRecommendations([]);
    setError("");
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="w-full px-6 py-8 lg:px-10">
        <header className="mb-8 overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 p-8 shadow-2xl">
          <div className="flex flex-col gap-8 xl:flex-row xl:items-end xl:justify-between">
            <div className="max-w-5xl">
              <p className="text-sm font-black uppercase tracking-[0.35em] text-indigo-400">
                Rivalytics
              </p>
              <h1 className="mt-3 text-5xl font-black tracking-tight md:text-6xl">
                Marvel Rivals Recommendation Engine
              </h1>
              <p className="mt-5 max-w-4xl text-lg leading-8 text-slate-400">
                Build a draft scenario, account for allied picks, enemy picks,
                and bans, then generate ranked recommendations using hero meta
                data and team-up synergy.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 xl:w-[26rem]">
              <button
                type="button"
                onClick={getRecommendations}
                disabled={loadingHeroes || loadingRecommendations}
                className="rounded-xl bg-indigo-600 px-6 py-4 text-sm font-black uppercase tracking-wide text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loadingRecommendations ? "Generating..." : "Recommend"}
              </button>

              <button
                type="button"
                onClick={clearDraft}
                className="rounded-xl border border-slate-700 px-6 py-4 text-sm font-black uppercase tracking-wide text-slate-300 transition hover:bg-slate-800"
              >
                Clear Draft
              </button>
            </div>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            <StatPill label="Heroes Loaded" value={String(heroes.length)} />
            <StatPill label="Recommendation Model" value="Meta + Synergy" />
            <StatPill label="Results" value="Top 5 Picks" />
          </div>
        </header>

        {error && (
          <div className="mb-6 rounded-xl border border-red-500/60 bg-red-950/60 p-4 text-sm font-semibold text-red-200">
            {error}
          </div>
        )}

        <div className="grid w-full gap-6 xl:grid-cols-[minmax(0,1.6fr)_minmax(30rem,0.9fr)]">
          <section className="space-y-6">
            {loadingHeroes ? (
              <Panel title="Draft Builder">
                <p className="text-slate-400">Loading hero data...</p>
              </Panel>
            ) : (
              <>
                <Panel
                  title="Draft Builder"
                  subtitle="Select the current match context before generating recommendations."
                >
                  <div className="grid gap-6 2xl:grid-cols-2">
                    <div className="rounded-2xl border border-emerald-500/20 bg-emerald-950/10 p-5">
                      <h3 className="mb-4 text-sm font-black uppercase tracking-wide text-emerald-400">
                        Allied Team
                      </h3>

                      <div className="grid gap-3 sm:grid-cols-2">
                        {myTeam.map((value, index) => (
                          <HeroInput
                            key={`my-team-${index}`}
                            label={`Ally ${index + 1}`}
                            value={value}
                            heroes={heroes}
                            unavailableNames={[
                              ...myTeam.filter((name) => name && name !== value),
                              ...bans.filter(Boolean),
                            ]}
                            onChange={(newValue) =>
                              updateSlot(setMyTeam, index, newValue)
                            }
                          />
                        ))}
                      </div>
                    </div>

                    <div className="rounded-2xl border border-red-500/20 bg-red-950/10 p-5">
                      <h3 className="mb-4 text-sm font-black uppercase tracking-wide text-red-400">
                        Enemy Team
                      </h3>

                      <div className="grid gap-3 sm:grid-cols-2">
                        {enemyTeam.map((value, index) => (
                          <HeroInput
                            key={`enemy-team-${index}`}
                            label={`Enemy ${index + 1}`}
                            value={value}
                            heroes={heroes}
                            unavailableNames={[
                              ...enemyTeam.filter((name) => name && name !== value),
                              ...bans.filter(Boolean),
                            ]}
                            onChange={(newValue) =>
                              updateSlot(setEnemyTeam, index, newValue)
                            }
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </Panel>

                <Panel
                  title="Bans"
                  subtitle="Exclude banned heroes from recommendation results."
                >
                  <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                    {bans.map((value, index) => (
                      <HeroInput
                        key={`ban-${index}`}
                        label={`Ban ${index + 1}`}
                        value={value}
                        heroes={heroes}
                        unavailableNames={[
                          ...bans.filter((name) => name && name !== value),
                          ...myTeam.filter(Boolean),
                          ...enemyTeam.filter(Boolean),
                        ]}
                        onChange={(newValue) => updateSlot(setBans, index, newValue)}
                      />
                    ))}
                  </div>
                </Panel>
              </>
            )}
          </section>

          <aside className="rounded-2xl border border-slate-800 bg-slate-900/95 p-6 shadow-xl">
            <div className="mb-5 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-black uppercase tracking-[0.25em] text-indigo-400">
                  Results
                </p>
                <h2 className="mt-1 text-3xl font-black">Recommended Picks</h2>
              </div>

              <span className="rounded-full border border-slate-700 bg-slate-950 px-4 py-2 text-xs font-black uppercase tracking-wide text-slate-300">
                Top 5
              </span>
            </div>

            {recommendations.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-950 p-10 text-center">
                <p className="text-base font-bold text-slate-300">
                  No recommendations yet.
                </p>
                <p className="mt-2 text-sm text-slate-500">
                  Fill in the draft state and click Recommend.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {recommendations.map((recommendation, index) => (
                  <RecommendationCard
                    key={recommendation.hero}
                    recommendation={recommendation}
                    rank={index + 1}
                  />
                ))}
              </div>
            )}
          </aside>
        </div>
      </div>
    </main>
  );
}