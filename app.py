
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.json
    text = data.get("text", "")
    language = data.get("language", "de")

    prompt = {
        "de": f"Formuliere diesen Text so um, dass keine sensiblen Daten enthalten sind: '{text}'",
        "en": f"Rewrite this text to avoid sharing any sensitive or personal data: '{text}'",
        "fr": f"Réécris ce texte pour éviter de divulguer des données sensibles: '{text}'",
        "es": f"Reescribe este texto para evitar compartir datos sensibles o personales: '{text}'"
    }.get(language, text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        rewritten = response.choices[0].message.content.strip()
        return jsonify({"rewritten": rewritten})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
