from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

# Flask-App erstellen
app = Flask(__name__)
CORS(app)  # CORS aktivieren

# Lade das deutsche Sprachmodell
nlp = spacy.load("de_core_news_sm")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    sentence = data.get("sentence", "")

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    # Verarbeite den Satz mit spaCy
    doc = nlp(sentence)
    result = [{"word": token.text, "pos": token.pos_} for token in doc]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
