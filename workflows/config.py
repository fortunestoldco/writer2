from typing import Dict, Any, List
from pydantic import BaseModel

class WorkflowConfig(BaseModel):
    graph_id: str
    phases: List[str]
    transitions: Dict[str, str]
    timeout: int = 600
    retry_attempts: int = 3

WORKFLOW_CONFIGS = {
    "story_creation": WorkflowConfig(
        graph_id="story_creation",
        phases=[
            "initialization",
            "development",
            "creation",
            "refinement",
            "finalization"
        ],
        transitions={
            "initialization": "development",
            "development": "creation",
            "creation": "refinement",
            "refinement": "finalization"
        }
    )
}