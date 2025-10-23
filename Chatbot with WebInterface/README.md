## Step 1: Hosting your chatbot on a backend server
## What is a backend server?
A backend server is like the brain behind a website or application. In this case, the backend server will receive prompts from your website, feed them into your chatbot, and return the output of the chatbot back to the website, which will be read by the user.

## Hosting a simple backend server using Flask
_Note: Consider using a requirements.txt file_

`flask` is a Python framework for building web applications with Python. It provides a set of tools and functionalities to handle incoming requests, process data, and generate responses, making it easy to power your website or application.

## Setting up the server
Next, you will create a script that stores your flask server code.

To create a new Python file, Click on File Explorer, then right-click in the explorer area and select New File. Name this new file `app.py`.

Let's take a look at how to implement a simple flask server:
```Python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```
Paste the above code in the `app.py` file you just created and save it.

In this code:
- You import the `Flask` class from the `flask` module.
- You create an instance of the `Flask` class and assign it to the variable app.
- You define a route for the homepage by decorating the `home()` function with the `@app.route()` decorator. The function returns the string 'Hello, World!'. This means that when the user visits the URL where the website is hosted, the backend server will receive the request and return 'Hello, World!' to the user.
- The `if __name__ == '__main__'`: condition ensures that the server is only run if the script is executed directly, not when imported as a module.
- Finally, you call `app.run()` to start the server.

Before proceeding, you'll also add two more lines of code to your program to mitigate CORS errors - a type of error related to making requests to domains other than the one that hosts this webpage.

You'll be modifying your code as follows:
```Python
from flask import Flask
from flask_cors import CORS		# newly added

app = Flask(__name__)
CORS(app)				# newly added

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

## Integrating your chatbot into your Flask server
Now that you have your Flask server set up, let's integrate your chatbot into your Flask server.
First, you'll install the requisites
```
python3.11 -m pip install transformers==4.38.2
python3.11 -m pip install torch==2.2.1
```

Next, let's copy the code to initialize your chatbot from lab 1 and place it at the top of your script. You also must import the necessary libraries for your chatbot.
```Python
from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
```
```Python
model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history = []
```
Next, you'll need to import a couple more modules to read the data.
```Python
from flask import request
import json
```

Before implementing the actual function though, you need to determine the structure you expect to receive in the incoming HTTP request.

Let's define your expected structure as follows:
```
{
    'prompt': 'message'
}
```
Now implement your chatbot function. Again, you'll copy code over from your chatbot implementation from the first lab.
```Python
@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    # Read prompt from HTTP request body
    data = request.get_data(as_text=True)
    data = json.loads(data)
    input_text = data['prompt']

    # Create conversation history string
    history = "\n".join(conversation_history)

    # Tokenize the input text and history
    inputs = tokenizer.encode_plus(history, input_text, return_tensors="pt")

    # Generate the response from the model
    outputs = model.generate(**inputs, max_length= 60)  # max_length will acuse model to crash at some point as history grows

    # Decode the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Add interaction to conversation history
    conversation_history.append(input_text)
    conversation_history.append(response)

    return response
```
The only new thing you've done uptil now is read the prompt from the HTTP request body. You've copied everything else from your previous chatbot implementation!

Perfect, now before testing your application, here's what the final version of your code looks like:
```Python
from flask import Flask, request, render_template
from flask_cors import CORS
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)
CORS(app)

model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history = []

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    input_text = data['prompt']

    # Create conversation history string
    history = "\n".join(conversation_history)

    # Tokenize the input text and history
    inputs = tokenizer.encode_plus(history, input_text, return_tensors="pt")

    # Generate the response from the model
    outputs = model.generate(**inputs, max_length= 60)  # max_length will cause the model to crash at some point as history grows

    # Decode the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Add interaction to conversation history
    conversation_history.append(input_text)
    conversation_history.append(response)

    return response

if __name__ == '__main__':
    app.run()
```
Now let's test your implementation by using curl to make a POST request to <HOST>/chatbot with the following request body: {'prompt':'Hello, how are you today?'}.
```
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Hello, how are you today?"}' 127.0.0.1:5000/chatbot
```
Here's the output of the above code:
```
I am doing very well today as well. I am glad to hear you are doing well.
```
If you got a similar response, then congratulations! You have successfully created a Flask backend server with an integrated chatbot!