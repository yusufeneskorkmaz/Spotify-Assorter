import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io

class ImageGenerator:
    def __init__(self):
        try:
            self.stability_api = client.StabilityInference(
                key=os.environ['STABILITY_API_KEY'],  # Use environment variable
                verbose=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Stability API: {e}")

    def generate_image(self, prompt: str) -> Image:
        try:
            answers = self.stability_api.generate(
                prompt=prompt,
                seed=992446758,
                steps=30,
                cfg_scale=8.0,
                width=512,
                height=512,
                samples=1,
                sampler=generation.SAMPLER_K_DPMPP_2M
            )
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                        return img
        except Exception as e:
            raise RuntimeError(f"Failed to generate image: {e}")

    def save_image(self, image: Image, path: str) -> str:
        try:
            image.save(path)
        except Exception as e:
            raise RuntimeError(f"Failed to save the image: {e}")
        return path