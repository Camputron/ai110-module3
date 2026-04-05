# Reflection: Profile Comparisons

## High-Energy Pop vs. Chill Lofi

These two profiles produce completely non-overlapping top 5 lists. The pop profile leads with Sunrise City (0.96) — a bright, upbeat track — while the lofi profile leads with Library Rain (0.93) — a mellow, acoustic study track. This makes sense because the profiles differ on all four axes: genre (pop vs. lofi), mood (happy vs. chill), energy (0.8 vs. 0.4), and acoustic preference (electronic vs. acoustic). The system has no trouble telling these listeners apart, which confirms that four preference dimensions are enough to separate clearly distinct tastes.

## Deep Intense Rock vs. High-Energy Pop

Both profiles target high energy (0.9 and 0.8), yet their top results barely overlap. Storm Runner dominates the rock profile at #1 (0.92), but doesn't even appear in the pop top 5. Meanwhile, Sunrise City is #1 for pop (0.96) but drops to #4 for rock (0.49). Genre is doing the heavy lifting here — without it, both profiles would converge on the same cluster of high-energy songs. This shows why genre carries the highest weight: it prevents the system from treating all energetic listeners as interchangeable.

## Conflicted Profile (High Energy + Sad) vs. Chill Lofi

The conflicted profile asks for blues, sad mood, and energy 0.9 — a combination that doesn't naturally exist in the catalog (Broken Strings is blues/sad but only 0.48 energy). Broken Strings still wins at #1 (0.80) because genre+mood together (0.45) outweigh the energy penalty. Compared to the Chill Lofi profile, which gets near-perfect matches across all features, the conflicted profile exposes how the system handles tension between categorical and numeric preferences. It prioritizes "what kind of music" over "how it should feel," which may not be the right call for someone who wants intense, emotionally heavy music.

## Genre Orphan (K-pop) vs. High-Energy Pop

The k-pop profile can never get a genre match (no k-pop songs exist in the catalog), so it loses 0.25 points on every song. Its top result, Sunrise City (0.68), is the same as the pop profile's #1 — but scores 0.28 points lower because of the missing genre bonus. This reveals how the system degrades gracefully for unknown genres: it falls back on mood, energy, and production style. But it also means k-pop fans are silently funneled toward pop music, which could feel like erasure if this were a real product.

## Middle of the Road (R&B) vs. Deep Intense Rock

The R&B profile (energy 0.5) and rock profile (energy 0.9) sit at opposite ends of the energy spectrum. Slow Honey leads for R&B with a near-perfect 0.90 — it's the only r&b track so genre+mood lock it in. For rock, Storm Runner leads at 0.92. What's interesting is the score gap between #1 and #5: it's 0.48 for R&B but only 0.44 for rock. The moderate energy target (0.5) compresses scores because most songs fall within a reasonable distance, while the extreme target (0.9) creates sharper separation. Moderate preferences are harder for the system to rank decisively.
