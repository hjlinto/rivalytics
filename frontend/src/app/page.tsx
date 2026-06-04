"use client";

/**
 * Rivalytics home page.
 *
 * Owns the recommendation workflow:
 * - loading heroes
 * - tracking draft state
 * - requesting top 3 recommendations per role
 * - composing the dashboard layout
 */

import { useEffect, useState } from "react";
import type { Dispatch, SetStateAction } from "react";

import { HeroInput } from "./_components/HeroInput";
import { Panel } from "./_components/Panel";
import { RecommendationCard } from "./_components/RecommendationCard";
import type { Hero, Recommendation } from "@/types/rivalytics";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

const RECOMMENDATION_ROLES = ["Vanguard", "Duelist", "Strategist"] as const;

type RecommendationRole = (typeof RECOMMENDATION_ROLES)[number];

type GroupedRecommendations = Record<RecommendationRole, Recommendation[]>;

function createEmptyRecommendations(): GroupedRecommendations {
  return {
    Vanguard: [],
    Duelist: [],
    Strategist: [],
  };
}

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

async function fetchWithRetry(
  url: string,
  options?: RequestInit,
  retries = 3,
  delayMs = 500
): Promise<Response> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < retries; attempt += 1) {
    try {
      const response = await fetch(url, options);

      if (response.ok) {
        return response;
      }

      lastError = new Error(`Request failed with status ${response.status}`);
    } catch (error) {
      lastError = error as Error;
    }

    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  throw lastError ?? new Error("Request failed.");
}

export default function Home() {
  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [myTeam, setMyTeam] = useState<string[]>(["", "", "", "", ""]);
  const [enemyTeam, setEnemyTeam] = useState<string[]>(["", "", "", "", "", ""]);
  const [bans, setBans] = useState<string[]>(["", "", "", ""]);
  const [recommendations, setRecommendations] =
    useState<GroupedRecommendations>(createEmptyRecommendations);
  const [loadingHeroes, setLoadingHeroes] = useState(false);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchHeroes() {
      try {
        setLoadingHeroes(true);
        setError("");

        const response = await fetchWithRetry(`${API_BASE_URL}/heroes`);
        const data = await response.json();

        setHeroes(data.heroes ?? []);
      } catch {
        setError("Could not load hero data. Please refresh the page and try again.");
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

  async function fetchRecommendationsForRole(
    role: RecommendationRole
  ): Promise<Recommendation[]> {
    const payload = {
      my_team: cleanTeam(myTeam),
      enemy_team: cleanTeam(enemyTeam),
      bans: cleanTeam(bans),
      role_needed: role,
      top_n: 3,
    };

    const response = await fetchWithRetry(`${API_BASE_URL}/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    return data.recommendations ?? [];
  }

  async function getRecommendations() {
    try {
      setLoadingRecommendations(true);
      setError("");

      const groupedResults = await Promise.all(
        RECOMMENDATION_ROLES.map(async (role) => {
          const roleRecommendations = await fetchRecommendationsForRole(role);

          return [role, roleRecommendations] as const;
        })
      );

      setRecommendations(Object.fromEntries(groupedResults) as GroupedRecommendations);
    } catch {
      setError("Could not fetch recommendations. Please try again.");
      setRecommendations(createEmptyRecommendations());
    } finally {
      setLoadingRecommendations(false);
    }
  }

  function clearDraft() {
    setMyTeam(["", "", "", "", ""]);
    setEnemyTeam(["", "", "", "", "", ""]);
    setBans(["", "", "", ""]);
    setRecommendations(createEmptyRecommendations());
    setError("");
  }

  const hasRecommendations = RECOMMENDATION_ROLES.some(
    (role) => recommendations[role].length > 0
  );

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto w-full max-w-[1600px] px-6 py-10">
        <header className="mb-8 grid gap-6 lg:grid-cols-[1.5fr_auto] lg:items-end">
          <div>
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.25em] text-indigo-400">
              Rivalytics
            </p>
            <h1 className="max-w-5xl text-4xl font-black tracking-tight text-white md:text-5xl">
              Marvel Rivals draft recommendations by role.
            </h1>
            <p className="mt-4 max-w-3xl text-base leading-7 text-slate-400">
              Select allied picks, enemy picks, and bans, then generate the top
              Vanguard, Duelist, and Strategist recommendations using meta data
              and team-up synergy.
            </p>
          </div>

          <div className="flex flex-wrap gap-3 lg:justify-end">
            <button
              type="button"
              onClick={getRecommendations}
              disabled={loadingHeroes || loadingRecommendations}
              className="h-12 rounded-xl bg-indigo-600 px-7 text-sm font-black uppercase tracking-wide text-white shadow-lg shadow-indigo-950/40 transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loadingRecommendations ? "Generating..." : "Recommend"}
            </button>

            <button
              type="button"
              onClick={clearDraft}
              className="h-12 rounded-xl border border-slate-700 bg-slate-900 px-7 text-sm font-black uppercase tracking-wide text-slate-300 transition hover:bg-slate-800"
            >
              Clear Draft
            </button>
          </div>
        </header>

        {error && (
          <div className="mb-6 rounded-2xl border border-red-500/60 bg-red-950/60 px-5 py-4 text-sm font-semibold text-red-200">
            {error}
          </div>
        )}

        <section className="mb-8 grid gap-6 xl:grid-cols-2">
          <Panel
            title="Allied Team"
            subtitle="Heroes already selected by your team are excluded from recommendations."
          >
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
                  onChange={(newValue) => updateSlot(setMyTeam, index, newValue)}
                />
              ))}
            </div>
          </Panel>

          <Panel
            title="Enemy Team"
            subtitle="Enemy picks are draft context. Mirror picks remain eligible unless banned."
          >
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
                  onChange={(newValue) => updateSlot(setEnemyTeam, index, newValue)}
                />
              ))}
            </div>
          </Panel>
        </section>

        <section className="mb-10">
          <Panel
            title="Bans"
            subtitle="Banned heroes are removed from all role recommendation groups."
          >
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
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
        </section>

        <section>
          <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="mb-2 text-sm font-semibold uppercase tracking-[0.25em] text-indigo-400">
                Recommendations
              </p>
              <h2 className="text-3xl font-black tracking-tight text-white">
                Top picks by position
              </h2>
            </div>
          </div>

          {!hasRecommendations ? (
            <section className="rounded-3xl border border-dashed border-slate-700 bg-slate-900/70 p-12 text-center shadow-xl">
              <h3 className="text-xl font-black text-white">
                No recommendations yet
              </h3>
              <p className="mt-2 text-sm text-slate-400">
                Build the draft state above, then click Recommend.
              </p>
            </section>
          ) : (
            <div className="grid gap-6 xl:grid-cols-3">
              {RECOMMENDATION_ROLES.map((role) => (
                <section
                  key={role}
                  className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5 shadow-xl"
                >
                  <div className="mb-4 flex items-center justify-between">
                    <h3 className="text-xl font-black text-white">{role}</h3>
                    <span className="rounded-full border border-slate-700 bg-slate-950 px-3 py-1 text-xs font-black uppercase tracking-wide text-slate-400">
                      Top 3
                    </span>
                  </div>

                  {recommendations[role].length === 0 ? (
                    <div className="rounded-2xl border border-slate-800 bg-slate-950 p-6 text-sm text-slate-500">
                      No eligible {role.toLowerCase()} recommendations.
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {recommendations[role].map((recommendation, index) => (
                        <RecommendationCard
                          key={`${role}-${recommendation.hero}`}
                          recommendation={recommendation}
                          rank={index + 1}
                        />
                      ))}
                    </div>
                  )}
                </section>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}