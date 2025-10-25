# Introduction
Babel Fish is a metaphor for a translation service or a tool - based on a fictional creature from Douglas Adams' "The Hitchhiker's Guide to the Galaxy" series. 

## Step 1: Understanding the interface
First, let's set up the environment by executing the following code:
```
python3.11 -m venv my_env
source my_env/bin/activate # activate my_env
```
Run the following commands in the terminal to receive the outline of the project, rename it with another name and finally move into that directory:
```
git clone https://github.com/ibm-developer-skills-network/translator-with-voice-and-watsonx
cd translator-with-voice-and-watsonx
```
installing the requirements for the project
```
pip install -r requirements.txt
```

## Step 2: Understanding the server
The server is how the application will run and communicate with all our services. Flask is a web development framework for Python and can be used as a backend for the application. It is a lightweight and simple framework that makes it quick and easy to build web applications.

The code provided gives the outline for the server in the ``server.py` file

At the top of the file, there are several import statements. These statements are used to bring in external libraries and modules, which will be used in the current file. For example, speech_text is a function inside the worker.py file, while ibm_watson_machine_learning is a package that needs to be installed to use Watsonx's mistralai/mistral-large model. These imported packages, modules, and libraries will allow you to access the additional functionalities and methods that they offer, making it easy to interact with the speech-to-text and mistralai/mistral-large models in your code.

Underneath the imports, the Flask application is initialized, and a CORS policy is set. 

_A CORS policy is used to allow or prevent web pages from making requests to different domains than the one that served the web page. Currently, it is set to * to allow any request._

Replace the first route in the server.py with the code below:
```Python
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
```

When a user tries to load the application, they initially send a request to go to the / endpoint. They will then trigger this index function and execute the code above. Currently, the returned code from the function is a render function to show the index.html file which is the frontend interface.

The next sections will take you through the process of completing the process_message_route and speech_to_text_route functions in this file and help you understand how to use the packages and endpoints.

## Step 3: Integrating Watsonx API
It's time to give your voice assistant a brain! With the power of Watsonx's API, we can pass the transcribed text and receive responses that answer your questions.

### Authenticating for programmatic access
In this project, you do not need to specify your own Watsonx_API and Project_id to the below worker.py code. You can just specify project_id="skills-network" and leave Watsonx_API blank, as in this CloudIDE environment, we have already granted you access to API without your own Watsonx_API and Project_id.

Add the following at the top of the file:
```Python
# To call watsonx's LLM, we need to import the library of IBM Watson Machine Learning
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models import Model

# placeholder for Watsonx_API and Project_id incase you need to use the code outside this environment
# API_KEY = "Your WatsonX API"
PROJECT_ID= "skills-network"

# Define the credentials 
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
    #"apikey": API_KEY
}
    
# Specify model_id that will be used for inferencing
model_id = "mistralai/mistral-medium-2505"


# Define the model parameters
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
    GenParams.MIN_NEW_TOKENS: 1,
    GenParams.MAX_NEW_TOKENS: 1024
}

# Define the LLM
model = Model(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=PROJECT_ID
)
```

### Watsonx process message function
We will be updating the function called watsonx_process_message, which will take in a prompt and pass it to Watsonx's mistralai/mistral-medium-2505 API to receive a response. Essentially, it's the equivalent of pressing the send button to get a response from ChatGPT.

Go ahead and update the watsonx_process_message function in the worker.py file with the following.
```Python
def watsonx_process_message(user_message):
    # Set the prompt for Watsonx API - using a strict translation instruction
    prompt = f"""Respond to the query: ```{user_message}```"""
    response_text = model.generate_text(prompt=prompt)
    print("wastonx response:", response_text)
    return response_text.strip()
```

### Prompt refinement
We will have to optimize our translation assistant. Since this is a translator, users shouldn't have to type "translate" every time. To address this, we've improved the prompt in the watsonx_process_message function to be more explicit.

For example, we now focus on translating sentences from English into Spanish, the updated prompt will look like below. Replace the prompt in the function with this:
```Python
 prompt = f"""
    Translate the following English sentence into Spanish. 
    Reply ONLY with the translation, no explanations, no formatting, no extra text.

    English: {user_message}
    Spanish:
    """
```

This revised prompt makes it evident that the user intends to translate a sentence into Spanish, eliminating the need to explicitly mention "translate."

If your translation needs to involve languages other than Spanish, you can easily adapt the prompt. Simply replace "Spanish" in the prompt with the name of your required target language. This modification simplifies the user interaction and ensures that the translator remains user-friendly for various language pairs.

### Function explanation
The function is really simple, thanks to the very easy-to-use `ibm_watson_machine_learning` library.

Then we call Wastonx's API by using model.generate_text function and pass the prompt that we need the response for. Remember that model refers to the LLM we established earlier.

## Step 4: Integrating Watson Speech-to-Text

Speech-to-Text functionality is a technology that converts speech into text using machine learning. It is useful for accessibility, productivity, convenience, multilingual support, and cost-effective solutions for a wide range of applications. For example, being able to take a user's voice as input for a chat application.

Using the embedded Watson Speech-to-Text AI model that was deployed earlier, it is possible to easily convert our Speech-to-Text by a simple API. This result can then be passed to Watsonx API for generating a response.

### Starting Speech-to-Text

kills Network provides its own Watson Speech-to-Text image that is run automatically in this environment. To access it, use this endpoint URL: `https://sn-watson-stt.labs.skills.network`

You can test it works by running this query:
```
curl https://sn-watson-stt.labs.skills.network/speech-to-text/api/v1/models
```
Next, try getting an example audio file to send a /recognize request to test the service. For example, you can download the example audio file by this command:
```
curl "https://github.com/watson-developer-cloud/doc-tutorial-downloads/raw/master/speech-to-text/0001.flac" -sLo example.flac
```
Send the audio file to the service:
```
curl "https://sn-watson-stt.labs.skills.network/speech-to-text/api/v1/recognize" --header "Content-Type: audio/flac" --data-binary @example.flac
```

### Implementation
We will be updating a function called `speech_to_text` in the `worker.py` file that will take in audio data received from the browser and pass it to the Watson Speech-to-Text API.

The `speech_to_text` function will take in audio data as a parameter, make an API call to the Watson Speech-to-Text API using the requests library, and return the transcription of the audio data.

Remember to replace the `...` for `the base_url` variable with the URL for your Speech-to-Text model (for example, `https://sn-watson-stt.labs.skills.network`).

```Python
import requests

def speech_to_text(audio_binary):

    # Set up Watson Speech-to-Text HTTP Api url
    base_url = '...'
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    # Set up parameters for our HTTP reqeust
    params = {
        'model': 'en-US_Multimedia',
    }

    # Set up the body of our HTTP request
    body = audio_binary

    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()

    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('Speech-to-Text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text
```

### Function explanation
The requests library imported at the top of our `worker.py` file is a simple HTTP request library that we will be using to make API calls to the Watson Speech-to-Text API.

The function simply takes `audio_binary` as the only parameter and then sends it in the body of the HTTP request.

To make an HTTP Post request to Watson Speech-to-Text API, we need the following three elements:
1. URL of the API: This is defined as `api_url` in our code and points to Watson's Speech-to-Text service
2. Parameters: This is defined as `params` in our code. It's just a dictionary having one key-value pair i.e. 'model': 'en-US_Multimedia' which tells Watson that we want to use the US English model for processing our speech
3. Body of the request: this is defined as `body` and is equal to `audio_binary` since we are sending the audio data inside the body of our POST request.

We then use the requests library to send this HTTP request passing in the URL, params, and data(body) to it and then use `.json()` to convert the API's response to json format which is very easy to parse and can be treated like a dictionary in Python.

```
{
  "response": {
    "results": {
      "alternatives": {
        "transcript": "Recognised text from your speech"
      }
    }
  }
}
```

## Step 5: Integrating Watson Text-to-Speech
Time to give your assistant a voice using Text-to-Speech functionality.

Once we have processed the user's message using Watsonx, let's add the final worker function that will convert that response to speech, so you get a more personalized feel as the Personal Assistant is going to read out the response to you. Just like other virtual assistants like Google, Alexa, Siri, etc.

### Starting Text-to-Speech
Skills Network provides its own Watson Text-to-Speech image that is run automatically in this environment. To access it, use this endpoint URL: `https://sn-watson-tts.labs.skills.network`

You can test it works by running this query:
```
curl https://sn-watson-tts.labs.skills.network/text-to-speech/api/v1/voices
```
You should see a list of a bunch of different voices this model can use. An example output is shown below.
```
{
   "voices": [
      {
         "name": "en-US_OliviaV3Voice",
         "language": "en-US",
         "gender": "female",
         "description": "Olivia: American English female voice. Dnn technology.",
         ...
      },
      {
         "name": "es-ES_EnriqueV3Voice",
         "language": "en-GB",
         "gender": "male",
         "description": "Enrique: Castilian Spanish (español castellano) male voice. Dnn technology.",
         ...
      },
      ...
   ]
}
```
Next, try sending an example text (ex: "Hello world") in JSON format to invoke /synthesize request. It will return an audio file named "output.wav" in the "translator-with-voice-and-watsonx" directory:
```
curl "https://sn-watson-stt.labs.skills.network/text-to-speech/api/v1/synthesize" --header "Content-Type: application/json" --data '{"text":"Hello world"}' --header "Accept: audio/wav" --output output.wav
```
To use a different model, add the voice query parameter to the request. To change the audio format, change the Accept header. For example:
```
curl "https://sn-watson-stt.labs.skills.network/text-to-speech/api/v1/synthesize?voice=es-LA_SofiaV3Voice" --header "Content-Type: application/json" --data '{"text":"Hola! Hoy es un dia muy bonito."}' --header "Accept: audio/mp3" --output hola.mp3
```
After executing the above command, you'll find the output file named "hola.mp3" in the "translator-with-voice-and-watsonx" directory.

### Text-to-Speech function
In the `worker.py` file, the `text_to_speech` function passes data to Watson's Text-to-Speech API to get the data as spoken output.

This function is going to be similar to `speech_to_text` as we will be utilizing our request library again to make an HTTP request. Lets dive into the code. Again, remember to replace the `...` for the `base_url` variable with the URL for your Text-to-Speech model (for example, `https://sn-watson-tts.labs.skills.network`).

```Python
def text_to_speech(text, voice=""):
    # Set up Watson Text-to-Speech HTTP Api url
    base_url = '...'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    # Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

    # Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }

    # Send a HTTP Post reqeust to Watson Text-to-Speech Service
    response = requests.post(api_url, headers=headers, json=json_data)
    print('Text-to-Speech response:', response)
    return response.content
```

### Function explanation
The function takes text and voice as parameters. It adds voice as a parameter to the api_url if it's not empty or not default. It sends the text in the body of the HTTP request.

Similarly as before, to make an HTTP Post request to Watson Text-to-Speech API, we need the following three elements:
1. URL of the API: This is defined as api_url in our code and points to Watson's Text-to-Speech service. This time we also append a voice parameter to the api_url if the user has sent a preferred voice in their request.
2. Headers: This is defined as headers in our code. It's just a dictionary having two key-value pairs. The first is 'Accept':'audio/wav' which tells Watson that we are sending audio having wav format. The second one is 'Content-Type':'application/json', which means that the format of the body would be JSON
3. Body of the request: This is defined as json_data and is a dictionary containing 'text':text key-value pair, this text will then be processed and converted to a speech.
We then use the requests library to send this HTTP to request passing in the URL, headers, and json(body) to it and then use .json() to convert the API's response to json format so we can parse it.

The structure of the response is something like this:
```
{
  "response": {
        content: The Audio data for the processed Text-to-Speech
    }
}
```
Therefore, we return response.content which contains the audio data received..