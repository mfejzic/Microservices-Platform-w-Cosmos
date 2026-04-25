from flask import Flask, request, jsonify
import os
from twilio.rest import Client                                       # imports Twilio's SDK

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)                                                # initializes new flask app instance


# prometheus and grafana API URL
REQUEST_COUNT = Counter('request_count', 'Total request count')

@app.route('/metrics')
def metrics():
    REQUEST_COUNT.inc()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)



@app.route("/trigger", methods=["POST"])                             # defines route handler for this endpoint /trigger
def trigger():                                                       # when trigger URL is hit, it will run the function below
    try:
        # Twilio settings from env vars                              # find these in trigger container in main.tf
        TWILIO_SID = os.environ.get("TWILIO_SID")
        TWILIO_FROM = os.environ.get("TWILIO_FROM")
        TWILIO_TO = os.environ.get("TWILIO_TO")
        TWILIO_AUTH = os.environ.get("TWILIO_AUTH")


        client = Client(TWILIO_SID, TWILIO_AUTH)                    # initializes twilio rest client using these 2 credentials
        client.messages.create(                                      # this will send SMS messages
            body="New message in chat board",
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )

        return jsonify({"status": "SMS sent"}), 200               # if it works, this will send back the 200 code and json payload

    except Exception as e:
        return jsonify({"error": str(e)}), 500                    # if didnt work, will return 500 error code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
