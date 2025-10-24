## Preparing the environment
Let's start with setting up the environment by creating a Python virtual environment and installing the required libraries, using the following commands in the terminal:
```
pip3 install virtualenv 
virtualenv my_env # create a virtual environment my_env
source my_env/bin/activate # activate my_env
```
Then, install the required libraries in the environment (this will take time ☕️☕️):
```
# installing required libraries in my_env
pip install transformers==4.36.0 torch==2.1.1 gradio==5.23.2 langchain==0.0.343 ibm_watson_machine_learning==1.0.335 huggingface-hub==0.28.1
```

_We need to install ffmpeg to be able to work with audio files in python._
```
sudo apt update
sudo apt install ffmpeg -y
```

## Step 1: Speech-to-Text
Create and open a Python file and call it `simple_speech2text.py`.
Let's download the file first (you can do it manually, then drag and drop it into the file environment).
```Python
import requests

# URL of the audio file to be downloaded
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-GPXX04C6EN/Testing%20speech%20to%20text.mp3"

# Send a GET request to the URL to download the file
response = requests.get(url)

# Define the local file path where the audio file will be saved
audio_file_path = "downloaded_audio.mp3"

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # If successful, write the content to the specified local file path
    with open(audio_file_path, "wb") as file:
        file.write(response.content)
    print("File downloaded successfully")
else:
    # If the request failed, print an error message
    print("Failed to download the file")
```
Run the Python file to test it.
```
python3 simple_speech2text.py
```

Next, implement OpenAI Whisper for transcribing voice to speech.

You can override the previous code in the Python file.
```Python
import torch
from transformers import pipeline

# Initialize the speech-to-text pipeline from Hugging Face Transformers
# This uses the "openai/whisper-tiny.en" model for automatic speech recognition (ASR)
# The `chunk_length_s` parameter specifies the chunk length in seconds for processing
pipe = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-tiny.en",
  chunk_length_s=30,
)

# Define the path to the audio file that needs to be transcribed
sample = 'downloaded_audio.mp3'

# Perform speech recognition on the audio file
# The `batch_size=8` parameter indicates how many chunks are processed at a time
# The result is stored in `prediction` with the key "text" containing the transcribed text
prediction = pipe(sample, batch_size=8)["text"]

# Print the transcribed text to the console
print(prediction)
```
Run the Python file and you will get the output.
```
python3 simple_speech2text.py
```

## Step 2: Creating audio transcription app
Create a new python file `speech2text_app.py`.
```Python
import torch
from transformers import pipeline
import gradio as gr

def transcript_audio(audio_file):
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny.en",
        chunk_length_s=30
    )

    result = pipe(audio_file, batch_size=8)["text"]
    return result

audio_input = gr.Audio(sources="upload", type="filepath")
output_text = gr.Textbox()

iface = gr.Interface(
    fn=transcript_audio, 
    inputs=audio_input,
    outputs=output_text,
    title="Audio Transcription App",
    description="Made by Maulana Hafidz"
    )

iface.launch(server_name="0.0.0.0",
server_port=7860)
```
Then, run your app

## Step 3: Integrating LLM: Using Llama 3 in WatsonX as LLM
Let's start by generating text with LLMs. Create a Python file and name it `simple_llm.py`.

In case, you want to use Llama 3 as an LLM instance, you can follow the instructions below:

_IBM WatsonX utilizes various language models, including Llama 3 by Meta, which is currently the strongest open-source language model._

Here's how the code works:
1. Setting up credentials: The credentials needed to access IBM's services are pre-arranged by the Skills Network team, so you don't have to worry about setting them up yourself.
2. Specifying parameters: The code then defines specific parameters for the language model. 'MAX_NEW_TOKENS' sets the limit on the number of words the model can generate in one go. 'TEMPERATURE' adjusts how creative or predictable the generated text is.
3. Setting up Llama 3 model: Next, the LLAMA3 model is set up using a model ID, the provided credentials, chosen parameters, and a project ID.
4. Creating an object for Llama 3: The code creates an object named llm, which is used to interact with the Llama 3 model. A model object, LLAMA3_model, is created using the Model class, which is initialized with a specific model ID, credentials, parameters, and project ID. Then, an instance of WatsonxLLM is created with LLAMA3_model as an argument, initializing the language model hub llm object.
5. Generating and printing response: Finally, 'llm' is used to generate a response to the question, "How to read a book effectively?" The response is then printed out.
```Python
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

my_credentials = {
    "url"    : "https://us-south.ml.cloud.ibm.com"
}

params = {
        GenParams.MAX_NEW_TOKENS: 700, # The maximum number of tokens that the model can generate in a single run.
        GenParams.TEMPERATURE: 0.1,   # A parameter that controls the randomness of the token generation. A lower value makes the generation more deterministic, while a higher value introduces more randomness.
    }

LLAMA2_model = Model(
        model_id= 'meta-llama/llama-3-2-11b-vision-instruct', 
        credentials=my_credentials,
        params=params,
        project_id="skills-network",  
        )

llm = WatsonxLLM(LLAMA2_model)  

print(llm("How to read a book effectively?"))
```
You can then run this script

## Step 4: Put them all together
Create a new Python file and call it `speech_analyzer.py`

In this exercise, we'll set up a language model (LLM) instance, which could be IBM WatsonxLLM, HuggingFaceHub, or an OpenAI model. Then, we'll establish a prompt template. These templates are structured guides to generate prompts for language models, aiding in output organization (more info in langchain prompt template).

Next, we'll develop a transcription function that employs the OpenAI Whisper model to convert speech-to-text. This function takes an audio file uploaded through a Gradio app interface (preferably in .mp3 format). The transcribed text is then fed into an LLMChain, which integrates the text with the prompt template and forwards it to the chosen LLM. The final output from the LLM is then displayed in the Gradio app's output textbox.