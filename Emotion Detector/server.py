"""
This module contains server initiating, the routes, etc
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

@app.route("/")
def index():
    """
    Main method for generating landing page
    """
    return render_template("index.html")

@app.route("/emotionDetector")
def emotion_detection():
    """
    Method as endpoint to detect emotion from string input
    """
    text_to_analyze = request.args.get('textToAnalyze')
    result = emotion_detector(text_to_analyze)
    if result['dominant_emotion'] is not None:
        text = (
            f"For the given statement, the system response is"
            f"'anger': {result['anger']},"
            f"'disgust': {result['disgust']},"
            f"'fear': {result['fear']},"
            f"'joy': {result['joy']} and"
            f"'sadness': {result['sadness']}. The dominant emotion is"
            f"{result['dominant_emotion']}."
            )
        return text

    return "Invalid text! Please try again!"

if __name__ == "__main__":
    app.run(debug=True)
