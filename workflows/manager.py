from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from agents import AgentFactory
import structlog
from .config import WORKFLOW_CONFIGS

logger = structlog.get_logger(__name__)

class WorkflowManager:
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        
    async def create_story(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the story creation workflow."""
        config = WORKFLOW_CONFIGS["story_creation"]
        current_phase = "initialization"
        state = input_data.copy()
        
        try:
            while current_phase != "complete":
                # Get the appropriate graph for current phase
                graph = self._create_phase_graph(current_phase)
                
                # Execute phase
                state = await graph.ainvoke(
                    state,
                    {"metadata": {"agent_factory": self.agent_factory}}
                )
                
                # Check completion and transition
                if state.get(f"{current_phase}_complete"):
                    current_phase = config.transitions.get(
                        current_phase, "complete"
                    )
                else:
                    logger.error(
                        "phase_failed",
                        phase=current_phase,
                        state=state
                    )
                    return {
                        "status": "error",
                        "phase": current_phase,
                        "error": f"Failed to complete {current_phase} phase"
                    }
            
            return {
                "status": "success",
                "story": state.get("story"),
                "metadata": {
                    "title": state.get("title"),
                    "quality_metrics": state.get("quality_metrics")
                }
            }
            
        except Exception as e:
            logger.error(
                "workflow_error",
                error=str(e),
                phase=current_phase
            )
            return {"status": "error", "error": str(e)}