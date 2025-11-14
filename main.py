import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json()
    tag = req.get('fulfillmentInfo', {}).get('tag')
    response_text = 'Webhook test successful!' if tag == 'testTag' else 'Default response from webhook.'
    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [response_text]}}]
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Use PORT from environment
    app.run(host='0.0.0.0', port=port)
