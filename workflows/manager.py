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
    
    async def execute_phase(self, phase: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all agents in a single phase."""
        try:
            logger.info(f"starting_phase", phase=phase['name'])
            
            # Verify required fields
            missing_fields = [
                field for field in phase['required_fields']
                if field not in state
            ]
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            # Execute each agent in the phase
            for agent_name in phase['agents']:
                agent = self.agents[agent_name]
                state = await agent.invoke(state)
                
                logger.info(
                    "agent_complete",
                    phase=phase['name'],
                    agent=agent_name
                )
            
            state['current_phase'] = phase['name']
            state[f"{phase['name']}_complete"] = True
            
            return state
            
        except Exception as e:
            logger.error(
                "phase_execution_failed",
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