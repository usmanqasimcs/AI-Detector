from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import re
from typing import Dict

app = FastAPI(title="AI Text Detector API", version="1.0.0")

# Add CORS middleware to allow requests from your React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class DetectionResult(BaseModel):
    prediction: str  # "Human" or "AI"
    confidence: float  # 0-100

def analyze_text_patterns(text: str) -> Dict[str, float]:
    """
    Simple heuristic-based analysis for demonstration.
    In a real implementation, you'd use a trained ML model.
    """
    # Basic text statistics
    word_count = len(text.split())
    sentence_count = len([s for s in re.split(r'[.!?]+', text) if s.strip()])
    avg_word_length = sum(len(word) for word in text.split()) / max(word_count, 1)
    avg_sentence_length = word_count / max(sentence_count, 1)
    
    # Simple scoring (this is just for demonstration)
    scores = {
        'repetition': check_repetition(text),
        'complexity': check_complexity(text),
        'coherence': check_coherence(text),
        'formality': check_formality(text)
    }
    
    return scores

def check_repetition(text: str) -> float:
    """Check for repetitive patterns (AI text often has more repetition)"""
    words = text.lower().split()
    if len(words) < 10:
        return 0.5
    
    unique_words = len(set(words))
    repetition_score = unique_words / len(words)
    return repetition_score

def check_complexity(text: str) -> float:
    """Check sentence and word complexity"""
    words = text.split()
    if not words:
        return 0.5
    
    # Count complex words (>6 characters)
    complex_words = sum(1 for word in words if len(word) > 6)
    complexity_ratio = complex_words / len(words)
    return complexity_ratio

def check_coherence(text: str) -> float:
    """Simple coherence check based on sentence transitions"""
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if len(sentences) < 2:
        return 0.5
    
    # Simple heuristic: check for transition words
    transition_words = ['however', 'therefore', 'furthermore', 'moreover', 'consequently', 'additionally', 'meanwhile', 'nevertheless']
    transition_count = sum(1 for sentence in sentences for word in transition_words if word in sentence.lower())
    
    return min(transition_count / len(sentences), 1.0)

def check_formality(text: str) -> float:
    """Check for formal vs informal language patterns"""
    formal_indicators = ['furthermore', 'consequently', 'therefore', 'moreover', 'nevertheless', 'subsequently']
    informal_indicators = ['gonna', 'wanna', 'yeah', 'ok', 'lol', 'btw', 'omg']
    
    words = text.lower().split()
    formal_count = sum(1 for word in words if word in formal_indicators)
    informal_count = sum(1 for word in words if word in informal_indicators)
    
    total_indicators = formal_count + informal_count
    if total_indicators == 0:
        return 0.5
    
    return formal_count / total_indicators

def make_prediction(text: str) -> DetectionResult:
    """
    Make AI/Human prediction based on text analysis.
    This is a simplified demonstration - replace with your actual ML model.
    """
    if len(text.strip()) < 10:
        # Too short to analyze reliably
        return DetectionResult(
            prediction="Human",
            confidence=50.0
        )
    
    # Analyze text patterns
    scores = analyze_text_patterns(text)
    
    # Simple scoring algorithm (replace with your ML model)
    ai_indicators = 0
    human_indicators = 0
    
    # AI text often has:
    # - Lower repetition (more diverse vocabulary)
    # - Higher formality
    # - More consistent patterns
    
    if scores['repetition'] > 0.7:  # High vocabulary diversity
        ai_indicators += 1
    else:
        human_indicators += 1
    
    if scores['formality'] > 0.3:  # Formal language
        ai_indicators += 1
    else:
        human_indicators += 1
    
    if scores['coherence'] > 0.2:  # Good transitions
        ai_indicators += 1
    else:
        human_indicators += 1
    
    # Add some randomness for demonstration
    random_factor = random.uniform(-0.1, 0.1)
    
    # Calculate final score
    ai_score = (ai_indicators / 3.0) + random_factor
    
    if ai_score > 0.5:
        prediction = "AI"
        confidence = min(95.0, max(55.0, ai_score * 100 + random.uniform(-10, 10)))
    else:
        prediction = "Human"
        confidence = min(95.0, max(55.0, (1 - ai_score) * 100 + random.uniform(-10, 10)))
    
    return DetectionResult(prediction=prediction, confidence=round(confidence, 1))

@app.get("/")
async def root():
    return {"message": "AI Text Detector API", "status": "running"}

@app.post("/detect", response_model=DetectionResult)
async def detect_ai_text(input_data: TextInput):
    """
    Analyze text and return AI detection results.
    """
    try:
        if not input_data.text or not input_data.text.strip():
            raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
        if len(input_data.text) > 10000:  # Limit text length
            raise HTTPException(status_code=400, detail="Text too long (max 10,000 characters)")
        
        result = make_prediction(input_data.text)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Text Detector API is running"}

if __name__ == "__main__":
    import uvicorn
    print("Starting AI Text Detector API server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
