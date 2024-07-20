import os
import argparse
import asyncio
from src.spotify_assorter.data_loader import get_spotify_client, get_liked_songs
from src.spotify_assorter.classifier import GenreClassifier
from src.spotify_assorter.playlist_manager import PlaylistManager
from src.spotify_assorter.smart_image_selector import SmartImageSelector

async def classify_songs_and_create_playlists(num_playlists):
    sp = get_spotify_client()
    liked_songs_df = get_liked_songs(sp)

    features = liked_songs_df[['danceability', 'energy', 'tempo', 'valence']]
    labels = liked_songs_df['genres'].apply(lambda x: x[0] if x else 'Unknown')

    classifier = GenreClassifier()
    accuracy = classifier.train(features, labels)

    liked_songs_df['predicted_genre'] = classifier.predict(features)

    top_genres = liked_songs_df['predicted_genre'].value_counts().nlargest(num_playlists).index

    playlist_manager = PlaylistManager(sp)
    smart_image_selector = SmartImageSelector(sp)

    created_playlists = []

    for genre in top_genres:
        playlist_name = f"{genre} Playlist"
        playlist_description = f"My favorite {genre} songs"
        playlist = playlist_manager.create_playlist(playlist_name, playlist_description)

        genre_tracks = liked_songs_df[liked_songs_df['predicted_genre'] == genre]['track_id'].tolist()
        playlist_manager.add_tracks_to_playlist(playlist['id'], genre_tracks)

        tracks = sp.playlist_tracks(playlist['id'])['items']
        image = await smart_image_selector.select_image([track['track'] for track in tracks], genre)
        image_path = f"cover_images/{genre}_playlist_cover.png"

        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)

        playlist_manager.update_playlist_cover_image(playlist['id'], image_path)

        created_playlists.append((playlist_name, len(genre_tracks), image_path))

    await smart_image_selector.close()

    return f"{num_playlists} playlists successfully created. Model Accuracy: {accuracy:.2f}", created_playlists

async def main(num_playlists):
    result, playlists = await classify_songs_and_create_playlists(num_playlists)
    print(result)
    for name, count, _ in playlists:
        print(f"- {name}: {count} tracks")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Genre Classifier and Playlist Creator")
    parser.add_argument("--num_playlists", type=int, default=5, help="Number of playlists to create")
    args = parser.parse_args()

    asyncio.run(main(args.num_playlists))