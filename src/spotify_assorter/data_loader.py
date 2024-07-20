import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from src.spotify_assorter.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI


def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-library-read playlist-modify-public playlist-modify-private ugc-image-upload"
    ))
    return sp


def get_liked_songs(sp):
    results = sp.current_user_saved_tracks()
    if 'items' not in results or len(results['items']) == 0:
        raise ValueError("No liked songs found.")

    tracks = results['items']
    song_data = []

    for item in tracks:
        track = item['track']
        track_id = track['id']

        # Get audio features for the track
        audio_features = sp.audio_features(track_id)[0]

        if audio_features:
            song_data.append({
                'track_id': track_id,
                'track_name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'release_date': track['album']['release_date'],
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'key': audio_features['key'],
                'loudness': audio_features['loudness'],
                'mode': audio_features['mode'],
                'speechiness': audio_features['speechiness'],
                'acousticness': audio_features['acousticness'],
                'instrumentalness': audio_features['instrumentalness'],
                'liveness': audio_features['liveness'],
                'valence': audio_features['valence'],
                'tempo': audio_features['tempo'],
                'duration_ms': audio_features['duration_ms'],
                'time_signature': audio_features['time_signature'],
                'genres': sp.artist(track['artists'][0]['id'])['genres']
            })

    df = pd.DataFrame(song_data)
    if df.empty:
        raise ValueError("No valid audio features found for any tracks.")
    if df.isnull().values.any():
        print("Warning: Some tracks have missing audio features.")
    return df