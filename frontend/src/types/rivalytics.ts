/**
 * Shared frontend types for Rivalytics.
 */

export type Hero = {
  id: number;
  name: string;
  role: string;
};

export type Recommendation = {
  hero: string;
  role: string;
  tier?: string;
  score: number;
  win_rate: number;
  pick_rate: number;
  ban_rate: number;
  matches_played?: number;
  base_score: number;
  teamup_score: number;
};