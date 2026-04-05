"""CLI runner for the Music Recommender Simulation."""

import sys

from src.recommender import load_songs, recommend_songs, SCORING_MODES

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


# ---------------------------------------------------------------------------
# User profiles for evaluation
# ---------------------------------------------------------------------------
PROFILES = {
    # --- Standard profiles ---
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
        "min_popularity": 50,
        "preferred_decade": "2020s",
        "mood_tag_preferences": ["uplifting", "bright"],
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
        "likes_instrumental": True,
        "mood_tag_preferences": ["mellow", "dreamy", "calm"],
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
        "preferred_decade": "2010s",
        "mood_tag_preferences": ["powerful", "raw", "driving"],
        "likes_live": True,
    },
    # --- Adversarial / edge-case profiles ---
    "Conflicted: High Energy + Sad": {
        "genre": "blues",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": True,
        "mood_tag_preferences": ["raw", "soulful"],
    },
    "Genre Orphan: No Match": {
        "genre": "k-pop",
        "mood": "happy",
        "energy": 0.7,
        "likes_acoustic": False,
        "min_popularity": 70,
        "preferred_decade": "2020s",
    },
    "Middle of the Road": {
        "genre": "r&b",
        "mood": "romantic",
        "energy": 0.5,
        "likes_acoustic": False,
        "mood_tag_preferences": ["smooth", "warm", "sensual"],
    },
}


# ---------------------------------------------------------------------------
# Challenge 4: formatted table output
# ---------------------------------------------------------------------------
def _format_reasons(explanation: str, max_reasons: int = 3) -> str:
    """Return the top N reasons as compact lines."""
    parts = explanation.split("; ")
    # Sort by point value descending (extract the (+X.XX) part)
    def _pts(r: str) -> float:
        try:
            return float(r.rsplit("+", 1)[-1].rstrip(")"))
        except (ValueError, IndexError):
            return 0.0
    parts.sort(key=_pts, reverse=True)
    return "\n".join(parts[:max_reasons])


def run_profile_table(
    name: str, prefs: dict, songs: list, mode: str = "balanced", k: int = 5
) -> None:
    """Display recommendations as a formatted table."""
    print(f"\n{'=' * 80}")
    print(f"  Profile: {name}  |  Mode: {mode}")
    print(f"  {prefs}")
    print("=" * 80)

    results = recommend_songs(prefs, songs, k=k, mode=mode, diverse=True)

    if tabulate:
        rows = []
        for rank, (song, score, explanation) in enumerate(results, 1):
            rows.append([
                f"#{rank}",
                song["title"],
                song["artist"],
                f"{song['genre']}/{song['mood']}",
                f"{score:.2f}",
                _format_reasons(explanation),
            ])
        print(tabulate(
            rows,
            headers=["Rank", "Title", "Artist", "Genre/Mood", "Score", "Top Reasons"],
            tablefmt="rounded_grid",
            maxcolwidths=[6, 22, 16, 18, 6, 45],
        ))
    else:
        # Fallback: ASCII table
        header = f"{'#':<4} {'Title':<22} {'Artist':<16} {'Genre/Mood':<18} {'Score':<6}"
        print(header)
        print("-" * len(header))
        for rank, (song, score, explanation) in enumerate(results, 1):
            gm = f"{song['genre']}/{song['mood']}"
            print(f"#{rank:<3} {song['title']:<22} {song['artist']:<16} {gm:<18} {score:.2f}")
            top = _format_reasons(explanation, 2)
            for line in top.split("\n"):
                print(f"     {line}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Available scoring modes: {', '.join(SCORING_MODES.keys())}")

    # Pick mode from CLI arg or default to balanced
    mode = sys.argv[1] if len(sys.argv) > 1 else "balanced"
    if mode not in SCORING_MODES:
        print(f"Unknown mode '{mode}'. Using 'balanced'.")
        mode = "balanced"

    for name, prefs in PROFILES.items():
        run_profile_table(name, prefs, songs, mode=mode)


if __name__ == "__main__":
    main()
