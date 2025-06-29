from fastapi import APIRouter
from app.schemas import PromptRequest
from app.prompt_engine import generate_prompt

router = APIRouter()

@router.post("/generate-prompt")
async def generate_prompt_endpoint(data: PromptRequest):
    print(f"Received request for URL: {data.url}")
    prompts = generate_prompt(data.url)
    return {"prompts": prompts}
