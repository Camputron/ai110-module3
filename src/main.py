"""CLI runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default user profile: upbeat pop listener
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    print(f"\nUser profile: {user_prefs}\n")
    print("=" * 60)
    print("  Top 5 Recommendations")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f} / 1.00")
        for reason in explanation.split("; "):
            print(f"         - {reason}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
