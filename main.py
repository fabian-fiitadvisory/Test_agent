import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    req = request.get_json(silent=True) or {}

    # Accept both formats:
    # - Playbook/OpenAPI tool: {"tag": "..."}
    # - Dialogflow CX webhook: {"fulfillmentInfo": {"tag": "..."}}
    tag = req.get("tag") or (req.get("fulfillmentInfo") or {}).get("tag", "")

    # Accept user message from multiple formats
    user_text = (
        req.get("user_message")
        or (((req.get("payload") or {}).get("user_message")) if isinstance(req.get("payload"), dict) else None)
        or (req.get("sessionInfo", {}).get("parameters", {}).get("user_message"))
        or ""
    )

    if tag == "testTag":
        response_text = "Webhook test successful!"
    elif tag == "triage":
        if user_text:
            response_text = f"Ik heb je bericht ontvangen: '{user_text}'. (triage-logica komt hier)"
        else:
            response_text = "Ik heb je bericht ontvangen, maar ik zie geen tekst. Kun je je klacht in 1 zin omschrijven?"
    else:
        response_text = f"Reached webhook. Tag={tag or 'EMPTY'}"

    return jsonify({
        "ok": True,
        "tag": tag,
        "user_message": user_text,
        "message": response_text,
        
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [response_text]}}
            ]
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
