from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .app.utils.scraper import extract_linkedin_text
from .app.prompt_engine import generate_questions

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ProfileLinks(BaseModel):
    learner_url: str
    mentor_url: str

@app.post("/generate")
def generate(data: ProfileLinks):
    try:
        print(f"Received URLs: learner={data.learner_url}, mentor={data.mentor_url}")
        
        learner_text = extract_linkedin_text(data.learner_url)
        mentor_text = extract_linkedin_text(data.mentor_url)
        questions = generate_questions(learner_text, mentor_text)
        return {"questions": questions}
    except Exception as e:
        print(f"Error details: {str(e)}")
        
        # Fallback: Generate generic questions if scraping fails
        fallback_questions = """1. What advice would you give to someone just starting their career in your industry?

2. What skills or experiences have been most valuable in your professional journey?

3. What trends do you see shaping the future of your field, and how can I prepare for them?"""
        
        return {"questions": f"Note: Could not access LinkedIn profiles ({str(e)}). Here are some generic coffee chat questions:\n\n{fallback_questions}"}

@app.get("/")
def root():
    return {"message": "LinkedIn Coffee Chat Question Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)