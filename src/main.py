"""CLI runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


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
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles ---
    "Conflicted: High Energy + Sad": {
        "genre": "blues",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": True,
    },
    "Genre Orphan: No Match": {
        "genre": "k-pop",
        "mood": "happy",
        "energy": 0.7,
        "likes_acoustic": False,
    },
    "Middle of the Road": {
        "genre": "r&b",
        "mood": "romantic",
        "energy": 0.5,
        "likes_acoustic": False,
    },
}


def run_profile(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    """Run and display recommendations for a single user profile."""
    print(f"\n{'=' * 60}")
    print(f"  Profile: {name}")
    print(f"  {prefs}")
    print("=" * 60)

    recommendations = recommend_songs(prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f} / 1.00")
        for reason in explanation.split("; "):
            print(f"         - {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
