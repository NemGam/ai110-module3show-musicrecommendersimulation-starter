from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """Represents a song and its attributes."""
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

class Recommender:
    """Implements recommendation logic with an object-oriented interface."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns up to k recommended songs for a user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for a recommendation."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into typed dictionaries."""
    songs: List[Dict] = []
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    with open(csv_path, mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Computes a recommendation score and explanation reasons for one song."""
    # Support either singular or plural preference keys.
    favorite_genres = user_prefs.get("favorite_genres", user_prefs.get("genre", []))
    favorite_moods = user_prefs.get("favorite_moods", user_prefs.get("mood", []))

    if isinstance(favorite_genres, str):
        favorite_genres = [favorite_genres]
    if isinstance(favorite_moods, str):
        favorite_moods = [favorite_moods]

    favorite_genres = {g.lower() for g in favorite_genres}
    favorite_moods = {m.lower() for m in favorite_moods}

    song_genre = str(song.get("genre", "")).lower()
    song_mood = str(song.get("mood", "")).lower()

    genre_match = 1.0 if song_genre in favorite_genres else 0.0
    mood_match = 1.0 if song_mood in favorite_moods else 0.0
    categorical_score = (0.55 * genre_match + 0.45 * mood_match) / (0.55 + 0.45)

    def closeness(song_value: float, target_value: float, tolerance: float) -> float:
        return max(0.0, 1.0 - abs(song_value - target_value) / tolerance)

    numeric_features = [
        ("energy", ["target_energy", "energy"], 0.50, 0.30, "energy"),
        ("valence", ["target_valence", "valence"], 0.50, 0.20, "valence"),
        ("danceability", ["target_danceability", "danceability"], 0.50, 0.20, "danceability"),
        ("acousticness", ["target_acousticness", "acousticness"], 0.50, 0.15, "acousticness"),
        ("tempo_bpm", ["target_tempo_bpm", "tempo_bpm"], 40.0, 0.15, "tempo"),
    ]

    provided_numeric: List[Tuple[str, float, float, str]] = []
    for song_key, target_keys, tolerance, weight, label in numeric_features:
        target_value = None
        for key in target_keys:
            if key in user_prefs and user_prefs[key] is not None:
                target_value = float(user_prefs[key])
                break
        if target_value is not None:
            close = closeness(float(song.get(song_key, 0.0)), target_value, tolerance)
            provided_numeric.append((label, close, weight, song_key))

    numeric_weight_sum = sum(weight for _, _, weight, _ in provided_numeric)
    numeric_score = 0.0
    normalized_numeric: Dict[str, float] = {}
    numeric_closeness: Dict[str, float] = {}
    if numeric_weight_sum > 0:
        for label, close, weight, _ in provided_numeric:
            normalized_weight = weight / numeric_weight_sum
            normalized_numeric[label] = normalized_weight
            numeric_closeness[label] = close
            numeric_score += normalized_weight * close

    final_score = 0.60 * categorical_score + 0.40 * numeric_score

    reasons: List[str] = []
    genre_points = 0.60 * 0.55 * genre_match
    mood_points = 0.60 * 0.45 * mood_match
    energy_points = 0.40 * normalized_numeric.get("energy", 0.0) * numeric_closeness.get("energy", 0.0)
    valence_points = 0.40 * normalized_numeric.get("valence", 0.0) * numeric_closeness.get("valence", 0.0)
    danceability_points = 0.40 * normalized_numeric.get("danceability", 0.0) * numeric_closeness.get("danceability", 0.0)
    acousticness_points = 0.40 * normalized_numeric.get("acousticness", 0.0) * numeric_closeness.get("acousticness", 0.0)
    tempo_points = 0.40 * normalized_numeric.get("tempo", 0.0) * numeric_closeness.get("tempo", 0.0)

    if genre_match:
        reasons.append(f"genre match (+{genre_points:.3f})")
    if mood_match:
        reasons.append(f"mood match (+{mood_points:.3f})")
    if numeric_closeness.get("energy", 0.0) >= 0.70:
        reasons.append(f"energy close to target (+{energy_points:.3f})")
    if numeric_closeness.get("valence", 0.0) >= 0.70:
        reasons.append(f"valence close to target (+{valence_points:.3f})")
    if numeric_closeness.get("danceability", 0.0) >= 0.70:
        reasons.append(f"danceability close to target (+{danceability_points:.3f})")
    if numeric_closeness.get("acousticness", 0.0) >= 0.70:
        reasons.append(f"acousticness close to target (+{acousticness_points:.3f})")
    if numeric_closeness.get("tempo", 0.0) >= 0.70:
        reasons.append(f"tempo close to target (+{tempo_points:.3f})")
    if not reasons:
        reasons.append("some feature overlap (+0.000)")

    return final_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores, sorts, and returns the top-k song recommendations."""
    if k <= 0:
        return []

    scored_songs = sorted(
        (
            (song, score, "; ".join(reasons))
            for song in songs
            for score, reasons in [score_song(user_prefs, song)]
        ),
        key=lambda item: item[1],
        reverse=True,
    )

    return scored_songs[:k]
