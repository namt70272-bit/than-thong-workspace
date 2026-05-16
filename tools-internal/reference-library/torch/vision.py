import os
from PIL import Image
from io import BytesIO
import requests
from urllib.parse import urlparse

from .agent import Agent
from ..model import Model

from ..utils import read_config

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# This is a temporary placeholder for a full-fledged Vision-Language Model (VLM).
# BLIP is used here only to simulate basic image-to-text generation functionality.
# Replace with a real VLM (e.g., BLIP-2, MiniGPT-4, Gemini, GPT-4V, etc.) when available.
class BLIPModel:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.vision = True
        self.device = device
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)

    def process_image(self, task: str, image: Image.Image) -> str:
        inputs = self.processor(image, task, return_tensors="pt").to(self.device)
        with torch.no_grad():
            output = self.model.generate(**inputs)
        return self.processor.decode(output[0], skip_special_tokens=True)



class Vision(Agent):
    """
    a vision agent should able to visually watch something
    in the base case it can watch video or photos provides by the user
    """
    def __init__(self, model: Model, db="./local_files"):
        self.model = model
        config = read_config()
        self.db = config.get("db", db)

    def _load_image(self, source: str) -> Image.Image:
        """Load image from a file path or URL."""
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source, timeout=5)
            img = Image.open(BytesIO(response.content))
        elif os.path.isfile(source):
            img = Image.open(source)
        else:
            raise ValueError("Invalid image source path or URL.")
        return img.convert("RGB")

    async def run(self, task: str, data: list[dict]):
        """
        Process a list of image items. Each image is saved locally, then a textual
        prompt describing the task and image path is passed to model.completion().
        """
        if not hasattr(self.model, "vision") or not self.model.vision:
            raise ValueError("Model does not support vision tasks.")

        results = []
        output_dir = os.path.join(self.db, "vision_outputs")
        os.makedirs(output_dir, exist_ok=True)

        for item in data:
            url = item.get("url")
            if not isinstance(url, str):
                raise ValueError("Each data item must contain a string 'url' field.")

            try:
                image = self._load_image(url)
            except Exception as e:
                raise RuntimeError(f"Failed to load image: {e}")

            # Save image to a local path so it can be passed to the model
            basename = os.path.basename(urlparse(url).path)
            temp_path = os.path.join(output_dir, f"temp_{basename}")
            image.save(temp_path)

            # Create a prompt describing the image path and task
            # prompt = f"{task}\nImage path: {temp_path}"
            # result_text = self.model.completion(prompt)
            result_text = self.model.process_image(task=task, image=image)

            results.append({
                "title": item.get("title", ""),
                "summary": item.get("summary", ""),
                "brief_summary": item.get("brief_summary", ""),
                "keywords": item.get("keywords", []),
                "url": url,
                "result": {"text": result_text}
            })

        return {
            "task": task,
            "results": results
        }

    async def get_recv_format(self):
        """Return the expected input format schema for the Vision agent."""
        return {
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "summary": {"type": "string"},
                            "brief_summary": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "url": {"type": "string"}
                        },
                        "required": ["title", "summary", "brief_summary", "keywords", "url"]
                    }
                }
            },
            "required": ["task", "data"]
        }

    async def get_send_format(self):
        """Return the expected output format schema from the Vision agent."""
        return {
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "summary": {"type": "string"},
                            "brief_summary": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "url": {"type": "string"},
                            "result": {"type": "object"}
                        },
                        "required": ["title", "summary", "brief_summary", "keywords", "url", "result"]
                    }
                }
            },
            "required": ["task", "results"]
        }

