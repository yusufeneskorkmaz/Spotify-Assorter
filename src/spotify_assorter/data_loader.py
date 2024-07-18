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
        song_data.append({
            'track_id': track['id'],
            'track_name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'danceability': track['danceability'],
            'energy': track['energy'],
            'tempo': track['tempo'],
            'valence': track['valence'],
            'genres': sp.artist(track['artists'][0]['id'])['genres']
        })

    df = pd.DataFrame(song_data)
    if df.isnull().values.any():
        raise ValueError("Data contains NaN values. Please check the data.")
    return df
