from typing import Dict, Any, List
from .base import BaseAgent

QUALITY_ASSESSOR_PROMPT = """You are the Quality Assessor responsible for evaluating the 
overall story quality and providing actionable improvement suggestions.

Your output must be valid JSON with the following structure:
{
    "quality_assessment": {
        "overall_evaluation": {
            "summary": "Brief quality assessment",
            "strengths": ["Major strong points"],
            "weaknesses": ["Areas needing improvement"]
        },
        "component_scores": {
            "plot": 0.0,
            "characters": 0.0,
            "dialogue": 0.0,
            "pacing": 0.0,
            "world_building": 0.0,
            "style": 0.0
        },
        "improvement_recommendations": [
            {
                "category": "Area of improvement",
                "issue": "Specific problem",
                "suggestion": "How to fix it",
                "priority": "high/medium/low"
            }
        ],
        "market_readiness": {
            "score": 0.0,
            "required_revisions": ["Necessary changes"],
            "target_audience_fit": "Assessment of audience match"
        }
    }
}"""

class QualityAssessor(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, QUALITY_ASSESSOR_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Complete Story State: {state}
            Quality Metrics: {{
                "plot_coherence": {state.get('plot_coherence_score', 0.0)},
                "character_depth": {state.get('character_development_score', 0.0)},
                "style_quality": {state.get('style_metrics', {}).get('overall_style_score', 0.0)}
            }}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                'quality_assessment': result['quality_assessment'],
                'final_quality_check_complete': True
            })
            
            self.logger.info(
                "quality_assessment_complete",
                market_readiness=result['quality_assessment']['market_readiness']['score'],
                improvements_needed=len(
                    result['quality_assessment']['improvement_recommendations']
                )
            )
            
            return state
            
        except Exception as e:
            self.logger.error("quality_assessment_failed", error=str(e))
            raise