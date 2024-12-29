import gradio as gr
import asyncio
from io import BytesIO
import numpy as np
from components import generate_image, translator, generate_video

prompt_new = ""

CSS = """
h1 {
    margin-top: 10px
}

footer {
    visibility: hidden;
}
"""

modelMap  = {
    "Qwen2.5-7B": "Qwen/Qwen2.5-7B-Instruct",
    "Llama-3.1-8B": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "Flux.1-Schnell": "black-forest-labs/FLUX.1-schnell",
    "LTX-Video": "Lightricks/LTX-Video",
    "NONE": "",
}


# image generation
async def gen(prompt: str, translateModel:str, imgModel: str):
    global prompt_new
    if modelMap[translateModel]:
        prompt_new = translator(prompt, modelMap[translateModel])
    else:
        prompt_new = prompt
    image_task = asyncio.create_task(generate_image(prompt_new, modelMap[imgModel]))
    output_image = await image_task
    yield prompt_new, output_image


def image_to_int_array(image, format="PNG"):
    """Current Workers AI REST API consumes an array of unsigned 8 bit integers"""
    # Convert to bytes
    buffer = BytesIO()
    image.save(buffer, format=format)

    # Convert to uint8 array and ensure values are between 0-255
    uint8_array = np.frombuffer(buffer.getvalue(), dtype=np.uint8)
    # Convert to regular Python list
    return uint8_array.tolist()


# video generation

async def gen_video(prompt: str, translateModel:str, model: str):
    global prompt_new
    if modelMap[translateModel]:
        prompt_new = translator(prompt, modelMap[translateModel])
    else:
        prompt_new = prompt
    video_task = asyncio.create_task(generate_video(prompt_new, modelMap[model]))
    video = await video_task
    return prompt_new, video

# Gradio Interface

with gr.Blocks(theme="soft", title="SFS By snekkenull", css=CSS) as demo:
    gr.HTML("<h1><center>SFStudio</center></h1>")
    with gr.Tab("Image generation"):
        gr.HTML("""
        <p>
            <center>
                Based on Flux.1 model, it can generate the corresponding image according to your cue words.
            </center>
        </p>
        """)
        prompt = gr.Textbox(label='Prompts ✏️', placeholder="A car...")
        with gr.Row():
            sendBtn = gr.Button(value="Submit", variant='primary')
            clearBtn = gr.ClearButton([prompt], value="Clear")
        gen_text = gr.Textbox(label="Translating 🦖")
        gen_img = gr.Image(type="filepath", label='Generate 🎨', height=600)
        with gr.Accordion("Advanced ⚙️", open=False):
            translateModel = gr.Dropdown(label="Prompts-To-Eng Model", value="Qwen2.5-7B", choices=["NONE","Qwen2.5-7B", "Llama-3.1-8B"])
            imgModel = gr.Dropdown(label="Image-Generator Model", value="Flux.1-Schnell", choices=["Flux.1-Schnell"])

        gr.on(
            triggers = [
                prompt.submit,
                sendBtn.click,
            ],
            fn = gen,
            inputs = [
                prompt,
                translateModel,
                imgModel,
            ],
            outputs = [gen_text, gen_img]
        )

    with gr.Tab("Video generation"):
        gr.HTML("""
        <p>
            <center>
                Based on LTX-Video model, generate video by inputting prompt.
            </center>
        </p>
        """)
        vg_prompt = gr.Textbox(label='Prompts ✏️', placeholder="A car...")
        with gr.Row():
            vg_sendBtn = gr.Button(value="Submit", variant='primary')
            vg_clearBtn = gr.ClearButton([vg_prompt], value="Clear")
        vg_text = gr.Textbox(label="Translating 🦖")
        video_out = gr.PlayableVideo(label='Generate 🎞️', height=600)
        with gr.Accordion("Advanced ⚙️", open=False):
            vg_translateModel = gr.Dropdown(label="Prompts-To-Eng Model", value="Qwen2.5-7B", choices=["NONE","Qwen2.5-7B", "Llama-3.1-8B"])
            vgModel = gr.Dropdown(label="Video-Generator Model", value="LTX-Video", choices=["LTX-Video"])

        gr.on(
            triggers = [
                vg_prompt.submit,
                vg_sendBtn.click,
            ],
            fn = gen_video,
            inputs = [
                vg_prompt,
                vg_translateModel,
                vgModel
            ],
            outputs = [vg_text, video_out]
        )

    gr.HTML("""
    <p><a href="https://github.dev/snekkenull/sfstudio"> Snekkenull </a>  Open-Source</p>
    """)

if __name__ == "__main__":
    demo.queue(api_open=False).launch(server_name="0.0.0.0", server_port=7860, show_api=False, share=False)