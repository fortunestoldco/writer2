import pytest
from agents.creative_director import CreativeDirectorAgent

@pytest.fixture
def test_state():
    return {
        "title": "The Last Lighthouse",
        "genre": "historical fiction",
        "vision": "A compelling story of isolation and hope",
        "outline": [
            "Chapter 1: The Arrival",
            "Chapter 2: First Storm",
            "Chapter 3: The Discovery"
        ]
    }

@pytest.mark.asyncio
async def test_creative_director_output(test_state):
    agent = CreativeDirectorAgent()
    result = await agent.invoke(test_state)
    
    assert "creative_direction" in result
    assert "character_guidelines" in result
    assert "pacing" in result
    assert "creative_quality_score" in result
    assert isinstance(result["creative_quality_score"], float)
    assert 0.0 <= result["creative_quality_score"] <= 1.0

@pytest.mark.asyncio
async def test_creative_director_error_handling():
    agent = CreativeDirectorAgent()
    with pytest.raises(Exception):
        await agent.invoke({})  # Empty state should raise error