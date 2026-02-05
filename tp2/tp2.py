from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    f1_score,
)
from sklearn.naive_bayes import GaussianNB
import joblib

# Chargement du dataset
ds = load_dataset("allocine", cache_dir="./hf_cache")
df = ds["train"].to_pandas()
df_test = ds["test"].to_pandas()

reviews = df["review"].tolist()
labels = df["label"].tolist()

reviews_test = df_test["review"].tolist()
labels_test = df_test["label"].tolist()

# Vectorisation (correcte)
vectorizer = TfidfVectorizer(max_features=500)
X_train = vectorizer.fit_transform(reviews).toarray()
y_train = labels

X_test = vectorizer.transform(reviews_test).toarray()
y_test = labels_test

# Modèle
model = GaussianNB()
model.fit(X_train, y_train)

# Évaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print("Accuracy:", accuracy)
print("F1 Score:", f1)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

