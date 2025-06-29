# Endpoint definitions

from fastapi import APIRouter
from app.prompt_engine import generate_prompt

router = APIRouter()

@router.post("/generate-prompt")
async def generate_prompt_endpoint(data: dict):
    linkedin_url = data.get("url")
    return {"promtpts": generate_prompt(linkedin_url)}
