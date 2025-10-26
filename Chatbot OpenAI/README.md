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

