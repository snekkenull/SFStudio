import requests
import gradio as gr
from .config import API_KEY, URL

translate_prompt = """
You are a professional translator, you can accurately translate any input content into natvie English. Your output should be only in English translation without other eplanation.
For example:
**Input** Coche de estilo ciberpunk.
**Output** A car in Cyber Punk style.
"""

def generate_text(prompt, translateModel):
    payload = {
        "model": translateModel,
        "messages": [
                {"role": "system", "content": translate_prompt},
                {"role": "user", "content": prompt}
            ],
        "stream": False,
        "max_tokens": 128,
        "temperature": 0.3
        }
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    url = URL + "/chat/completions"
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.text
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise gr.Error(f'Errors, try again later. Reports：{str(e)}')