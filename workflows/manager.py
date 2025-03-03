from typing import Dict, Any, List
from agents import (
    ExecutiveDirectorAgent,
    CreativeDirectorAgent,
    WorldBuildingExpert,
    CharacterDesigner,
    PlotArchitect,
    SceneComposer,
    DialogueWriter,
    PacingEditor,
    ContinuityChecker,
    StyleEditor,
    QualityAssessor
)
import structlog

logger = structlog.get_logger(__name__)

class WorkflowManager:
    def __init__(self):
        self.agents = {
            'executive': ExecutiveDirectorAgent(),
            'creative': CreativeDirectorAgent(),
            'world_building': WorldBuildingExpert(),
            'character': CharacterDesigner(),
            'plot': PlotArchitect(),
            'scene': SceneComposer(),
            'dialogue': DialogueWriter(),
            'pacing': PacingEditor(),
            'continuity': ContinuityChecker(),
            'style': StyleEditor(),
            'quality': QualityAssessor()
        }
        
        # Define workflow phases and their agents
        self.workflow_phases = [
            {
                'name': 'initialization',
                'agents': ['executive', 'creative'],
                'required_fields': ['title', 'genre']
            },
            {
                'name': 'world_building',
                'agents': ['world_building'],
                'required_fields': ['creative_direction']
            },
            {
                'name': 'character_development',
                'agents': ['character'],
                'required_fields': ['world_building']
            },
            {
                'name': 'plot_development',
                'agents': ['plot'],
                'required_fields': ['characters']
            },
            {
                'name': 'scene_creation',
                'agents': ['scene', 'dialogue'],
                'required_fields': ['plot_structure']
            },
            {
                'name': 'refinement',
                'agents': ['pacing', 'continuity', 'style'],
                'required_fields': ['scenes', 'scene_dialogues']
            },
            {
                'name': 'final_review',
                'agents': ['quality'],
                'required_fields': ['style_metrics', 'continuity_analysis']
            }
        ]
    
    def _validate_state(self, state: Dict[str, Any], required_fields: List[str]) -> None:
        """Validate that required fields are present in state."""
        missing_fields = [
            field for field in required_fields 
            if field not in state
        ]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
    
    async def execute_phase(self, phase: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all agents in a single phase."""
        try:
            for agent_name in phase['agents']:
                try:
                    agent = self.agents[agent_name]
                    state = await agent.invoke(state)
                    self.logger.info(
                        "agent_complete",
                        phase=phase['name'],
                        agent=agent_name
                    )
                except Exception as e:
                    self.logger.error(
                        "agent_failed",
                        phase=phase['name'],
                        agent=agent_name,
                        error=str(e)
                    )
                    raise
            return state
        except Exception as e:
            self.logger.error(
                "phase_failed",
                phase=phase['name'],
                error=str(e)
            )
            raise
    
    async def create_story(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete story creation workflow."""
        state = initial_state.copy()
        
        try:
            for phase in self.workflow_phases:
                state = await self.execute_phase(phase, state)
                
                logger.info(
                    "phase_complete",
                    phase=phase['name'],
                    status="success"
                )
            
            return {
                "status": "success",
                "story": state
            }
            
        except Exception as e:
            logger.error("workflow_failed", error=str(e))
            return {
                "status": "error",
                "error": str(e),
                "phase": state.get('current_phase', 'unknown')
            }