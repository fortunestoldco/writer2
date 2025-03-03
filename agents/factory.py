from typing import Dict, Any
from langchain.agents import AgentExecutor  # Updated import
from langchain_core.agents import Tool
from langchain_anthropic import ChatAnthropic
import structlog
from .base import BaseAgent
from .executive_director import ExecutiveDirectorAgent
from .creative_director import CreativeDirectorAgent
from .world_building import WorldBuildingExpert
from .character_designer import CharacterDesigner
from .plot_architect import PlotArchitect
from .scene_composer import SceneComposer
from .dialogue_writer import DialogueWriter
from .pacing_editor import PacingEditor
from .continuity_checker import ContinuityChecker
from .style_editor import StyleEditor
from .quality_assessor import QualityAssessor

logger = structlog.get_logger(__name__)

class AgentFactory:
    """Factory for creating and managing agents."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all available agents."""
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
    
    def get_agent(self, agent_type: str) -> BaseAgent:
        """Get an agent instance by type."""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return self.agents[agent_type]