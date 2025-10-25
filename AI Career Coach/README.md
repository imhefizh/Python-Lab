## Preparation
1. Setting up a virtual environtment
2. Installing necessary libs
3. Setting up Gradio (Testing demo)

## Create a Q&A bot

This tutorial will walk you through the process of creating a Q&A chatbot leveraging the `llama-3-2-11b-vision-instruct` model developed by Meta.

This powerful foundation model has been seamlessly integrated into IBM's watsonx.ai platform, simplifying your development journey. Our provided API eliminates the need for generating complex API tokens, streamlining the application creation process. The llama-3-2-11b-vision-instruct model is equipped with features designed to
- Supports Q&A
- Summarization
- Classification
- Generation
- Extraction
- Retrieval-Augmented Generation tasks

Follow these step-by-step instructions to create your application:
1. Still in the PROJECT directory, create a new Python file named `simple_llm.py` (you are welcome to choose a different name if you prefer).
2. Enter the following script content into your newly created `simple_llm.py` file and save your changes. Line-by-line explanation of the code snippet is provided.
```py
# Import necessary packages
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model, ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames

# Model and project settings
model_id = "meta-llama/llama-3-2-11b-vision-instruct"  # Directly specifying the LLAMA3 model

# Set credentials to use the model
credentials = Credentials(
                   url = "https://us-south.ml.cloud.ibm.com",
                  )

# Set necessary parameters
params = TextChatParameters()

# Specifying project_id as provided
project_id = "skills-network"  


# Initialize the model
model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params=params
)
prompt_txt = "How to be a good Data Scientist?"  # Your question

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_txt
            },
        ]
    }
]

# Attempt to generate a response using the model with overridden parameters
generated_response = model.chat(messages=messages)
generated_text = generated_response['choices'][0]['message']['content']

# Print the generated response
print(generated_text)
```
3. Open your terminal and ensure that you are operating within the virtual environment (my_env) you previously established.
4. Run the app

In the code, we simply used "skills-network" as project_id to gain immediate, free access to the API without the need for initial registration. It's important to note that this access method is exclusive to this Cloud IDE environment.

## Integrate the application into Gradio
Having successfully created a Q&A bot with our script, you might notice that responses are only displayed in the terminal. You may wonder if it's possible to integrate this application with Gradio to leverage a web interface for inputting questions and receiving responses.

1. Navigate to the PROJECT directory, right-click and create a new file named llm_chat.py.
2. Input the script provided above into this new file.
3. Open your terminal and ensure you are within the my_env virtual environment.
4. Execute the following code in the terminal to run the application.



