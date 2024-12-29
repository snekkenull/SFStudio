import os
import gradio as gr
import asyncio
import requests
from requests.exceptions import RequestException
from .config import API_KEY, URL

def check_response(response):
    if response.status_code != 200:
        raise gr.Error(f'API Error: {response.status_code} - {response.text}')
    else:
        return response.json()

async def generate_video(prompt, model):
    payload = {
        "model": model,
        "prompt": prompt
    }
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    try:
        url = URL + "/video/submit"
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise exception for bad status codes
        data = check_response(response)

        requestId = data["requestId"]

        status_url = URL + "/video/status" # Get from config if available

        payload = {
            "requestId": requestId
        }

        response = requests.post(status_url, json=payload, headers=headers)
        response.raise_for_status()
        data = check_response(response)

        while data["status"] == "InProgress":
            await asyncio.sleep(5)
            response = requests.post(status_url, json=payload, headers=headers)
            response.raise_for_status()
            data = check_response(response)

        if data["status"] != "Succeed":
            raise gr.Error(f"Video generation failed. Status: {data['status']}")

        video_url = data["results"]["videos"][0]["url"]

        # Download video
        video = requests.get(video_url, stream=True)
        video.raise_for_status()

        # Ensure output directory exists
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        videoname = os.path.join(output_dir, f"{os.urandom(16).hex()}.mp4")

        with open(videoname, 'wb') as f:
            for chunk in video.iter_content(chunk_size=8192):
                f.write(chunk)

        return videoname # Return filepath for gradio.Video

    except RequestException as e:
        raise gr.Error(f'Network Error: {str(e)}')
    except Exception as e:
        raise gr.Error(f'An unexpected error occurred: {str(e)}')
