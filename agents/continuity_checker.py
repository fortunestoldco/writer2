from typing import Dict, Any, List
from .base import BaseAgent

CONTINUITY_CHECKER_PROMPT = """You are the Continuity Checker responsible for maintaining 
story consistency. Verify plot continuity, character arcs, and world-building rules.

Your output must be valid JSON with the following structure:
{
    "continuity_analysis": {
        "plot_threads": [
            {
                "thread_id": "unique_identifier",
                "elements": ["Related story elements"],
                "status": "resolved/unresolved/inconsistent",
                "issues": ["Any continuity problems"]
            }
        ],
        "character_arcs": [
            {
                "character": "Character name",
                "arc_progression": ["Key development points"],
                "consistency_issues": ["Any character inconsistencies"]
            }
        ],
        "world_rule_violations": [
            {
                "rule": "Violated world-building rule",
                "instances": ["Specific violations"],
                "suggested_fixes": ["How to resolve"]
            }
        ]
    },
    "consistency_metrics": {
        "plot_consistency": 0.0,
        "character_consistency": 0.0,
        "world_consistency": 0.0,
        "overall_consistency": 0.0
    }
}"""

class ContinuityChecker(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, CONTINUITY_CHECKER_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Plot Structure: {state.get('plot_structure', {})}
            Characters: {state.get('characters', [])}
            World Building: {state.get('world_building', {})}
            Scenes: {state.get('scenes', [])}
            Dialogue: {state.get('scene_dialogues', [])}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            state.update({
                'continuity_analysis': result['continuity_analysis'],
                'consistency_metrics': result['consistency_metrics'],
                'continuity_check_complete': True
            })
            
            self.logger.info(
                "continuity_check_complete",
                overall_consistency=result['consistency_metrics']['overall_consistency'],
                issues_found=len(result['continuity_analysis']['world_rule_violations'])
            )
            
            return state
            
        except Exception as e:
            self.logger.error("continuity_check_failed", error=str(e))
            raise