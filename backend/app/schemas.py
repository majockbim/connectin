from pydantic import BaseModel

class PromptRequest(BaseModel):
    url: str
