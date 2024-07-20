import base64
import requests
from PIL import Image
import io


class PlaylistManager:
    def __init__(self, sp):
        self.sp = sp
        self.user_id = sp.current_user()['id']

    def create_playlist(self, name, description=""):
        try:
            return self.sp.user_playlist_create(self.user_id, name, description=description)
        except Exception as e:
            raise RuntimeError(f"Failed to create playlist: {e}")

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        try:
            self.sp.user_playlist_add_tracks(self.user_id, playlist_id, track_ids)
        except Exception as e:
            raise RuntimeError(f"Failed to add tracks to playlist: {e}")

    def update_playlist_cover_image(self, playlist_id, image_path):
        try:
            # Open the image and resize it to 300x300 (Spotify's recommended size)
            with Image.open(image_path) as img:
                img = img.resize((300, 300))

                # Convert the image to PNG format
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")

                # Encode the image
                encoded_image = base64.b64encode(buffered.getvalue())

                # Upload the image
                self.sp.playlist_upload_cover_image(playlist_id, encoded_image)
        except Exception as e:
            print(f"Error updating playlist cover image: {e}")
            # Instead of raising an exception, we'll just print the error and continue