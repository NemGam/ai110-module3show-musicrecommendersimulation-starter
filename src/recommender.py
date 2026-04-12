from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
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
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
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

    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", song.get("energy", 0.0))))
    target_valence = float(user_prefs.get("target_valence", song.get("valence", 0.0)))
    target_danceability = float(user_prefs.get("target_danceability", song.get("danceability", 0.0)))
    target_acousticness = float(user_prefs.get("target_acousticness", song.get("acousticness", 0.0)))
    target_tempo_bpm = float(user_prefs.get("target_tempo_bpm", song.get("tempo_bpm", 0.0)))

    energy_close = closeness(float(song.get("energy", 0.0)), target_energy, 0.50)
    valence_close = closeness(float(song.get("valence", 0.0)), target_valence, 0.50)
    danceability_close = closeness(float(song.get("danceability", 0.0)), target_danceability, 0.50)
    acousticness_close = closeness(float(song.get("acousticness", 0.0)), target_acousticness, 0.50)
    tempo_close = closeness(float(song.get("tempo_bpm", 0.0)), target_tempo_bpm, 40.0)

    numeric_score = (
        0.30 * energy_close
        + 0.20 * valence_close
        + 0.20 * danceability_close
        + 0.15 * acousticness_close
        + 0.15 * tempo_close
    )

    final_score = 0.60 * categorical_score + 0.40 * numeric_score

    reasons: List[str] = []
    genre_points = 0.60 * 0.55 * genre_match
    mood_points = 0.60 * 0.45 * mood_match
    energy_points = 0.40 * 0.30 * energy_close
    valence_points = 0.40 * 0.20 * valence_close
    danceability_points = 0.40 * 0.20 * danceability_close
    acousticness_points = 0.40 * 0.15 * acousticness_close
    tempo_points = 0.40 * 0.15 * tempo_close

    if genre_match:
        reasons.append(f"genre match (+{genre_points:.3f})")
    if mood_match:
        reasons.append(f"mood match (+{mood_points:.3f})")
    if energy_close >= 0.70:
        reasons.append(f"energy close to target (+{energy_points:.3f})")
    if valence_close >= 0.70:
        reasons.append(f"valence close to target (+{valence_points:.3f})")
    if danceability_close >= 0.70:
        reasons.append(f"danceability close to target (+{danceability_points:.3f})")
    if acousticness_close >= 0.70:
        reasons.append(f"acousticness close to target (+{acousticness_points:.3f})")
    if tempo_close >= 0.70:
        reasons.append(f"tempo close to target (+{tempo_points:.3f})")
    if not reasons:
        reasons.append("some feature overlap (+0.000)")

    return final_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
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
