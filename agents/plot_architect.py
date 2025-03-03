from typing import Dict, Any, List
from .base import BaseAgent

PLOT_ARCHITECT_PROMPT = """You are the Plot Architect responsible for crafting engaging 
and coherent plot structures. Design the story's plot based on the established elements.

Your output must be valid JSON with the following structure:
{
    "plot_structure": {
        "act_one": {
            "setup": ["Key setup elements"],
            "inciting_incident": "Event that starts the story",
            "plot_points": ["Major events"]
        },
        "act_two": {
            "rising_action": ["Escalating events"],
            "midpoint": "Central turning point",
            "complications": ["Challenges and obstacles"]
        },
        "act_three": {
            "climax_buildup": ["Events leading to climax"],
            "climax": "Main story climax",
            "resolution": ["Resolution elements"]
        }
    },
    "subplots": [
        {
            "name": "Subplot name",
            "related_characters": ["Character names"],
            "arc": ["Key subplot events"],
            "resolution": "Subplot resolution"
        }
    ],
    "pacing_markers": [
        {
            "position": "Story percentage (0-100)",
            "event": "Key event",
            "tension_level": "1-10 scale"
        }
    ],
    "plot_coherence_score": 0.0
}"""

class PlotArchitect(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, PLOT_ARCHITECT_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Title: {state.get('title')}
            Genre: {state.get('genre')}
            Characters: {state.get('characters', [])}
            World: {state.get('world_building', {})}
            Creative Direction: {state.get('creative_direction', {})}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                "plot_structure": result["plot_structure"],
                "subplots": result["subplots"],
                "pacing_markers": result["pacing_markers"],
                "plot_coherence_score": result["plot_coherence_score"],
                "plot_development_complete": True
            })
            
            self.logger.info(
                "plot_architecture_complete",
                title=state.get('title'),
                subplot_count=len(result["subplots"]),
                coherence_score=result["plot_coherence_score"]
            )
            
            return state
            
        except Exception as e:
            self.logger.error("plot_architecture_failed", error=str(e))
            raise