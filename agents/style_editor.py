from typing import Dict, Any, List
from .base import BaseAgent

STYLE_EDITOR_PROMPT = """You are the Style Editor responsible for maintaining consistent 
writing quality and tone. Polish prose and ensure stylistic coherence.

Your output must be valid JSON with the following structure:
{
    "style_analysis": {
        "tone_assessment": {
            "identified_tone": "Current tone",
            "consistency_issues": ["Tone breaks"],
            "recommendations": ["Tone adjustments"]
        },
        "prose_quality": {
            "strengths": ["Strong elements"],
            "weaknesses": ["Areas for improvement"],
            "suggested_revisions": [
                {
                    "scene_id": "scene_identifier",
                    "original": "Original text",
                    "revised": "Improved version",
                    "reasoning": "Why this improves style"
                }
            ]
        },
        "voice_consistency": {
            "narrative_voice": "Identified voice",
            "deviations": ["Points where voice wavers"],
            "fixes": ["How to maintain voice"]
        }
    },
    "style_metrics": {
        "tone_consistency": 0.0,
        "prose_quality": 0.0,
        "voice_stability": 0.0,
        "overall_style_score": 0.0
    }
}"""

class StyleEditor(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, STYLE_EDITOR_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Creative Direction: {state.get('creative_direction', {})}
            Scenes: {state.get('scenes', [])}
            Dialogue: {state.get('scene_dialogues', [])}
            Target Style: {state.get('style_guidelines', {})}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                'style_analysis': result['style_analysis'],
                'style_metrics': result['style_metrics'],
                'style_editing_complete': True
            })
            
            return state
            
        except Exception as e:
            self.logger.error("style_editing_failed", error=str(e))
            raise