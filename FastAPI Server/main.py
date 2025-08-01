from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

# Load model and vectorizer
model = joblib.load("ai_text_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Input schema
class InputText(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "AI Text Detector API is running!", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Text Detector API"}

@app.post("/detect")
def detect_text(input_data: InputText):
    try:
        text_vector = vectorizer.transform([input_data.text])
        prediction = model.predict(text_vector)[0]
        probability = model.predict_proba(text_vector)[0].max()
        
        # Convert prediction to human-readable format
        prediction_label = "Human" if prediction == 1 else "AI"
        confidence_percentage = float(round(probability * 100, 1))
        
        return {
            "prediction": prediction_label,
            "confidence": confidence_percentage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))