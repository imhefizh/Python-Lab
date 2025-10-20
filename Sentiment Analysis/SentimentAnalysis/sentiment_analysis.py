"""
This module contains sentiment analysis
"""
import json
import requests

def sentiment_analyzer(text_to_analyse):
    """
    Sentiment Analyzer
    """
    url = (
        'https://sn-watson-sentiment-bert.labs.skills.network/'
        'v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'
    )
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    body =  { "raw_document": { "text": text_to_analyse } }
    response = requests.post(url, json = body, headers = header, timeout=15)
    formatted_response = json.loads(response.text)
    try:
        return (
            {"score": formatted_response['documentSentiment']['score'],
            "label": formatted_response['documentSentiment']['label']}
        )
    except Exception as e:
        return formatted_response
