from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from dependencies import get_agent_factory
from workflows import create_story
from models.request import StoryRequest
from models.response import StoryResponse

router = APIRouter(prefix="/story", tags=["story"])

@router.post("/create", response_model=StoryResponse)
async def create_new_story(
    request: StoryRequest,
    agent_factory = Depends(get_agent_factory)
) -> Dict[str, Any]:
    """Create a new story using the LangGraph workflow."""
    config = {"metadata": {"agent_factory": agent_factory}}
    result = await create_story(request.dict(), config)
    
    if result["status"] != "success":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result