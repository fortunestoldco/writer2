from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from workflows.manager import WorkflowManager
from dependencies import get_workflow_manager
from models.request import StoryRequest
from models.response import StoryResponse

router = APIRouter(prefix="/story", tags=["story"])

@router.post("/create", response_model=StoryResponse)
async def create_new_story(
    request: StoryRequest,
    workflow_manager: WorkflowManager = Depends(get_workflow_manager)
) -> Dict[str, Any]:
    """Create a new story using the workflow manager."""
    result = await workflow_manager.create_story(request.dict())
    
    if result["status"] != "success":
        raise HTTPException(
            status_code=500,
            detail={"message": "Story creation failed", "error": result["error"]}
        )
    
    return result