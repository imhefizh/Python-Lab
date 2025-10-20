"""
This module consists of emotion detector method
"""
import json
import requests

def emotion_detector(text_to_analyse):
    """
    This method detects emotion from a string
    """
    url= (
        'https://sn-watson-emotion.labs.skills.network/'
        'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    header= {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    body= { "raw_document": { "text": text_to_analyse } }
    response = requests.post(url, json = body, headers = header, timeout = 15)
    formatted_response = json.loads(response.text)
    anger_score = formatted_response['emotionPredictions'][0]['emotion']['anger']
    disgust_score = formatted_response['emotionPredictions'][0]['emotion']['disgust']
    fear_score = formatted_response['emotionPredictions'][0]['emotion']['fear']
    joy_score = formatted_response['emotionPredictions'][0]['emotion']['joy']
    sadness_score = formatted_response['emotionPredictions'][0]['emotion']['sadness']
    result = {
       'anger': float(anger_score),
        'disgust': float(disgust_score),
        'fear': float(fear_score),
        'joy': float(joy_score),
        'sadness': float(sadness_score),
        'dominant_emotion': 0
    }
    dominant_emotion = ''
    prev = 0
    for key, value in result.items():
        if (prev < value):
            dominant_emotion = key
            prev = value
    result['dominant_emotion'] = dominant_emotion
    return result
