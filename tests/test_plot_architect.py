import pytest
from agents.plot_architect import PlotArchitect

@pytest.fixture
def test_state():
    return {
        "title": "The Echo of Time",
        "genre": "science fiction",
        "characters": [
            {
                "name": "Dr. Sarah Chen",
                "role": "Protagonist",
                "personality": {
                    "traits": ["brilliant", "determined", "haunted"]
                }
            },
            {
                "name": "Marcus Webb",
                "role": "Antagonist",
                "personality": {
                    "traits": ["charismatic", "ruthless", "visionary"]
                }
            }
        ],
        "world_building": {
            "setting": {
                "time_period": "near future",
                "location": "research facility"
            }
        }
    }

@pytest.mark.asyncio
async def test_plot_architect_structure(test_state):
    agent = PlotArchitect()
    result = await agent.invoke(test_state)
    
    # Verify plot structure
    assert "plot_structure" in result
    assert all(act in result["plot_structure"] for act in ["act_one", "act_two", "act_three"])
    
    # Verify subplots
    assert "subplots" in result
    assert len(result["subplots"]) > 0
    for subplot in result["subplots"]:
        assert all(key in subplot for key in ["name", "related_characters", "arc", "resolution"])

@pytest.mark.asyncio
async def test_plot_coherence(test_state):
    agent = PlotArchitect()
    result = await agent.invoke(test_state)
    
    assert "plot_coherence_score" in result
    assert 0.0 <= result["plot_coherence_score"] <= 1.0
    
    # Verify pacing markers
    assert "pacing_markers" in result
    for marker in result["pacing_markers"]:
        assert 0 <= float(marker["position"]) <= 100
        assert 1 <= int(marker["tension_level"]) <= 10

@pytest.mark.asyncio
async def test_plot_architect_error_handling():
    agent = PlotArchitect()
    with pytest.raises(Exception):
        await agent.invoke({})