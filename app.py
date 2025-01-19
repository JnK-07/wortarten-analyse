from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)

nlp = spacy.load("de_core_news_sm")

# Mapping of POS tags to categories and subcategories
CATEGORY_MAPPING = {
    "ADJ": ("Adjektive", "steigerbare"),
    "AUX": ("Verben", "Hilfsverben"),
    "NOUN": ("Substantive", "konkrete"),
    "DET": ("Artikel", "bestimmte"),
    "PRON": ("Pronomen", "Personalpronomen"),
    "VERB": ("Verben", "Vollverben"),
    "ADV": ("Adverbien", "modal"),
    "ADP": ("Präpositionen", None),
    "CCONJ": ("Konjunktionen", "nebenordnend"),
    "SCONJ": ("Konjunktionen", "unterordnend"),
    "INTJ": ("Interjektionen", None),
    "NUM": ("Numerale", "Kardinalzahlen"),
    "PUNCT": ("Satzzeichen", None),
    "PROPN": ("Substantive", "Eigennamen"),
    "SYM": ("Symbole", None),
    "X": ("Unbekannt", None),
}

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        sentence = data.get("sentence", "")

        if not sentence:
            return jsonify({"error": "Kein Satz angegeben."}), 400

        doc = nlp(sentence)
        result = []

        for token in doc:
            pos = token.pos_
            category, subcategory = CATEGORY_MAPPING.get(pos, ("Nicht definiert", "Keine Unterkategorie"))

            if category == "Adverbien":
                if token.text in ["weil", "deshalb", "wegen"]:
                    subcategory = "kausal"
                elif token.text in ["hier", "dort", "überall"]:
                    subcategory = "lokal"
                elif token.text in ["so", "sehr", "gerne", "nicht"]:
                    subcategory = "modal"
                elif token.text in ["jetzt", "bald", "gestern"]:
                    subcategory = "temporal"

            result.append({
                "word": token.text,
                "category": category,
                "subcategory": subcategory,
                "lemma": token.lemma_,
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Fehler bei der Verarbeitung des Satzes.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
