from typing import Dict, Any, List
from .base import BaseAgent

DIALOGUE_WRITER_PROMPT = """You are the Dialogue Writer responsible for creating natural, 
character-specific dialogue that advances the story and reveals character depth.

Your output must be valid JSON with the following structure:
{
    "scene_dialogues": [
        {
            "scene_id": "scene_identifier",
            "exchanges": [
                {
                    "speaker": "Character name",
                    "line": "Spoken dialogue",
                    "subtext": "Hidden meaning or emotion",
                    "delivery": "How the line is delivered"
                }
            ],
            "tension_points": ["Moments of heightened tension"],
            "character_dynamics": ["Relationship developments"]
        }
    ],
    "dialogue_metrics": {
        "naturalness_score": 0.0,
        "character_voice_consistency": 0.0,
        "subtext_effectiveness": 0.0
    }
}"""

class DialogueWriter(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, DIALOGUE_WRITER_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Characters: {state.get('characters', [])}
            Scenes: {state.get('scenes', [])}
            Plot Points: {state.get('plot_structure', {})}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                'scene_dialogues': result['scene_dialogues'],
                'dialogue_metrics': result['dialogue_metrics'],
                'dialogue_complete': True
            })
            
            self.logger.info(
                "dialogue_writing_complete",
                scene_count=len(result['scene_dialogues']),
                metrics=result['dialogue_metrics']
            )
            
            return state
            
        except Exception as e:
            self.logger.error("dialogue_writing_failed", error=str(e))
            raise