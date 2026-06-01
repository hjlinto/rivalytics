"use client";

/**
 * Searchable hero input for selecting allied heroes, enemy heroes, and bans.
 */

import { useMemo, useState } from "react";

import type { Hero } from "@/types/rivalytics";

type HeroInputProps = {
  label: string;
  value: string;
  heroes: Hero[];
  unavailableNames: string[];
  onChange: (value: string) => void;
};

export function HeroInput({
  label,
  value,
  heroes,
  unavailableNames,
  onChange,
}: HeroInputProps) {
  const [open, setOpen] = useState(false);

  const filteredHeroes = useMemo(() => {
    return heroes
      .filter((hero) => hero.name.toLowerCase().includes(value.toLowerCase()))
      .filter((hero) => hero.name === value || !unavailableNames.includes(hero.name))
      .slice(0, 12);
  }, [heroes, value, unavailableNames]);

  return (
    <div className="relative">
      <label className="mb-1 block text-xs font-bold uppercase tracking-wide text-slate-500">
        {label}
      </label>

      <input
        value={value}
        onChange={(event) => {
          onChange(event.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
        placeholder="Search hero..."
        className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 hover:border-slate-500 focus:border-indigo-500"
      />

      {open && filteredHeroes.length > 0 && (
        <div className="absolute z-50 mt-2 max-h-56 w-full overflow-y-auto rounded-xl border border-slate-700 bg-slate-900 shadow-2xl">
          {filteredHeroes.map((hero) => (
            <button
              key={hero.id}
              type="button"
              onMouseDown={() => {
                onChange(hero.name);
                setOpen(false);
              }}
              className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left text-sm transition hover:bg-indigo-600"
            >
              <span className="font-semibold text-white">{hero.name}</span>
              <span className="rounded-full border border-slate-700 bg-slate-950 px-2 py-1 text-xs text-slate-300">
                {hero.role}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}