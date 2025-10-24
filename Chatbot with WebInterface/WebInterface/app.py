import json
from flask import Flask, request, render_template
from flask_cors import CORS	
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

app = Flask(__name__)
CORS(app)				

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    # Read prompt from HTTP request body
    data = request.get_data(as_text=True)
    data = json.loads(data)

    # Tokenize the input text and history
    
    messages = {"role": "user", "content": data['prompt']}
    conversation_history.append(messages)

    inputs = tokenizer.apply_chat_template(
	    conversation_history,
	    add_generation_prompt=True,
	    tokenize=True,
	    return_dict=True,
	    return_tensors="pt",
    ).to(model.device)

    # Generate the response from the model
    outputs = model.generate(**inputs, max_new_tokens=40)  # max_length will acuse model to crash at some point as history grows

    # Decode the response
    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])

    # Add interaction to conversation history
    conversation_history.append({"role": "assistant", "content": response})
    print(conversation_history)

    return response

if __name__ == '__main__':
    app.run()