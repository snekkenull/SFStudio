import os
from io import BytesIO
from PIL import Image
import gradio as gr
import asyncio
import json
import requests
from .config import API_KEY, URL


async def generate_image(prompt, model):
    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": "1024x1024",
        "prompt_enhancement": True
    }
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    try:
        url = URL + "/images/generations"
        response = requests.request("POST", url, json=payload, headers=headers)

        data = json.loads(response.text)

        image_url = data["images"][0]["url"]

        image = Image.open(BytesIO(requests.get(image_url).content))
        # Ensure output directory exists
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        # random uuid filename
        imagename = os.path.join(output_dir, f"{os.urandom(16).hex()}.webp")

        # save image in data folder
        image.save(imagename)

        return imagename

    except Exception as e:
        raise gr.Error(f'Errors, try again later. Reports：{str(e)}')
