from typing import Dict, Any
from .base import BaseAgent

CREATIVE_DIRECTOR_PROMPT = """You are the Creative Director responsible for the artistic vision and narrative quality.
Analyze the current story state and provide creative direction.

Your output must be valid JSON with the following structure:
{
    "creative_vision": {
        "tone": "Overall tone and mood",
        "style": "Writing style guidelines",
        "narrative_voice": "POV and narrative approach"
    },
    "character_guidelines": [
        {
            "name": "Character name",
            "arc": "Character development arc",
            "voice": "Distinctive voice traits"
        }
    ],
    "pacing_recommendations": [
        "Specific pacing guidelines"
    ],
    "creative_score": 0.0
}
"""

class CreativeDirectorAgent(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, CREATIVE_DIRECTOR_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Title: {state.get('title')}
            Genre: {state.get('genre')}
            Current Vision: {state.get('vision', 'Not set')}
            Outline: {state.get('outline', [])}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                "creative_direction": result["creative_vision"],
                "character_guidelines": result["character_guidelines"],
                "pacing": result["pacing_recommendations"],
                "creative_quality_score": result["creative_score"]
            })
            
            self.logger.info(
                "creative_direction_complete",
                title=state.get('title'),
                creative_score=result["creative_score"]
            )
            
            return state
            
        except Exception as e:
            self.logger.error("creative_direction_failed", error=str(e))
            raise