from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Lade das Sprachmodell
nlp = spacy.load("de_core_news_sm")

# Route für die Wortarten-Analyse
@app.route('/analyze', methods=['POST'])
def analyze():
    # Hole den JSON-Body aus der Anfrage
    data = request.json
    sentence = data.get("sentence", "")

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    # Analysiere den Satz mit spaCy
    doc = nlp(sentence)
    result = [{"word": token.text, "pos": token.pos_} for token in doc]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
