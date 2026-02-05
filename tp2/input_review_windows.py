from flask import Flask, request, render_template_string
import joblib

# Charger le modèle et le vectorizer entraînés dans tp2.py
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

app = Flask(__name__)

HTML = """
<h2>Saisir un avis Allociné</h2>
<form method="post">
  <textarea name="text" rows="6" cols="60" placeholder="Écris ton avis ici..."></textarea><br><br>
  <button type="submit">Envoyer</button>
</form>

{% if review %}
<hr>
<h3>Avis saisi :</h3>
<p>{{ review }}</p>

<h3>Résultat :</h3>
<p><b>{{ result }}</b></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    review = None
    result = None

    if request.method == "POST":
        review = request.form["text"]

        # Classification
        X_new = vectorizer.transform([review]).toarray()
        pred = model.predict(X_new)[0]
        result = "POSITIF" if pred == 1 else "NÉGATIF"

    return render_template_string(HTML, review=review, result=result)

app.run(host="0.0.0.0", port=5008, debug=False)