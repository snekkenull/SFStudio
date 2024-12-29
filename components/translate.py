import requests
import gradio as gr
import json
from .config import API_KEY, URL

# working in process

translate_prompt = """
You are a professional translator, you can accurately translate any input content into natvie English. Your output should be only in English translation without other eplanation.
For example:
**Input** Coche de estilo ciberpunk.
**Output** A car in Cyber Punk style.
"""

def translator(prompt, system_prompt, history, model):
    payload = {
        "model": model,
        "messages": [
                {"role": "system", "content": system_prompt},
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
        data = json.loads(response.text)
        result = data["choices"][0]["message"]["content"]
        return result
    except Exception as e:
        raise gr.Error(f'Errors, try again later. Reports：{str(e)}')