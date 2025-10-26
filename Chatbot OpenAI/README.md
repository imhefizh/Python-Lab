## Prequisites
- Node and Express are two technologies that are commonly used to create web applications.
- Node is a runtime environment that allows you to run JavaScript code on the server side, without a browser.
- Express is a framework that provides a set of features and tools to simplify the development of web applications with Node.

Some of the benefits of using Node and Express are:
- They are fast and scalable, as they use an event-driven, non-blocking I/O model that can handle many concurrent requests.
- They are flexible and modular, as they allow you to use various libraries and middleware to customize your application according to your needs.
- They are easy to learn and use, as they are based on JavaScript, which is a popular and widely used programming language.

## Task 1: Set Up Your Project
- Step 1: Open a terminal, click on "Terminal", and then select the "New Terminal" option.
- Step 2: Create a new directory for your project named `software-dev-chatbot`, navigate to the directory, and initialize a Node.js project using the commands below.
```
npm init -y
```
- Step 3: Install express and openai dependencies by executing the following command.
```
npm install express openai
```
- Step 4: Create a new directory named `public` inside a project directory using the below command.
```
mkdir public
```

## Task 2: Create the user interface for your chatbot using HTML and CSS
Create an `index.html` file within the public directory, right-click on the public folder, and select the "New File" option, this file will function as the user interface for your chatbot.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Software Dev Chatbot</title>
</head>
<body>
    <div class="main-container">
        <div class="chat-container">
            <div class="header">
                <img src="chat.png" alt="Logo" class="logo">
                <h2 class="name">Chat Window</h2>
            </div>
            <div class="chat-log" id="chat-log"></div>
            <div class="input-container">
                <input type="text" id="user-input" placeholder="Ask me anything...">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>
    <script src="main.js"></script> 	
</body>
</html>
```
Create a `style.css` file in the `public` directory and insert the following code into the CSS file.

```css
.chat-container {
    max-width: 600px;
    margin: 20px auto;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 80vh;
    position: relative;
    background: linear-gradient(to bottom, #1e5799, #2989d8);
}
.logo {
    width: auto;
    height: 50px;
    margin-left: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    border-radius: 50px;
}
.name {
    font-size: 20px;
    font-weight: bold;
    margin: 10px;
    color: #fff;
    margin-left: 10px;
    margin-right: 10px;
}
.chat-window {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding: 20px;
    background-color: #fff;
overflow-y: auto;
}
.input-container {
    display: flex;
    align-items: center;
    padding: 20px;
    background-color: #fff;
}
input[type="text"] {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    outline: none;
    font-size: 16px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
.chat-log {
    height: 400px;
    padding: 20px;
    overflow-y: auto;
    background-color: rgba(255, 255, 255, 0.8);
}
/* Added space between user prompts */
.chat-log p {
    margin: 10px 0;
}
.input-container input[type="text"] {
    flex: 1;
    height: 40px;
    padding: 5px 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
    outline: none;
}
.input-container button {
    margin-left: 10px;
    padding: 8px 16px;
border: none;
border-radius: 5px;
background-color: #4CAF50;
color: #fff;
 font-size: 16px;
 cursor: pointer;
}
.input-container button:hover {
    background-color: #45a049;
}
html, body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}
```

## Task 3: Create a JavaScript file to implement the functionality of the Chatbot
- Create a `main.js` file in the public directory to implement the functionality.
- In the `main.js` file, the JavaScript code is designed to handle user input and initiate an API call to the OpenAI API.
- An event listener is attached to the submit button so that when the user clicks it, the code is executed.
- In the event listener callback function, we retrieve the user's input from the text input element and display their message in the chat log
- Next, we make an API request to the server with the user's message using the `fetch()` function, specifying the appropriate endpoint on the server to receive this request.
- After receiving the response from the OpenAI API, we send it back to the client and display the chatbot's response in the text area of the `index.html` file.
- We then append the response to the chat log on the front end, making the conversation visible on the UI (User Interface).

Insert the following code into the newly created `main.js` file.

```javascript title:"main.js"
const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
function sendMessage() {
    const message = userInput.value;
    // Display user's message
    displayMessage('user', message);
    // Call OpenAI API to get chatbot's response
    getChatbotResponse(message);
    // Clear user input
    userInput.value = '';
}
function displayMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    // Wrap the message in a <p> tag
    const messageParagraph = document.createElement('p');
    messageParagraph.innerText = message;
    // Append the <p> tag to the message element
    messageElement.appendChild(messageParagraph);
    chatLog.appendChild(messageElement);
}
function getChatbotResponse(userMessage) {
    // Make a request to your server with the user's message
    fetch('/getChatbotResponse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Display chatbot's response
        displayMessage('chatbot', data.chatbotResponse);
    })
    .catch(error => console.error('Error:', error));
}
```

## Task 4: Create an Express Server and integrate OpenAI API
- Create a new file named `server.js` within your project directory (software-dev-chatbot)
- This file will be responsible for managing API requests and integrating with OpenAI.
- This code sets up a basic Express.js server that serves static files from a `public` directory.
- It includes a route for the root path ('/') to serve an HTML file.
- Additionally, there is a POST endpoint `/getChatbotResponse` that receives a user message, utilizes an OpenAI API wrapper (`OpenAIAPI`), generates a chatbot response using the OpenAI API, and sends the response back to the client.
- The server listens on a specified port 3000, and a message is logged to the console when the server is successfully running.

```Javascript title:"server.js"
process.env["NODE_TLS_REJECT_UNAUTHORIZED"]=0;
const express = require('express');
const path = require('path');
const { OpenAIAPI } = require('./openai');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/getChatbotResponse', async (req, res) => {
    const userMessage = req.body.userMessage;

    // Use OpenAI API to generate a response
    const chatbotResponse = await OpenAIAPI.generateResponse(userMessage);

    // Send the response back to the client
    res.json({ chatbotResponse });
});
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
```

## Task 5: Create OpenAI API Module
Create an `openai.js` file within the project directory to encapsulate the OpenAI API logic.

This code facilitates communication with the OpenAI API, specifically the gpt-3.5-turbo Codex engine, allowing developers to generate responses based on user input through a secure configuration using an API key.
```Javascript
class OpenAIAPI {
    static async generateResponse(userMessage, conversationHistory = []) {
        const apiKey = process.env.OPENAI_API_KEY;
        const endpoint = 'https://api.openai.com/v1/chat/completions';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
            },
            body: JSON.stringify({
                model: "gpt-3.5-turbo-1106",
                messages: conversationHistory.concat([{ role: 'user', content: userMessage }]),
                max_tokens: 150
            }),
        });
        const responseData = await response.json();
        // Log the entire API response for debugging
        console.log('Response from OpenAI API:', responseData.choices[0].message);
        // Check if choices array is defined and not empty
        if (responseData.choices && responseData.choices.length > 0 && responseData.choices[0].message) {
            return responseData.choices[0].message.content;
        } else {
            // Handle the case where choices array is undefined or empty
            console.error('Error: No valid response from OpenAI API');
            return 'Sorry, I couldn\'t understand that.';
        }
    }
}
module.exports = { OpenAIAPI };
```


