import aiohttp
from PIL import Image
import io
from src.spotify_assorter.config import UNSPLASH_ACCESS_KEY

class ImageGenerator:
    def __init__(self):
        self.api_key = UNSPLASH_ACCESS_KEY
        if not self.api_key:
            raise RuntimeError("UNSPLASH_ACCESS_KEY is not set in the config file")
        self.api_url = "https://api.unsplash.com/search/photos"
        self.session = None

    async def create_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def generate_image(self, prompt: str) -> Image:
        await self.create_session()
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        params = {
            "query": prompt,
            "per_page": 1,
            "orientation": "square"
        }

        try:
            async with self.session.get(self.api_url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                if data['results']:
                    image_url = data['results'][0]['urls']['regular']
                    async with self.session.get(image_url) as image_response:
                        image_response.raise_for_status()
                        image_data = await image_response.read()
                        image = Image.open(io.BytesIO(image_data))
                        return image
                else:
                    raise RuntimeError("No images found for the given prompt")
        except aiohttp.ClientError as e:
            raise RuntimeError(f"Failed to generate image: {e}")

    async def save_image(self, image: Image, path: str) -> str:
        try:
            image.save(path)
            return path
        except Exception as e:
            raise RuntimeError(f"Failed to save the image: {e}")