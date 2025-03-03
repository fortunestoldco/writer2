from typing import Dict, Any
from .base import BaseAgent

WORLD_BUILDING_PROMPT = """You are the World Building Expert responsible for creating rich, 
consistent story environments. Analyze the current story requirements and develop the world.

Your output must be valid JSON with the following structure:
{
    "setting": {
        "time_period": "Historical or fictional period",
        "location": "Primary story location",
        "atmosphere": "Environmental and emotional atmosphere"
    },
    "world_elements": [
        {
            "name": "Element name",
            "description": "Detailed description",
            "significance": "Story importance"
        }
    ],
    "rules": [
        "Key rules or constraints of this world"
    ],
    "consistency_score": 0.0
}
"""

class WorldBuildingExpert(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, WORLD_BUILDING_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Story Title: {state.get('title')}
            Genre: {state.get('genre')}
            Creative Direction: {state.get('creative_direction', {})}
            Current Setting: {state.get('setting', 'Not established')}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                "world_building": {
                    "setting": result["setting"],
                    "elements": result["world_elements"],
                    "rules": result["rules"]
                },
                "world_consistency_score": result["consistency_score"]
            })
            
            self.logger.info(
                "world_building_complete",
                title=state.get('title'),
                consistency_score=result["consistency_score"]
            )
            
            return state
            
        except Exception as e:
            self.logger.error("world_building_failed", error=str(e))
            raise