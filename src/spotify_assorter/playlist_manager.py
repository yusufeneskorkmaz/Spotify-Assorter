import base64
import os

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
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read())
                self.sp.playlist_upload_cover_image(playlist_id, encoded_image)
        except Exception as e:
            raise RuntimeError(f"Failed to update playlist cover image: {e}")
