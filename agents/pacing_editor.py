from typing import Dict, Any, List
from .base import BaseAgent

PACING_EDITOR_PROMPT = """You are the Pacing Editor responsible for managing story rhythm 
and tension. Analyze and adjust scene pacing to maintain reader engagement.

Your output must be valid JSON with the following structure:
{
    "pacing_analysis": {
        "overall_rhythm": "Assessment of story rhythm",
        "tension_curve": [
            {
                "position": "0-100 percentage",
                "tension_level": "1-10 scale",
                "scene_id": "related_scene_id",
                "pacing_type": "slow/medium/fast"
            }
        ],
        "scene_adjustments": [
            {
                "scene_id": "scene_identifier",
                "recommended_changes": [
                    "Specific pacing adjustments"
                ],
                "target_length": "word count or duration",
                "intensity_shift": "increase/decrease/maintain"
            }
        ]
    },
    "pacing_metrics": {
        "rhythm_consistency": 0.0,
        "tension_progression": 0.0,
        "scene_balance": 0.0
    }
}"""

class PacingEditor(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, PACING_EDITOR_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Plot Structure: {state.get('plot_structure', {})}
            Scenes: {state.get('scenes', [])}
            Scene Dialogues: {state.get('scene_dialogues', [])}
            Current Pacing: {state.get('pacing_markers', [])}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                'pacing_analysis': result['pacing_analysis'],
                'pacing_metrics': result['pacing_metrics'],
                'pacing_complete': True
            })
            
            self.logger.info(
                "pacing_editing_complete",
                rhythm_score=result['pacing_metrics']['rhythm_consistency'],
                tension_score=result['pacing_metrics']['tension_progression']
            )
            
            return state
            
        except Exception as e:
            self.logger.error("pacing_editing_failed", error=str(e))
            raise