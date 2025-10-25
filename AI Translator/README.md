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
.