import gradio as gr
from image_cap import image_captioning

imgcap = gr.Interface(
    fn=image_captioning,
    inputs=gr.Image(),
    outputs="text",
    title="Image Captioning",
    description="This is a simple web app for generating image caption"
)

imgcap.launch(server_name="0.0.0.0", server_port= 7860)