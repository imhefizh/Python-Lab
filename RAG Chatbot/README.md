## Setting up and understanding the user interface

In this project, the goal is to create a chatbot with an interface that allows communication.

First, let's set up the environment by executing the following code:
```
pip3 install virtualenv 
virtualenv my_env # create a virtual environment my_env
source my_env/bin/activate # activate my_env
```
The frontend will use HTML, CSS, and JavaScript. The user interface will be similar to many chatbots you see and use online. The code for the interface is provided and the focus of this guided project is to connect this interface with the backend that handles the uploading of your custom documents and integrates it with an LLM model to get customized responses. The provided code will help you to understand how the frontend and backend interact, and as you go through it, you will learn about the important parts and how it works, giving you a clear understanding of how the frontend works and how to create this simple web page.

Run the following commands to retrieve the project, give it an appropriate name, and finally move to that directory by running the following:
```
git clone https://github.com/ibm-developer-skills-network/wbphl-build_own_chatbot_without_open_ai.git
mv wbphl-build_own_chatbot_without_open_ai build_chatbot_for_your_data
cd build_chatbot_for_your_data
```
installing the requirements for the project
```
pip install -r requirements.txt
pip install langchain-community
```

### HTML, CSS, and JavaScript
The `index.html` file is responsible for the layout and structure of the web interface. This file contains the code for incorporating external libraries such as JQuery, Bootstrap, and FontAwesome Icons, and the CSS (`style.css`) and JavaScript code (`script.js`) that control the styling and interactivity of the interface.

The `style.css` file is responsible for customizing the visual appearance of the page's components. It also handles the loading animation using CSS keyframes. Keyframes are a way of defining the values of an animation at various points in time, allowing for a smooth transition between different styles and creating dynamic animations.

The `script.js` file is responsible for the page's interactivity and functionality. It contains the majority of the code and handles all the necessary functions such as switching between light and dark mode, sending messages, and displaying new messages on the screen. It even enables the users to record audio.

## Understanding the worker: Document processing and conversation management worker, part 1
`worker.py` is part of a chatbot application that processes user messages and documents. It uses the `langchain` library, which is a Python library for building conversational AI applications. It is responsible for setting up the language model, processing PDF documents into a format that can be used for conversation retrieval, and handling user prompts to generate responses based on the processed documents. 

Let's break down each section in the worker file.
The worker.py is designed to provide a conversational interface that can answer questions based on the contents of a given PDF document.

![The diagram illustrates the procedure of document processing and information retrieval, seamlessly integrating a large language model (LLM) to facilitate the task of question answering. The whole process happens in worker.py](document-processing.jpg)

1. Initialization `init_llm()`:
    - Setting environment variables: The environment variable for the HuggingFace API token is set.
    - Loading the language model: The WatsonX language model is initialized with specified parameters.
    - Loading embeddings: Embeddings are initialized using a pre-trained model.
2. Document processing `process_document(document_path)`:
This function is responsible for processing a given PDF document.
    - Loading the document: The document is loaded using PyPDFLoader.
    - Splitting text: The document is split into smaller chunks using RecursiveCharacterTextSplitter.
    - Creating embeddings database: An embeddings database is created from the text chunks using Chroma.
    - Setting Up the RetrievalQA chain: A RetrievalQA chain is set up to facilitate the question-answering process. This chain uses the initialized language model and the embeddings database to answer questions based on the processed document.
3. User prompt processing `process_prompt(prompt)`:
This function processes a user's prompt or question.
    - Receiving user prompt: The system receives a user prompt (question).
    - Querying the model: The model is queried using the retrieval chain, and it generates a response based on the processed document and previous chat history.
    - Updating chat history: The chat history is updated with the new prompt and response.

### Delving into each section
_IBM watsonX utilizes various language models, including Llama models by Meta, which have been among the strongest open-source language model published so far (in Feb 2024)_

#### Initialization `init_llm()`:
This code is for setting up and using an AI language model, from IBM watsonX:
1. Credentials setup: Initializes a dictionary with the service URL and an authentication token ("skills-network").
2. Parameters configuration: Sets up model parameters like maximum token generation (256) and temperature (0.1, controlling randomness).
3. Model initialization: Creates a model instance with a specific model_id, using the credentials and parameters defined above, and specifies "skills-network" as the project ID.
4. Model usage: Initializes an interface (WatsonxLLM) with the configured model for interaction.

This script is specifically configured for a project or environment associated with the “skills-network”.

Complete the following code in `worker.py` by inserting the embeddings.

In this project, you do not need to specify your own `Watsonx_API` and `Project_id`. You can just specify `project_id="skills-network"` and leave `Watsonx_API` blank.

But it's important to note that this access method is exclusive to this Cloud IDE environment. If you are interested in using the model/API outside this environment (e.g., in a local environment), detailed instructions and further information are available in tutorials.

```Python
# placeholder for Watsonx_API and Project_id incase you need to use the code outside this environment
Watsonx_API = "Your WatsonX API"
Project_id= "Your Project ID"

# Function to initialize the language model and its embeddings
def init_llm():
    global llm_hub, embeddings

    logger.info("Initializing WatsonxLLM and embeddings...")

    # Llama Model Configuration
    MODEL_ID = "meta-llama/llama-3-3-70b-instruct"
    WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
    PROJECT_ID = "skills-network"

    # Use the same parameters as before:
    #   MAX_NEW_TOKENS: 256, TEMPERATURE: 0.1
    model_parameters = {
        # "decoding_method": "greedy",
        "max_new_tokens": 256,
        "temperature": 0.1,
    }

    # Initialize Llama LLM using the updated WatsonxLLM API
    llm_hub = WatsonxLLM(
        model_id=MODEL_ID,
        url=WATSONX_URL,
        project_id=PROJECT_ID,
        params=model_parameters
    )
    logger.debug("WatsonxLLM initialized: %s", llm_hub)

    #Initialize embeddings using a pre-trained model to represent the text data.
    embeddings =  # create object of Hugging Face Instruct Embeddings with (model_name,  model_kwargs={"device": DEVICE} )
    
    logger.debug("Embeddings initialized with model device: %s", DEVICE)
```



