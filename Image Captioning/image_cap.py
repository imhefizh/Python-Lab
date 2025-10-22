import numpy as np
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def image_captioning(input_img: np.ndarray):
    # Load your image, DON'T FORGET TO WRITE YOUR IMAGE NAME
    img_path = "img_sample2.jpg"
    # convert it into an RGB format 
    image = Image.fromarray(input_img).convert('RGB')

    # You do not need a question for image captioning
    text = "the image of"
    inputs = processor(images=image, text=text, return_tensors="pt")

    # Generate a caption for the image
    outputs = model.generate(**inputs, max_length=50)

    # Decode the generated tokens to text
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    # Print the caption
    return caption