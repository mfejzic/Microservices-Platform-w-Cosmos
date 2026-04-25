from flask import Flask, request, jsonify                           # jsonify is a helper function that creates proper json http response --  requests lets app access incoming http request data, like json, or input
import requests                                                     # imports library to send https requests to other API's or services, in this case to cognitive AI
import os

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)



# prometheus and grafana API URL
REQUEST_COUNT = Counter('request_count', 'Total request count')

@app.route('/metrics')
def metrics():
    REQUEST_COUNT.inc()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)



# check the container env in main for these vars
AZURE_ENDPOINT = os.environ.get("COG_ENDPOINT")                                   # sets the API's url endpoint
AZURE_KEY = os.environ.get("COG_KEY")                                             # holds API key to auth reuestts

@app.route("/analyze", methods=["POST"])                                          # this is a route decorator - it tells flask when a POST https request goes to the analyze path, call the function below to handle it
def analyze_sentiment():                                                          # method calls cognitive AI to get a sentiment, returns sentiment back as a json
    data = request.get_json()                                                     # reads incoming request and converts it to python dictionary
    message = data.get("message")                                                 # extracts the 'message' from the dictionary - this will go to sentiment to analyze

    # prints debuggin info to console
    print(f"[DEBUG] Calling: {AZURE_ENDPOINT}/text/analytics/v3.1/sentiment")     # prints the API url
    print(f"[DEBUG] Sent text: {message}")                                        # prints the message being sent
 
    # prepars http request headers needed for api
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,                                  # api key header for auth - find this in main
        "Content-Type": "application/json"                                       # will always come through in json
    }

    body = {                                                                 # this constructs the json body payload being sent to sentiment analysis
        "documents": [                                                       # 'documents' is part of azures API design
            {
                "language": "en",                                            # english
                "id": "1",
                "text": message                                              # refers to message var from the route 
            }
        ]
    }

    response = requests.post(                                               # sends an http post reqeust to cognitive AI API using the requests library
        f"{AZURE_ENDPOINT}/text/analytics/v3.1/sentiment",                  # send the json body and auth headers
        headers=headers,
        json=body
    )

    print(f"[DEBUG] Status: {response.status_code}")                       # prints http status - 200 means ok
    print(f"[DEBUG] Response: {response.text}")                            # prints raw jso body as text - here we see any errors

    if response.status_code == 200:                                        # checks if api call was successful - if so move to next line
        result = response.json()                                           # turns the json into a python dictionary
        sentiment = result["documents"][0]["sentiment"]                    # gets the list of analyzed documents, 0 picks the first and only list, sentiment adds positive, neutral, or negative
        scores = result["documents"][0]["confidenceScores"]                # adds scores to document
        return jsonify({"sentiment": sentiment, "scores": scores})         # creates new json response to send back to client that requests the /analyze path
    else:
        return jsonify({"sentiment": "N/A", "scores": {}}), 500            # returns n/a and 500 internal server error

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)