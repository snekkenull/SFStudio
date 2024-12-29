# Siliconflow Studio WebUI

A Gradio webui for Siliconflow API.

Use Siliconflow text-generation model to translate prompts, and auto optimzing the prompts and text-to-image model to generate images.

Now supports:

- Text-to-image(flux.1-schnell)

- Text-to-video(LTX-Video)

- Translation(for prompt, by text-generation models)


## Preview

![alt text](<image.png>)

## Use

Clone the repo to your disk, change the .env.example to .env, and set the right values.Run the commands in terminal on the directory:

```
python -m venv venv

source ./venv/bin/activate

python -m pip install -r requirements.txt

python app.py
```
