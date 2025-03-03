from typing import Dict, Any, List
from .base import BaseAgent

SCENE_COMPOSER_PROMPT = """You are the Scene Composer responsible for creating vivid, 
engaging scenes that bring the story to life. Craft detailed scene compositions based on 
the plot structure and character interactions.

Your output must be valid JSON with the following structure:
{
    "scenes": [
        {
            "id": "unique_scene_id",
            "title": "Scene title",
            "setting": {
                "location": "Specific location",
                "time": "Time of day/period",
                "atmosphere": "Mood and environmental details"
            },
            "participants": [
                {
                    "character": "Character name",
                    "objective": "Character's goal in scene",
                    "emotional_state": "Character's emotions"
                }
            ],
            "action": {
                "opening": "Scene opening description",
                "key_events": ["Major events in scene"],
                "closing": "Scene closing description"
            },
            "narrative_focus": "POV or perspective emphasis",
            "pacing": "Fast/Medium/Slow",
            "tension_level": "1-10 scale value"
        }
    ],
    "scene_transitions": [
        {
            "from_scene": "source_scene_id",
            "to_scene": "target_scene_id",
            "transition_type": "cut/fade/parallel",
            "transition_notes": "Specific transition guidance"
        }
    ],
    "composition_quality_score": 0.0
}"""

class SceneComposer(BaseAgent):
    def __init__(self, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name, SCENE_COMPOSER_PROMPT)
    
    async def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            input_text = f"""
            Title: {state.get('title')}
            Plot Structure: {state.get('plot_structure', {})}
            Characters: {state.get('characters', [])}
            World: {state.get('world_building', {})}
            Current Scene Count: {len(state.get('scenes', []))}
            """
            
            chain = self.prompt | self.llm | self.output_parser
            result = await chain.ainvoke({"input": input_text})
            
            # Update state with new scenes
            existing_scenes = state.get('scenes', [])
            new_scenes = result['scenes']
            
            state.update({
                'scenes': existing_scenes + new_scenes,
                'scene_transitions': result['scene_transitions'],
                'composition_quality_score': result['composition_quality_score'],
                'scene_composition_complete': True
            })
            
            self.logger.info(
                "scene_composition_complete",
                title=state.get('title'),
                new_scene_count=len(new_scenes),
                quality_score=result['composition_quality_score']
            )
            
            return state
            
        except Exception as e:
            self.logger.error("scene_composition_failed", error=str(e))
            raise