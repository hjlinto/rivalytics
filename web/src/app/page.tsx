"use client";

import { useEffect, useState } from "react";

type Hero = {
  name: string;
  role: string;
};

export default function Home() {
  const [heroes, setHeroes] = useState<Hero[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/heroes")
      .then((res) => res.json())
      .then((data => {
        setHeroes(data.heroes ?? []);
      }))
      .catch(console.error);
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <h1>Marvel Rivals Meta Tracker</h1>

      <ul>
        {heroes.map((h) => (
          <li key={h.name}>
            {h.name} — {h.role}
          </li>
        ))}
      </ul>
    </main>
  );
}
