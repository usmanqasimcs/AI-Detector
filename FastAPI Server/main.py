from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

# Load model and vectorizer
model = joblib.load("ai_text_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = FastAPI()

# Input schema
class InputText(BaseModel):
    text: str
@app.post("/predict")
def predict_text(input_data: InputText):
    try:
        text_vector = vectorizer.transform([input_data.text])
        prediction = model.predict(text_vector)[0]
        probability = model.predict_proba(text_vector)[0].max()
        return {
            "label": int(prediction),
            "confidence": float(round(probability, 4))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))