NLP sentiment analysis is the practice of using computers to recognize sentiment or emotion expressed in a text. Through NLP, sentiment analysis categorizes words as positive, negative or neutral.

Sentiment analysis is often performed on textual data to help businesses monitor brand and product sentiment in customer feedback, and understanding customer needs. It helps attain the attitude and mood of the wider public which can then help gather insightful information about the context.

For creating the sentiment analysis application, we'll be making use of the Watson Embedded AI Libraries. Instead, we need to send a POST request to the relevant model with the required text and the model will send the appropriate response.

```
import requests
def <function_name>(<input_args>):
    url = '<relevant_url>'
    headers = {<header_dictionary>}
    myobj = {<input_dictionary_to_the_function>}
    response = requests.post(url, json = myobj, headers=header)
    return response.text
```

The response of the Watson NLP functions is in the form of an object. For accessing the details of the response, we can use text attribute of the object by calling response.text and make the function return the response as simple text.

The output of the application created is in the form of a dictionary, but has been formatted as a text. To access relevant pieces of information from this output, we need to first convert this text into a dictionary. Since dictionaries are the default formatting system for JSON files, we make use of the in-built Python library json.

Now, pass the response variable as an argument to the json.loads function and save the output in formatted_response. Print formatted_response to see the difference in the formatting.