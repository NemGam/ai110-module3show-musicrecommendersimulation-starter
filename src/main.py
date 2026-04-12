"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"\nLoaded {len(songs)} songs")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("Top recommendations")
    print("=" * 72)

    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        reason_parts = [part.strip() for part in explanation.split(";") if part.strip()]
        title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        genre = song.get("genre", "unknown")
        mood = song.get("mood", "unknown")

        print(f"{idx}. {title} - {artist}")
        print(f"   Score : {score:.3f}")
        print(f"   Tags  : genre={genre}, mood={mood}")
        print("   Why   :")
        for reason in reason_parts:
            print(f"     - {reason}")
        print("-" * 72)


if __name__ == "__main__":
    main()
