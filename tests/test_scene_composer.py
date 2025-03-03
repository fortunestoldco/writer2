import pytest
from agents.scene_composer import SceneComposer

@pytest.fixture
def test_state():
    return {
        "title": "The Last Light",
        "plot_structure": {
            "act_one": {
                "setup": ["Lighthouse introduction", "Storm warning"],
                "inciting_incident": "First radio failure"
            }
        },
        "characters": [
            {
                "name": "Thomas Wright",
                "role": "Protagonist",
                "personality": {
                    "traits": ["dedicated", "isolated", "resourceful"]
                }
            }
        ],
        "world_building": {
            "setting": {
                "location": "Remote lighthouse",
                "time_period": "1950s"
            }
        }
    }

@pytest.mark.asyncio
async def test_scene_composition(test_state):
    agent = SceneComposer()
    result = await agent.invoke(test_state)
    
    assert 'scenes' in result
    assert len(result['scenes']) > 0
    
    # Verify scene structure
    first_scene = result['scenes'][0]
    assert all(key in first_scene for key in [
        'id', 'title', 'setting', 'participants', 
        'action', 'narrative_focus', 'pacing', 'tension_level'
    ])
    
    # Verify transitions
    assert 'scene_transitions' in result
    assert isinstance(result['composition_quality_score'], float)
    assert 0.0 <= result['composition_quality_score'] <= 1.0

@pytest.mark.asyncio
async def test_scene_composer_error_handling():
    agent = SceneComposer()
    with pytest.raises(Exception):
        await agent.invoke({})