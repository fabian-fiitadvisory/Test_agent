import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    req = request.get_json(silent=True) or {}
    tag = (req.get("fulfillmentInfo") or {}).get("tag", "")

    if tag == "testTag":
        response_text = "Webhook test successful!"
    else:
        response_text = f"Reached webhook. Tag={tag or 'EMPTY'}"

    return jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [response_text]}}
            ]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
