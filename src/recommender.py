import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Challenge 2: Scoring mode weight presets (Strategy pattern)
# Each mode is a dict of weights that must sum to 1.0.
# ---------------------------------------------------------------------------
SCORING_MODES = {
    "balanced": {
        "genre": 0.20,
        "mood": 0.15,
        "energy": 0.15,
        "acousticness": 0.10,
        "danceability": 0.08,
        "valence": 0.07,
        "popularity": 0.08,
        "decade": 0.07,
        "mood_tags": 0.05,
        "instrumentalness": 0.03,
        "liveness": 0.02,
    },
    "genre-first": {
        "genre": 0.40,
        "mood": 0.15,
        "energy": 0.10,
        "acousticness": 0.08,
        "danceability": 0.05,
        "valence": 0.05,
        "popularity": 0.05,
        "decade": 0.05,
        "mood_tags": 0.04,
        "instrumentalness": 0.02,
        "liveness": 0.01,
    },
    "mood-first": {
        "genre": 0.10,
        "mood": 0.30,
        "energy": 0.10,
        "acousticness": 0.08,
        "danceability": 0.07,
        "valence": 0.10,
        "popularity": 0.05,
        "decade": 0.05,
        "mood_tags": 0.10,
        "instrumentalness": 0.03,
        "liveness": 0.02,
    },
    "energy-focused": {
        "genre": 0.10,
        "mood": 0.10,
        "energy": 0.35,
        "acousticness": 0.10,
        "danceability": 0.12,
        "valence": 0.05,
        "popularity": 0.05,
        "decade": 0.03,
        "mood_tags": 0.03,
        "instrumentalness": 0.05,
        "liveness": 0.02,
    },
}

# Default mode used by the OOP Recommender class
WEIGHTS = SCORING_MODES["balanced"]

# Valid decades for proximity scoring
DECADES = ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]


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
    popularity: int
    release_decade: str
    mood_tags: List[str]
    instrumentalness: float
    liveness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Challenge 1: new preference fields with defaults for backward compatibility
    min_popularity: int = 0
    preferred_decade: str = ""
    mood_tag_preferences: List[str] = field(default_factory=list)
    likes_instrumental: bool = False
    likes_live: bool = False


# ---------------------------------------------------------------------------
# Shared scoring helpers
# ---------------------------------------------------------------------------
def _decade_proximity(song_decade: str, pref_decade: str) -> float:
    """Return 0.0–1.0 based on how close two decades are."""
    if not pref_decade or pref_decade not in DECADES:
        return 0.5  # neutral if no preference
    if song_decade not in DECADES:
        return 0.5
    dist = abs(DECADES.index(song_decade) - DECADES.index(pref_decade))
    return max(0.0, 1.0 - dist * 0.25)


def _mood_tag_overlap(song_tags: List[str], pref_tags: List[str]) -> float:
    """Return fraction of user's preferred mood tags found in the song."""
    if not pref_tags:
        return 0.5  # neutral
    matches = sum(1 for t in pref_tags if t in song_tags)
    return matches / len(pref_tags)


def _score_features(song: Dict, prefs: Dict, weights: Dict) -> Tuple[float, List[str]]:
    """Core scoring logic shared by OOP and functional paths."""
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if song["genre"] == prefs.get("genre", ""):
        score += weights["genre"]
        reasons.append(f"genre match '{song['genre']}' (+{weights['genre']:.2f})")

    # Mood match
    if song["mood"] == prefs.get("mood", ""):
        score += weights["mood"]
        reasons.append(f"mood match '{song['mood']}' (+{weights['mood']:.2f})")

    target_energy = prefs.get("energy", 0.5)

    # Energy proximity
    energy_prox = 1 - abs(song["energy"] - target_energy)
    energy_pts = weights["energy"] * energy_prox
    score += energy_pts
    reasons.append(f"energy proximity {energy_prox:.2f} (+{energy_pts:.2f})")

    # Acousticness
    likes_acoustic = prefs.get("likes_acoustic", False)
    acoustic_val = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]
    acoustic_pts = weights["acousticness"] * acoustic_val
    score += acoustic_pts
    reasons.append(f"acousticness {acoustic_val:.2f} (+{acoustic_pts:.2f})")

    # Danceability proximity
    dance_prox = 1 - abs(song["danceability"] - target_energy)
    dance_pts = weights["danceability"] * dance_prox
    score += dance_pts
    reasons.append(f"danceability proximity {dance_prox:.2f} (+{dance_pts:.2f})")

    # Valence proximity
    valence_prox = 1 - abs(song["valence"] - target_energy)
    valence_pts = weights["valence"] * valence_prox
    score += valence_pts
    reasons.append(f"valence proximity {valence_prox:.2f} (+{valence_pts:.2f})")

    # --- Challenge 1: new feature scoring ---

    # Popularity bonus (normalized 0–1)
    min_pop = prefs.get("min_popularity", 0)
    pop_norm = song["popularity"] / 100.0
    pop_score = pop_norm if min_pop > 0 else 0.5
    pop_pts = weights["popularity"] * pop_score
    score += pop_pts
    reasons.append(f"popularity {song['popularity']} (+{pop_pts:.2f})")

    # Decade proximity
    pref_decade = prefs.get("preferred_decade", "")
    decade_prox = _decade_proximity(song["release_decade"], pref_decade)
    decade_pts = weights["decade"] * decade_prox
    score += decade_pts
    if pref_decade:
        reasons.append(f"decade '{song['release_decade']}' prox {decade_prox:.2f} (+{decade_pts:.2f})")

    # Mood tag overlap
    pref_tags = prefs.get("mood_tag_preferences", [])
    song_tags = song["mood_tags"] if isinstance(song["mood_tags"], list) else song["mood_tags"].split("|")
    tag_overlap = _mood_tag_overlap(song_tags, pref_tags)
    tag_pts = weights["mood_tags"] * tag_overlap
    score += tag_pts
    if pref_tags:
        reasons.append(f"mood tags overlap {tag_overlap:.2f} (+{tag_pts:.2f})")

    # Instrumentalness
    likes_instr = prefs.get("likes_instrumental", False)
    instr_val = song["instrumentalness"] if likes_instr else 1 - song["instrumentalness"]
    instr_pts = weights["instrumentalness"] * instr_val
    score += instr_pts
    reasons.append(f"instrumentalness {instr_val:.2f} (+{instr_pts:.2f})")

    # Liveness
    likes_live = prefs.get("likes_live", False)
    live_val = song["liveness"] if likes_live else 1 - song["liveness"]
    live_pts = weights["liveness"] * live_val
    score += live_pts
    reasons.append(f"liveness {live_val:.2f} (+{live_pts:.2f})")

    return score, reasons


# ---------------------------------------------------------------------------
# Challenge 3: Diversity penalty
# ---------------------------------------------------------------------------
def _apply_diversity(
    ranked: List[Tuple[Dict, float, str]],
    k: int,
    max_per_genre: int = 2,
    max_per_artist: int = 1,
) -> List[Tuple[Dict, float, str]]:
    """Pick top-k results while limiting repeats of genre and artist."""
    result: List[Tuple[Dict, float, str]] = []
    genre_count: Dict[str, int] = {}
    artist_count: Dict[str, int] = {}

    for song, score, explanation in ranked:
        g = song["genre"]
        a = song["artist"]
        if genre_count.get(g, 0) >= max_per_genre:
            continue
        if artist_count.get(a, 0) >= max_per_artist:
            continue
        genre_count[g] = genre_count.get(g, 0) + 1
        artist_count[a] = artist_count.get(a, 0) + 1
        result.append((song, score, explanation))
        if len(result) >= k:
            break

    return result


# ---------------------------------------------------------------------------
# OOP implementation (used by tests)
# ---------------------------------------------------------------------------
class Recommender:
    """Scores and ranks songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Return (total_score, [reason_strings]) for one song."""
        song_dict = {
            "genre": song.genre, "mood": song.mood, "energy": song.energy,
            "acousticness": song.acousticness, "danceability": song.danceability,
            "valence": song.valence, "popularity": song.popularity,
            "release_decade": song.release_decade, "mood_tags": song.mood_tags,
            "instrumentalness": song.instrumentalness, "liveness": song.liveness,
        }
        prefs = {
            "genre": user.favorite_genre, "mood": user.favorite_mood,
            "energy": user.target_energy, "likes_acoustic": user.likes_acoustic,
            "min_popularity": user.min_popularity,
            "preferred_decade": user.preferred_decade,
            "mood_tag_preferences": user.mood_tag_preferences,
            "likes_instrumental": user.likes_instrumental,
            "likes_live": user.likes_live,
        }
        return _score_features(song_dict, prefs, WEIGHTS)

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
            row["popularity"] = int(row["popularity"])
            row["instrumentalness"] = float(row["instrumentalness"])
            row["liveness"] = float(row["liveness"])
            row["mood_tags"] = row["mood_tags"].split("|")
            songs.append(row)
    return songs


def score_song(
    user_prefs: Dict, song: Dict, mode: str = "balanced"
) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; return (score, reasons)."""
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    return _score_features(song, user_prefs, weights)


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diverse: bool = True,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending, return top-k with optional diversity."""
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    scored = []
    for song in songs:
        total, reasons = _score_features(song, user_prefs, weights)
        explanation = "; ".join(reasons)
        scored.append((song, total, explanation))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)

    if diverse:
        return _apply_diversity(scored, k)
    return scored[:k]
