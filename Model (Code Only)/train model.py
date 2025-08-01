import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Load Dataset
df = pd.read_csv("AI_Human.csv")
df = df.dropna(subset=["text", "generated"])  # Drop rows with missing values

# 2. Rename 'generated' to 'label' for clarity
df.rename(columns={"generated": "label"}, inplace=True)

# Optional: shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# 3. Features and Labels
X_text = df["text"]
y = df["label"]

# 4. Text Vectorization
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words="english"
)
X = vectorizer.fit_transform(X_text)

# 5. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Train Classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 7. Evaluate Model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 8. Save Model and Vectorizer
joblib.dump(model, "ai_text_classifier.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Training complete. Model and vectorizer saved.")
