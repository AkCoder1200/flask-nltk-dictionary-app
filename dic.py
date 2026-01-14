from flask import Flask, render_template, request
from nltk.corpus import wordnet as wn
import nltk

# Download wordnet (run once)
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = ""

    if request.method == "POST":
        word = request.form.get("word", "").strip()

        if not word:
            error = "Please enter a word"
        else:
            meanings = []
            synonyms = set()
            antonyms = set()

            for synset in wn.synsets(word):
                meanings.append(synset.definition())
                for lemma in synset.lemmas():
                    synonyms.add(lemma.name())
                    if lemma.antonyms():
                        antonyms.add(lemma.antonyms()[0].name())

            if not meanings:
                error = "Word not found in dictionary"
            else:
                data = {
                    "word": word,
                    "meanings": meanings,
                    "synonyms": list(synonyms),
                    "antonyms": list(antonyms)
                }

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)

