import aiohttp
from PIL import Image
import io
import os
from urllib.parse import quote

class ImageGenerator:
    def __init__(self):
        self.api_key = os.getenv('UNSPLASH_ACCESS_KEY')
        self.session = aiohttp.ClientSession()

    def sanitize_query(self, query):
        # Remove any characters that are not alphanumeric or spaces
        return ' '.join(''.join(char for char in word if char.isalnum()) for word in query.split())

    async def generate_image(self, prompt):
        try:
            sanitized_prompt = self.sanitize_query(prompt)
            encoded_prompt = quote(sanitized_prompt)
            url = f"https://api.unsplash.com/search/photos?query={encoded_prompt}&per_page=1&orientation=square"
            headers = {"Authorization": f"Client-ID {self.api_key}"}

            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

            if 'results' in data and len(data['results']) > 0:
                image_url = data['results'][0]['urls']['regular']
                async with self.session.get(image_url) as img_response:
                    img_response.raise_for_status()
                    img_data = await img_response.read()
                    return Image.open(io.BytesIO(img_data))
            else:
                print("No image found, returning default image.")
                return self.default_image()
        except Exception as e:
            print(f"Error generating image: {e}")
            return self.default_image()

    def default_image(self):
        # Return a default image or a blank image
        return Image.new('RGB', (500, 500), color='grey')

    async def close_session(self):
        await self.session.close()