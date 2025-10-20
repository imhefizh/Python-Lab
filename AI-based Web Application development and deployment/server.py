''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''
from flask import Flask, render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer

app = Flask("Sentiment Analyzer")

@app.route("/sentimentAnalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analysis()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyse = request.args.get('textToAnalyze')
    result = sentiment_analyzer(text_to_analyse)
    try:
        return (
            f"The given text has been identified as {result['label'][5:]} "
            f"with a score of {result['score']}."
        )
    except Exception as e:
        return f"Invalid input ! Try again. <br/><br/> Log: {result}"

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
