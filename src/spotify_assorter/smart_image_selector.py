import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from src.spotify_assorter.image_generator import ImageGenerator
import asyncio
import aiohttp
from functools import lru_cache

class SmartImageSelector:
    def __init__(self, sp):
        self.sp = sp
        self.image_generator = ImageGenerator()
        self.vectorizer = TfidfVectorizer()
        self.session = aiohttp.ClientSession()

    async def get_track_features(self, track):
        try:
            async with self.session.get(f"https://api.spotify.com/v1/audio-features/{track['id']}") as resp:
                audio_features = await resp.json()
            async with self.session.get(f"https://api.spotify.com/v1/artists/{track['artists'][0]['id']}") as resp:
                artist = await resp.json()

            return {
                'energy': audio_features.get('energy', 0),
                'valence': audio_features.get('valence', 0),
                'danceability': audio_features.get('danceability', 0),
                'genres': ' '.join(artist.get('genres', [])),
                'name': track.get('name', ''),
                'artist': track['artists'][0].get('name', '') if track.get('artists') else ''
            }
        except Exception as e:
            print(f"Error getting features for track {track.get('id', 'unknown')}: {str(e)}")
            return None

    async def get_playlist_features(self, tracks):
        tasks = [self.get_track_features(track) for track in tracks[:min(len(tracks), 20)]]  # Limit to 20 tracks
        features = await asyncio.gather(*tasks)
        return [feature for feature in features if feature is not None]

    @lru_cache(maxsize=100)
    def generate_smart_prompt(self, genre, avg_energy, avg_valence, avg_danceability, important_words_tuple):
        mood = "energetic" if avg_energy > 0.6 else "calm"
        mood += " happy" if avg_valence > 0.6 else " melancholic"
        style = "danceable" if avg_danceability > 0.6 else "ambient"
        return f"{mood} {style} {genre} music {' '.join(important_words_tuple[:3])}"  # Limit to 3 important words

    async def select_image(self, tracks, genre):
        features = await self.get_playlist_features(tracks)

        if not features:
            print(f"Warning: No valid features found for genre {genre}")
            return self.image_generator.default_image()

        avg_energy = np.mean([f['energy'] for f in features])
        avg_valence = np.mean([f['valence'] for f in features])
        avg_danceability = np.mean([f['danceability'] for f in features])

        text = ' '.join([f"{f['genres']} {f['name']} {f['artist']}" for f in features])
        tfidf = self.vectorizer.fit_transform([text])
        important_words = [word for word, _ in
                           sorted(zip(self.vectorizer.get_feature_names_out(), tfidf.toarray()[0]), key=lambda x: x[1],
                                  reverse=True)[:5]]

        # Convert list to tuple for caching
        important_words_tuple = tuple(important_words)

        prompt = self.generate_smart_prompt(genre, avg_energy, avg_valence, avg_danceability, important_words_tuple)
        return await self.image_generator.generate_image(prompt)

    async def close(self):
        await self.session.close()
        await self.image_generator.close_session()