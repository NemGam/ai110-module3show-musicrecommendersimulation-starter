# Model Card: Music Recommender Simulation

## 1. Model Name

SignalBlend Music Recommender

## 2. Intended Use

This recommender suggests a small set of songs from a classroom-sized catalog based on a user's stated taste profile. It is designed for explainable, content-based recommendation rather than production use. The system assumes the user can describe what they like in terms of genre, mood, era, listening context, and several measurable audio-style features.

This project is for classroom exploration only. It is not trained on real listening histories and it should not be treated like a commercial music product.

## 3. How the Model Works

Each song is represented by a combination of categorical and numeric features.

Categorical features:

- `genre`
- `mood`
- `release_decade`
- `listening_context`
- `detailed_mood_tags`

Numeric features:

- `energy`
- `valence`
- `danceability`
- `acousticness`
- `tempo_bpm`
- `popularity_100`
- `vocal_presence`
- `instrumental_focus`
- `replay_value`

The model first checks whether a song matches the user's favorite categories. Genre and mood still matter, but now the recommender can also reward songs from a preferred decade, songs that fit a preferred use case like `deep_work` or `night_drive`, and songs whose detailed mood tags overlap with the user's preferred emotional descriptors.

Then it measures how close the song's numeric values are to the user's target values. A song does not need to match perfectly. It gets more credit when it is close to the target on features such as energy, tempo, popularity, or vocal presence.

Finally, the model blends the categorical score and the numeric score. The user can tune the category weights, feature weights, and the final blend between categorical and numeric matching.

Compared with the starter version, this model is richer in two ways:

- the dataset includes several new song attributes
- the scoring logic can actively use those new attributes when the user profile provides them

## 4. Data

The catalog contains 18 songs in `data/songs.csv`.

Genres represented:

- pop
- lofi
- rock
- ambient
- jazz
- synthwave
- indie pop
- hip hop
- electronic

Base moods represented:

- happy
- chill
- intense
- relaxed
- moody
- focused
- energetic

I kept the original 18-song catalog size but expanded each row with richer metadata. The added attributes are:

- `popularity_100`
- `release_decade`
- `detailed_mood_tags`
- `vocal_presence`
- `instrumental_focus`
- `listening_context`
- `replay_value`

These additions make the dataset more expressive, but the catalog is still small. Many parts of musical taste are still missing, including lyrics, language, artist similarity, instrumentation details, cultural context, and real user behavior.

## 5. Strengths

The system works best for users who can describe their taste in a structured way. It performs reasonably well when a user knows not only the genre they like, but also the kind of situation and emotional tone they want.

Examples of cases it handles better now:

- distinguishing `night_drive` synthwave from `deep_work` lofi
- separating broad mood labels from more detailed tags like `nostalgic`, `aggressive`, or `cinematic`
- matching users who want a balance between vocal-heavy and instrumental tracks
- filtering for songs that feel more mainstream or more niche using `popularity_100`

The explanations are also better because the system can point to more specific reasons for a match.

## 6. Limitations and Bias

The biggest limitation is still the dataset size. With only 18 songs, the recommender cannot offer much diversity within each niche. Some genres appear only once or twice, so a strong preference can cause the system to repeat similar choices.

Bias can also come from the hand-authored attributes:

- popularity values are synthetic, not measured from real listeners
- mood tags are subjective and reflect the dataset creator's judgment
- listening contexts like `study` or `workout` are simplified and may not generalize across people
- decade labels are coarse and may overstate the importance of era

The scoring can still overfit to whichever features receive the heaviest weights. For example, if genre and decade weights are too high, the system may ignore a better mood or tempo fit. If popularity is weighted too strongly, it may favor more mainstream-looking entries even when the user mainly cares about atmosphere.

## 7. Evaluation

I evaluated the recommender by trying profiles with different combinations of:

- favorite genres and moods
- preferred decades
- preferred listening contexts
- detailed mood tags
- numeric targets such as energy, tempo, popularity, and vocal presence

I checked whether the top recommendations were explainable and whether the reasons matched the profile. I also verified that older profiles still work, meaning the system remains backward compatible if a user only provides genre, mood, and a few numeric targets.

One useful comparison was between broad profiles and narrow profiles. Broad profiles produced more varied results, while narrow profiles often surfaced one small pocket of the dataset repeatedly. That behavior is expected for a content-based recommender with a small catalog.

## 8. Future Work

- Add more songs so each genre, decade, and context has better coverage
- Learn feature weights from user feedback instead of setting them by hand
- Add diversity rules so the top results are less repetitive
- Include artist similarity and lyrical themes
- Support negative preferences such as moods or contexts the user wants to avoid
- Use the added fields in the command-line interface so user input can control them directly

## 9. Personal Reflection

Building this made it clearer that recommendation quality depends as much on representation as on scoring. A simple scoring function can become much more useful when the data captures richer aspects of taste. It also showed how quickly bias enters the system when labels like mood, popularity, or context are hand-assigned. Even in a small classroom project, the choice of features already shapes what kinds of listeners the model serves well and which tastes it flattens.
