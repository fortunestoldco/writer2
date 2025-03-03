from typing import Dict, Any, List
from .base import BaseAgent

CHARACTER_DESIGNER_PROMPT = """You are the Character Designer responsible for creating deep, 
compelling characters. Create detailed character profiles based on the story requirements.

Your output must be valid JSON with the following structure:
{
    "characters": [
        {
            "name": "Character name",
            "role": "Protagonist/Antagonist/Supporting",
            "background": "Character history and context",
            "personality": {
                "traits": ["Key personality traits"],
                "motivations": ["Core driving forces"],
                "conflicts": ["Internal and external conflicts"]
            },
            "relationships": [
                {
                    "with": "Other character name",
                    "type": "Relationship type",
                    "dynamics": "Relationship dynamics"
                }
            ]
        }
    ],
    "character_arcs": [
        {
            "character": "Character name",
            "arc_type": "Growth/Fall/Change/Static",
            "key_moments": ["Important moments in character development"]
        }
    ],
    "ensemble_dynamics": {
        "group_conflicts": ["Major group tensions"],
        "power_dynamics": ["Power relationships"],
        "character_chemistry_score": 0.0
    }
}"""

class CharacterDesigner(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, CHARACTER_DESIGNER_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Title: {state.get('title')}
            Genre: {state.get('genre')}
            Creative Vision: {state.get('creative_direction', {})}
            World Building: {state.get('world_building', {})}
            Existing Characters: {state.get('characters', [])}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                "characters": result["characters"],
                "character_arcs": result["character_arcs"],
                "ensemble_dynamics": result["ensemble_dynamics"],
                "character_development_complete": True
            })
            
            self.logger.info(
                "character_design_complete",
                title=state.get('title'),
                character_count=len(result["characters"]),
                chemistry_score=result["ensemble_dynamics"]["character_chemistry_score"]
            )
            
            return state
            
        except Exception as e:
            self.logger.error("character_design_failed", error=str(e))
            raise