import pytest
from agents.character_designer import CharacterDesigner

@pytest.fixture
def test_state():
    return {
        "title": "The Hidden Legacy",
        "genre": "mystery",
        "creative_direction": {
            "tone": "suspenseful and intricate",
            "style": "character-driven psychological"
        },
        "world_building": {
            "setting": {
                "time_period": "contemporary",
                "location": "small coastal town"
            }
        }
    }

@pytest.mark.asyncio
async def test_character_designer_output(test_state):
    agent = CharacterDesigner()
    result = await agent.invoke(test_state)
    
    # Verify character creation
    assert "characters" in result
    assert len(result["characters"]) > 0
    assert all(
        {"name", "role", "personality", "relationships"} <= set(char.keys())
        for char in result["characters"]
    )
    
    # Verify character arcs
    assert "character_arcs" in result
    assert len(result["character_arcs"]) > 0
    
    # Verify ensemble dynamics
    assert "ensemble_dynamics" in result
    assert "character_chemistry_score" in result["ensemble_dynamics"]
    assert 0.0 <= result["ensemble_dynamics"]["character_chemistry_score"] <= 1.0

@pytest.mark.asyncio
async def test_character_designer_relationships(test_state):
    agent = CharacterDesigner()
    result = await agent.invoke(test_state)
    
    # Check relationship consistency
    characters = {char["name"] for char in result["characters"]}
    for char in result["characters"]:
        for rel in char["relationships"]:
            assert rel["with"] in characters

@pytest.mark.asyncio
async def test_character_designer_error_handling():
    agent = CharacterDesigner()
    with pytest.raises(Exception):
        await agent.invoke({})