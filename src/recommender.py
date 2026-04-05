import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Scoring weights (must sum to 1.0)
# ---------------------------------------------------------------------------
WEIGHTS = {
    "genre": 0.25,
    "mood": 0.20,
    "energy": 0.20,
    "acousticness": 0.15,
    "danceability": 0.10,
    "valence": 0.10,
}


@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# OOP implementation (used by tests)
# ---------------------------------------------------------------------------
class Recommender:
    """Scores and ranks songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Return (total_score, [reason_strings]) for one song."""
        score = 0.0
        reasons: List[str] = []

        # Genre match (categorical, binary)
        if song.genre == user.favorite_genre:
            score += WEIGHTS["genre"]
            reasons.append(f"genre match '{song.genre}' (+{WEIGHTS['genre']:.2f})")

        # Mood match (categorical, binary)
        if song.mood == user.favorite_mood:
            score += WEIGHTS["mood"]
            reasons.append(f"mood match '{song.mood}' (+{WEIGHTS['mood']:.2f})")

        # Energy proximity
        energy_prox = 1 - abs(song.energy - user.target_energy)
        energy_pts = WEIGHTS["energy"] * energy_prox
        score += energy_pts
        reasons.append(f"energy proximity {energy_prox:.2f} (+{energy_pts:.2f})")

        # Acousticness
        acoustic_val = song.acousticness if user.likes_acoustic else 1 - song.acousticness
        acoustic_pts = WEIGHTS["acousticness"] * acoustic_val
        score += acoustic_pts
        reasons.append(f"acousticness {acoustic_val:.2f} (+{acoustic_pts:.2f})")

        # Danceability proximity (use target_energy as rough proxy for dance preference)
        dance_prox = 1 - abs(song.danceability - user.target_energy)
        dance_pts = WEIGHTS["danceability"] * dance_prox
        score += dance_pts
        reasons.append(f"danceability proximity {dance_prox:.2f} (+{dance_pts:.2f})")

        # Valence proximity (use target_energy as rough proxy)
        valence_prox = 1 - abs(song.valence - user.target_energy)
        valence_pts = WEIGHTS["valence"] * valence_prox
        score += valence_pts
        reasons.append(f"valence proximity {valence_prox:.2f} (+{valence_pts:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score descending."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        score, reasons = self._score(user, song)
        lines = [f"Score: {score:.2f} / 1.00"]
        lines.extend(f"  - {r}" for r in reasons)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Functional implementation (used by main.py)
# ---------------------------------------------------------------------------
def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with proper numeric types."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if song["genre"] == user_prefs.get("genre"):
        score += WEIGHTS["genre"]
        reasons.append(f"genre match '{song['genre']}' (+{WEIGHTS['genre']:.2f})")

    # Mood match
    if song["mood"] == user_prefs.get("mood"):
        score += WEIGHTS["mood"]
        reasons.append(f"mood match '{song['mood']}' (+{WEIGHTS['mood']:.2f})")

    # Energy proximity
    target_energy = user_prefs.get("energy", 0.5)
    energy_prox = 1 - abs(song["energy"] - target_energy)
    energy_pts = WEIGHTS["energy"] * energy_prox
    score += energy_pts
    reasons.append(f"energy proximity {energy_prox:.2f} (+{energy_pts:.2f})")

    # Acousticness
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_val = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]
    acoustic_pts = WEIGHTS["acousticness"] * acoustic_val
    score += acoustic_pts
    reasons.append(f"acousticness {acoustic_val:.2f} (+{acoustic_pts:.2f})")

    # Danceability proximity
    dance_prox = 1 - abs(song["danceability"] - target_energy)
    dance_pts = WEIGHTS["danceability"] * dance_prox
    score += dance_pts
    reasons.append(f"danceability proximity {dance_prox:.2f} (+{dance_pts:.2f})")

    # Valence proximity
    valence_prox = 1 - abs(song["valence"] - target_energy)
    valence_pts = WEIGHTS["valence"] * valence_prox
    score += valence_pts
    reasons.append(f"valence proximity {valence_prox:.2f} (+{valence_pts:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending, return top-k as (song, score, explanation)."""
    scored = []
    for song in songs:
        total, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, total, explanation))

    # sorted() returns a new list — leaves the original `songs` list unmodified,
    # unlike .sort() which mutates in place.
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    return scored[:k]
