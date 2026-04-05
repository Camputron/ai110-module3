# Model Card: Music Recommender Simulation

## 1. Model Name

> **VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests 3–5 songs from a small catalog based on a user's preferred genre, mood, energy level, and production style (acoustic vs. electronic). It is a classroom simulation designed to illustrate how content-based filtering works — it is not intended for real users or production deployment.

---

## 3. How the Model Works

The system takes a user profile (favorite genre, favorite mood, target energy, acoustic preference) and compares it against every song in the catalog. For text-based features like genre and mood, a song gets bonus points for an exact match. For numeric features like energy, the system rewards songs that are *close* to the user's target rather than just picking the highest or lowest value — so a user who wants energy 0.4 gets mellow tracks, not silence or heavy metal.

Each feature has a weight that controls how much it matters: genre counts the most (25%), followed by mood (20%) and energy (20%), then acousticness (15%), danceability (10%), and valence (10%). The scores are added up, every song gets a total, and the system returns the top 5 in order.

---

## 4. Data

The catalog contains **20 songs** in `data/songs.csv`. The original starter set had 10 songs; 10 more were added to cover underrepresented genres and moods.

**Genres represented (14):** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, electronic, r&b, country, metal, reggae, folk, latin, blues.

**Moods represented (11):** happy, chill, intense, relaxed, moody, focused, romantic, nostalgic, aggressive, melancholy, sad.

Most genres have only 1 song; lofi and pop have 2–3. The dataset reflects a Western-centric music perspective — genres like K-pop, Afrobeats, or Bollywood are absent. The numeric feature values were hand-assigned, not derived from audio analysis, so they carry the bias of whoever designed them.

---

## 5. Strengths

- **Clear-cut profiles work well.** The "High-Energy Pop" user gets Sunrise City (#1, 0.96) and Gym Hero (#2, 0.76) — exactly what a pop/happy listener would expect. The "Chill Lofi" user gets Library Rain and Midnight Coding at the top. The system nails these unambiguous cases.
- **Explanations are transparent.** Every recommendation comes with a per-feature score breakdown, so you can see *why* a song was chosen. There is no black box.
- **Cross-genre discovery still happens.** The "Deep Intense Rock" profile surfaces Gym Hero (pop) and Bass Cathedral (electronic) at #2 and #3 because they share high energy and intense mood, even though their genre doesn't match.

---

## 6. Limitations and Bias

- **Genre dominance creates a ceiling.** With genre weighted at 25%, a single genre match is worth more than a perfect energy score. For the "Conflicted: High Energy + Sad" profile, Broken Strings (blues, sad, energy 0.48) ranked #1 despite being far from the user's energy target of 0.9. The genre+mood match (0.45 combined) overwhelmed the poor energy fit (0.12). This means the system sometimes prioritizes *what* you listen to over *how* it feels.
- **Single-genre representation.** Most genres have only one song. A blues fan will always get Broken Strings at #1 regardless of their other preferences — there's no variety within the genre. This creates a filter bubble for minority genres.
- **Binary categorical matching.** "Indie pop" and "pop" are treated as completely different genres (0 match), even though a pop listener would likely enjoy indie pop. The system has no concept of genre proximity.
- **No handling of conflicting preferences.** The "High Energy + Sad" profile is a real use case (intense sad music exists — think heavy emo or dark electronic). But the system can't find these songs because the catalog links "sad" with low-energy blues. The mood labels themselves carry assumptions about what emotional states pair with what energy levels.
- **The "Middle of the Road" problem.** Users with moderate preferences (energy 0.5) see the proximity formula benefit *all* songs somewhat evenly, since most songs are within 0.5 distance. This compresses score differences and makes ranking less decisive — the gap between #1 and #5 for the R&B profile was only 0.48 points.

---

## 7. Evaluation

**Profiles tested (6):**

| Profile | Top Result | Score | Feels Right? |
|---|---|---|---|
| High-Energy Pop | Sunrise City (pop, happy, 0.82) | 0.96 | Yes — perfect match |
| Chill Lofi | Library Rain (lofi, chill, 0.35) | 0.93 | Yes — exactly the vibe |
| Deep Intense Rock | Storm Runner (rock, intense, 0.91) | 0.92 | Yes — obvious pick |
| Conflicted: High Energy + Sad | Broken Strings (blues, sad, 0.48) | 0.80 | Partially — genre/mood right, energy wrong |
| Genre Orphan (k-pop) | Sunrise City (pop, happy, 0.82) | 0.68 | Reasonable fallback, but no genre match possible |
| Middle of the Road (r&b) | Slow Honey (r&b, romantic, 0.50) | 0.90 | Yes — sole r&b track, perfect energy |

**Weight experiment:** Halving genre (0.25 to 0.125) and doubling energy (0.20 to 0.40) caused notable ranking shifts:
- For "High-Energy Pop": Fuego Lento (latin) jumped from #3 to #2, overtaking Gym Hero (pop) — energy proximity mattered more than genre loyalty.
- For "Deep Intense Rock": Gym Hero rose from #2 (0.72) to #2 (0.85) with a much tighter gap to Storm Runner — the pop genre penalty shrank.
- For "Conflicted: High Energy + Sad": Broken Strings dropped from 0.80 to 0.75 but stayed #1, while high-energy songs like Gym Hero and Fuego Lento climbed into the top 5 — the system pulled toward the energy target more strongly.

**Conclusion:** The original weights produce more genre-coherent recommendations (good for users with clear genre loyalty). The experimental weights produce more energy-coherent recommendations (good for activity-based listening like workouts or studying). Neither is universally "better."

---

## 8. Future Work

- **Genre similarity map.** Treat "indie pop" as partially matching "pop" (e.g., 0.7 instead of 0.0) to reduce harsh binary penalties.
- **Multi-context profiles.** Allow users to have multiple mood/genre preferences for different contexts (workout, study, commute).
- **Diversity constraint.** Limit the top-k to at most 2 songs from the same genre so results don't cluster.
- **Larger catalog.** 20 songs is too few for meaningful recommendations — expanding to 100+ would reduce the single-genre-representative problem.
- **Learned weights.** Instead of hand-tuning weights, use user feedback (thumbs up/down) to adjust them automatically.

---

## 9. Personal Reflection

Building this recommender made the "why" behind Spotify's Discover Weekly much more concrete. A simple weighted formula can produce surprisingly good results for clear-cut profiles, but it breaks down quickly with conflicting preferences or underrepresented genres. The biggest surprise was the "Conflicted: High Energy + Sad" profile — it exposed that my mood labels carry implicit energy assumptions (sad = slow), which is a form of bias baked into the data itself, not the algorithm.

The weight experiment showed that there is no single "correct" set of weights — the right balance depends on what the user cares about in that moment. Real systems solve this by learning personalized weights over time, which is something a static scoring formula can never do. It made me realize that the hardest part of recommendation isn't the math; it's deciding what "good" means for each individual listener.
