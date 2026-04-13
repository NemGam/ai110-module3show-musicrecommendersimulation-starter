# Model Card: Music Recommender Simulation

## 1. Model Name

VibeFlow 1.0

## 2. Goal

This recommender suggests a small set of songs from a classroom-sized catalog based on a user's stated taste profile. It is designed for explainable, content-based recommendation rather than production use. The system assumes the user can describe what they like in terms of genre, mood, era, listening context, and several measurable audio-style features.

This project is for classroom exploration only. It is not trained on real listening histories and it should not be treated like a commercial music product.

## 3. Data Used

The catalog contains 18 songs in `data/songs.csv`.

Genres represented:

- pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, electronic

Base moods represented:

- happy, chill, intense, relaxed, moody, focused, energetic

I kept the original 18-song catalog size but expanded each row with richer metadata. The added attributes are:

- `popularity_100`
- `release_decade`
- `detailed_mood_tags`
- `vocal_presence`
- `instrumental_focus`
- `listening_context`
- `replay_value`

These additions make the dataset more expressive, but the catalog is still small. Many parts of musical taste are still missing, including lyrics, language, artist similarity, instrumentation details, cultural context, and real user behavior.

## 4. Algorithm Summary

The recommender gives every song a score based on how well it matches the user's taste profile.

One part of the score comes from category matches. A song gets points when it matches the user's preferred genre, mood, decade, listening context, or detailed mood tags.

Another part of the score comes from feature closeness. A song earns more points when its energy, tempo, popularity, vocal presence, instrumental focus, and similar traits are close to the user's target values.

These points are added together into one final score. Songs with higher scores are treated as better matches, so they appear closer to the top of the recommendation list.

## 5. Observed Behavior / Biases

The system works best for users who can describe their taste in a structured way. It performs reasonably well when a user knows not only the genre they like, but also the kind of situation and emotional tone they want.

The main issue I found is that partial-profile users are strongly under-scored because genre and mood are always kept in the categorical denominator even when the user did not provide them, and the numeric blend stays active even when no numeric prefs were given. In score_song, active_category_features always starts with genre and mood, and the final blend always uses 55% categorical / 45% numeric. 

Result: a context-only user can max out at about 0.073, a mood-only user at about 0.212, and a genre-only user at about 0.338. That means users who express fewer preference types are effectively treated as weak-signal users even when their one stated preference matches perfectly.

## 6. Evaluation

I evaluated the recommender by trying profiles with different combinations of:

- favorite genres and moods
- preferred decades
- preferred listening contexts
- detailed mood tags
- numeric targets such as energy, tempo, popularity, and vocal presence

The five main user profiles I tested were:

- `Late Night Coder`, which preferred lofi and ambient music for `study` and `deep_work` with low energy, high acousticness, and strong instrumental focus
- `Night Drive Mood`, which targeted synthwave, electronic, and rock for `night_drive` with moody, cinematic tags and higher energy and danceability
- `Weekend Pop Boost`, which favored pop and indie pop for `party`, `commute`, and `walk` with high valence, popularity, and replay value
- `Quiet Morning Reader`, which leaned toward jazz, ambient, and lofi for `reading`, `cafe`, and `sleep` with gentle low-tempo, acoustic, instrumental songs
- `Genre First Explorer`, which mostly specified hip hop and rock plus focused and intense moods, with fewer supporting preferences than the other profiles

I checked whether the top recommendations were explainable and whether the reasons matched the profile.

One useful comparison was between broad profiles and narrow profiles. Broad profiles produced more varied results, while narrow profiles often surfaced one small pocket of the dataset repeatedly. That behavior is expected for a content-based recommender with a small catalog.

One surprising result was that the richer profiles behaved as expected, but the more partial `Genre First Explorer` profile exposed a scoring weakness: because the denominator still assumes genre, mood, and numeric structure even when some preferences are missing, partial-profile users are under-scored compared with fully specified users. Another small surprise was how much overlap appeared between `Late Night Coder` and `Quiet Morning Reader`; even though their use cases differ, the shared low-energy, instrumental, and acoustic targets made parts of their recommendation lists converge.

## 7. Intended Use and Non-Intended Use

This project is for classroom exploration only. It is not trained on real listening histories and it should not be treated like a commercial music product.

All song names and authors, as well as parameters of those songs are generated using Copilot.
Any resemblance to actual names or persons is coincidental.


## 8. Future Work

- Add more songs so each genre, decade, and context has better coverage
- Learn feature weights from user feedback instead of setting them by hand
- Include artist similarity and lyrical themes
- Support negative preferences such as moods or contexts the user wants to avoid
- Use the added fields in the command-line interface so user input can control them directly

## 9. Personal Reflection

I really enjoyed building this project. I've learned a lot about song recommendation systems (real-life systems are way more complex) and there is still a lot to learn. The biggest moment of learning for me was how complex these systems are. While my system uses 7-8 parameters with simple math and blending, real systems will try to actually calculate user's profile from what they listen and not just preset values.

It also showed how quickly bias enters the system when labels like mood, popularity, or context are hand-assigned. Even in a small classroom project, the choice of features already shapes what kinds of listeners the model serves well and which tastes it flattens.

I would like to add an actual system in place to calculate users' preferences from what they listen and not just a bunch of fields.
