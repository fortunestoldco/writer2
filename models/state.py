from datetime import datetime
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field


class ProjectState(BaseModel):
    project_id: str
    title: str
    current_phase: str
    status: str
    last_update: datetime = Field(default_factory=datetime.utcnow)
    quality_metrics: Dict[str, float] = Field(default_factory=dict)
    phase_history: List[str] = Field(default_factory=list)
    feedback: List[Dict] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My Novel",
                "current_phase": "initialization",
                "status": "in_progress",
            }
        }


class StoryState(BaseModel):
    title: str
    genre: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    current_phase: str
    initialization_complete: bool = False
    world_building_complete: bool = False
    character_development_complete: bool = False
    plot_development_complete: bool = False
    scene_creation_complete: bool = False
    refinement_complete: bool = False
    final_review_complete: bool = False
    
    def validate_phase_completion(self, phase: str) -> bool:
        return getattr(self, f"{phase}_complete", False)
