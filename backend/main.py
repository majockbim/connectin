from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .app.utils.scraper import extract_linkedin_text
from .app.prompt_engine import generate_questions  # Fixed import path

app = FastAPI()

class ProfileLinks(BaseModel):
    learner_url: str
    mentor_url: str

@app.post("/generate")
def generate(data: ProfileLinks):
    try:
        learner_text = extract_linkedin_text(data.learner_url)
        mentor_text = extract_linkedin_text(data.mentor_url)
        questions = generate_questions(learner_text, mentor_text)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
def root():
    return {"message": "LinkedIn Coffee Chat Question Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)