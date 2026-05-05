"use client";

import { useEffect, useMemo, useState } from "react";

type Hero = {
  id: number;
  name: string;
  role: string;
};

type Recommendation = {
  hero: string;
  role: string;
  tier: string;
  win_rate: number;
  pick_rate: number;
  ban_rate: number;
  base_score: number;
  teamup_score: number;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
/**
 * Reusable input component for selecting a hero.
 * Feature:
 * - Searchable input with dropdown of matching heroes
 */
function HeroInput({
  label,
  value,
  heroes,
  takenNames,
  onChange,
}: {
  label: string;
  value: string;
  heroes: Hero[];
  takenNames: string[];
  onChange: (value: string) => void;
}) {
  const [open, setOpen] = useState(false);
/**
 * Filter heroes based on current search input
 */
  const filtered = heroes
    .filter((h) => h.name.toLowerCase().includes(value.toLowerCase()))

  return (
    <div className="relative">
      <label className="mb-1 block text-sm text-zinc-400">{label}</label>

      <input
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 100)}
        placeholder="Type hero..."
        className="w-full rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2 text-white outline-none focus:border-indigo-400"
      />

      {open && filtered.length > 0 && (
        <div className="absolute z-50 mt-1 max-h-48 w-full overflow-y-auto rounded-lg border border-zinc-700 bg-zinc-900">
          {filtered.map((hero) => (
            <div
              key={hero.id}
              onMouseDown={() => {
                onChange(hero.name);
                setOpen(false);
              }}
              className="cursor-pointer px-3 py-2 hover:bg-indigo-600"
            >
              {hero.name}
              <span className="ml-2 text-xs text-zinc-400">
                ({hero.role})
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function Home() {
  const [heroes, setHeroes] = useState<Hero[]>([]);

  const [myTeam, setMyTeam] = useState<string[]>(["", "", "", "", ""]);
  const [enemyTeam, setEnemyTeam] = useState<string[]>([
    "",
    "",
    "",
    "",
    "",
    "",
  ]);
  const [bans, setBans] = useState<string[]>(["", "", "", ""]);

  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loadingHeroes, setLoadingHeroes] = useState(false);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    /**
     * Fetch hero list from backend API and handle loading/error states
     */
    async function fetchHeroes() {
      try {
        setLoadingHeroes(true);
        setError("");

        const res = await fetch(`${API_BASE_URL}/heroes`);

        if (!res.ok) {
          throw new Error("Failed to fetch heroes");
        }

        const data = await res.json();

        // Backend should return { heroes: Hero[] }, but default to empty array if not present
        setHeroes(data.heroes ?? []);
      } catch (err) {
        setError("Could not load heroes. Make sure your backend is running.");
        setHeroes([]);
      } finally {
        setLoadingHeroes(false);
      }
    }

    fetchHeroes();
  }, []);

  const heroNames = heroes.map((hero) => hero.name);

  const selectedNames = [...myTeam, ...enemyTeam, ...bans].filter(Boolean);

  /**
   * Updates a specific index in a team/bans array
   * Used for controlled inputs
   */
  function updateSlot(
    setter: React.Dispatch<React.SetStateAction<string[]>>,
    index: number,
    value: string
  ) {
    setter((current) => {
      const copy = [...current];
      copy[index] = value;
      return copy;
    });
  }

  /**
   * Removes empty/invalid entries before sending to backend.
   */
  function cleanTeam(values: string[]) {
    return values.filter((name) => name.trim() !== "" && heroNames.includes(name));
  }

  /** 
   * Calls backend recommendation engine with current team comps and bans, then updates recommendations state with results 
   */
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

      const res = await fetch(`${API_BASE_URL}/recommend`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch recommendations");
      }

      const data = await res.json();
      console.log("Recommendations response:", data);
      setRecommendations(data.recommendations ?? []);
    } catch (err) {
      setError("Could not get recommendations.");
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
    <main className="min-h-screen bg-zinc-950 p-8 text-white">
      <div className="mx-auto max-w-7xl space-y-8">
        <section>
          <h1 className="text-4xl font-bold">Marvel Rivals Meta Tracker</h1>
          <p className="mt-2 text-zinc-400">
            Enter your team, the enemy team, and bans to get ranked hero
            recommendations.
          </p>
        </section>

        {error && (
          <div className="rounded-lg border border-red-500 bg-red-950 p-4 text-red-200">
            {error}
          </div>
        )}

        {loadingHeroes ? (
          <p className="text-zinc-400">Loading heroes...</p>
        ) : (
          <section className="grid gap-6 lg:grid-cols-3">
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
              <h2 className="mb-4 text-2xl font-semibold">My Team</h2>

              <div className="space-y-3">
                {myTeam.map((value, index) => (
                  <HeroInput
                    key={`my-team-${index}`}
                    label={`Teammate ${index + 1}`}
                    value={value}
                    heroes={heroes}
                    takenNames={selectedNames.filter((name) => name !== value)}
                    onChange={(newValue) =>
                      updateSlot(setMyTeam, index, newValue)
                    }
                  />
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
              <h2 className="mb-4 text-2xl font-semibold">Enemy Team</h2>

              <div className="space-y-3">
                {enemyTeam.map((value, index) => (
                  <HeroInput
                    key={`enemy-team-${index}`}
                    label={`Enemy ${index + 1}`}
                    value={value}
                    heroes={heroes}
                    takenNames={selectedNames.filter((name) => name !== value)}
                    onChange={(newValue) =>
                      updateSlot(setEnemyTeam, index, newValue)
                    }
                  />
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
              <h2 className="mb-4 text-2xl font-semibold">Bans</h2>

              <div className="space-y-3">
                {bans.map((value, index) => (
                  <HeroInput
                    key={`ban-${index}`}
                    label={`Ban ${index + 1}`}
                    value={value}
                    heroes={heroes}
                    takenNames={selectedNames.filter((name) => name !== value)}
                    onChange={(newValue) => updateSlot(setBans, index, newValue)}
                  />
                ))}
              </div>
            </div>
          </section>
        )}

        <section className="flex flex-wrap gap-3">
          <button
            onClick={getRecommendations}
            disabled={loadingRecommendations || loadingHeroes}
            className="rounded-lg bg-indigo-600 px-5 py-3 font-medium hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loadingRecommendations ? "Getting recommendations..." : "Recommend"}
          </button>

          <button
            onClick={clearDraft}
            className="rounded-lg border border-zinc-700 px-5 py-3 font-medium text-zinc-300 hover:bg-zinc-900"
          >
            Clear
          </button>
        </section>

        {recommendations.length > 0 && (
          <section>
            <h2 className="mb-4 text-2xl font-semibold">Recommendations</h2>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recommendations.map((rec, index) => (
                <div
                  key={rec.hero}
                  className="rounded-xl border border-zinc-800 bg-zinc-900 p-4"
                >
                  <p className="text-sm text-zinc-500">Rank #{index + 1}</p>
                  <h3 className="mt-1 text-xl font-bold">{rec.hero}</h3>
                  <p className="text-zinc-400">{rec.role}</p>

                  <div className="mt-4 space-y-1 text-sm text-zinc-300">
                    <p>Win Rate: {rec.win_rate}</p>
                    <p>Pick Rate: {rec.pick_rate}</p>
                    <p>Ban Rate: {rec.ban_rate}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}