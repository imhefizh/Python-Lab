## Image Captioning BLIP
Create a Python virtual environment and install Gradio using the following commands in the terminal:
```
pip3 install virtualenv 
virtualenv my_env # create a virtual environment my_env
source my_env/bin/activate # activate my_env
```
Then, install the required libraries in the environment:
```
# installing required libraries in my_env
pip install langchain==0.1.11 gradio==5.23.2 transformers==4.38.2 bs4==0.0.2 requests==2.31.0 torch==2.2.1
```

### Step 1: Import your required tools from the transformers library
You have already installed the package transformers during setting up the environment.

In the project directory, create a Python file, Click on File Explorer, then right-click in the explorer area and select New File. Name this new file image_cap.py. copy the various code segments below and paste them into the Python file.

You will be using AutoProcessor and BlipForConditionalGeneration from the transformers library.

"AutoProcessor" and "BlipForConditionalGeneration" are components of the BLIP model, which is a vision-language model available in the Hugging Face Transformers library.

- AutoProcessor : This is a processor class that is used for preprocessing data for the BLIP model. It wraps a BLIP image processor and an OPT/T5 tokenizer into a single processor. This means it can handle both image and text data, preparing it for input into the BLIP model.

Note: A tokenizer is a tool in natural language processing that breaks down text into smaller, manageable units (tokens), such as words or phrases, enabling models to analyze and understand the text.

- BlipForConditionalGeneration : This is a model class that is used for conditional text generation given an image and an optional text prompt. In other words, it can generate text based on an input image and an optional piece of text. This makes it useful for tasks like image captioning or visual question answering, where the model needs to generate text that describes an image or answer a question about an image.
```
import requests
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
```

### Step 2: Load and Preprocess an Image
After loading the processor and the model, you need to initialize the image to be captioned. The image data needs to be loaded and pre-processed to be ready for the model.

To load the image right-click anywhere in the Explorer (on the left side of code pane), and click Upload Files... (shown in image below). You can upload any image from your local files, and modify the img_path according to the name of the image.

In the next phase, you fetch an image, which will be captioned by your pre-trained model. This image can either be a local file or fetched from a URL. The Python Imaging Library, PIL, is used to open the image file and convert it into an RGB format which is suitable for the model.
```
# Load your image, DON'T FORGET TO WRITE YOUR IMAGE NAME
img_path = "YOUR IMAGE NAME.jpeg"
# convert it into an RGB format 
image = Image.open(img_path).convert('RGB')
```
Next, the pre-processed image is passed through the processor to generate inputs in the required format. The return_tensors argument is set to "pt" to return PyTorch tensors.
```
# You do not need a question for image captioning
text = "the image of"
inputs = processor(images=image, text=text, return_tensors="pt")
```

You then pass these inputs into your model's generate method. The argument max_length=50 specifies that the model should generate a caption of up to 50 tokens in length.

The two asterisks (**) in Python are used in function calls to unpack dictionaries and pass items in the dictionary as keyword arguments to the function. **inputs is unpacking the inputs dictionary and passing its items as arguments to the model.

```
# Generate a caption for the image
outputs = model.generate(**inputs, max_length=50)
```
Finally, the generated output is a sequence of tokens. To transform these tokens into human-readable text, you use the decode method provided by the processor. The skip_special_tokens argument is set to True to ignore special tokens in the output text.
```
# Decode the generated tokens to text
caption = processor.decode(outputs[0], skip_special_tokens=True)
# Print the caption
print(caption)
```

Save your Python file and run it to see the result.
```
python3 image_cap.py
```

## Gradio: Creating a simple demo

```
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

demo.launch(server_name="0.0.0.0", server_port= 7860)
```

The code creates a Gradio interface called demo using the gr.Interface class. It wraps the greet function with a simple text-to-text user interface that you could interact with.

The gr.Interface class is initialized with 3 required parameters:
- fn: the function to wrap a UI around
- inputs: which component(s) to use for the input (e.g. “text”, “image” or “audio”)
- outputs: which component(s) to use for the output (e.g. “text”, “image” or “label”)
The last line demo.launch() launches a server to serve your demo.

### Launching the Demo App
Now go back to the terminal and make sure that the my_env virtual environment name is displayed at the beginning of the line.

Now run the following command to execute the Python script.
```
python3 hello.py
```

## Exercise: Implement image captioning app with Gradio
Make sure you have the necessary libraries installed. Run 
```
pip install gradio transformers Pillow to install Gradio, Transformers, and Pillow.
```

## Implementing automated image captioning tool
