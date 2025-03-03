import pytest
from agents.dialogue_writer import DialogueWriter

@pytest.fixture
def test_state():
    return {
        "characters": [
            {
                "name": "John Smith",
                "personality": {"traits": ["witty", "sarcastic"]}
            },
            {
                "name": "Emma Chen",
                "personality": {"traits": ["direct", "passionate"]}
            }
        ],
        "scenes": [
            {
                "id": "scene_001",
                "title": "Coffee Shop Confrontation",
                "participants": ["John Smith", "Emma Chen"]
            }
        ]
    }

@pytest.mark.asyncio
async def test_dialogue_generation(test_state):
    agent = DialogueWriter()
    result = await agent.invoke(test_state)
    
    # Verify dialogue structure
    assert "scene_dialogues" in result
    assert len(result["scene_dialogues"]) > 0
    
    first_scene = result["scene_dialogues"][0]
    assert "scene_id" in first_scene
    assert "exchanges" in first_scene
    
    # Verify dialogue metrics
    assert "dialogue_metrics" in result
    metrics = result["dialogue_metrics"]
    assert all(0.0 <= score <= 1.0 for score in metrics.values())

@pytest.mark.asyncio
async def test_character_voice_consistency(test_state):
    agent = DialogueWriter()
    result = await agent.invoke(test_state)
    
    # Check if each character's dialogue matches their personality
    for scene in result["scene_dialogues"]:
        for exchange in scene["exchanges"]:
            assert exchange["speaker"] in [char["name"] for char in test_state["characters"]]
            assert "subtext" in exchange
            assert "delivery" in exchange

@pytest.mark.asyncio
async def test_dialogue_writer_error_handling():
    agent = DialogueWriter()
    with pytest.raises(Exception):
        await agent.invoke({})