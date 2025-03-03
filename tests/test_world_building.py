import pytest
from agents.world_building import WorldBuildingExpert

@pytest.fixture
def test_state():
    return {
        "title": "The Crystal Cities",
        "genre": "science fiction",
        "creative_direction": {
            "tone": "mysterious and ethereal",
            "style": "descriptive and atmospheric"
        }
    }

@pytest.mark.asyncio
async def test_world_building_output(test_state):
    agent = WorldBuildingExpert()
    result = await agent.invoke(test_state)
    
    assert "world_building" in result
    assert "setting" in result["world_building"]
    assert "elements" in result["world_building"]
    assert "rules" in result["world_building"]
    assert "world_consistency_score" in result
    assert isinstance(result["world_consistency_score"], float)
    assert 0.0 <= result["world_consistency_score"] <= 1.0

@pytest.mark.asyncio
async def test_world_building_error_handling():
    agent = WorldBuildingExpert()
    with pytest.raises(Exception):
        await agent.invoke({})  # Empty state should raise error