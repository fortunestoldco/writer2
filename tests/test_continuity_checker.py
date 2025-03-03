import pytest
from agents.continuity_checker import ContinuityChecker

@pytest.fixture
def test_state():
    return {
        "plot_structure": {
            "act_one": {"setup": ["Character introduces magic amulet"]},
            "act_two": {"midpoint": "Character uses amulet's power"}
        },
        "characters": [
            {
                "name": "Sarah",
                "arc": ["Discovers amulet", "Masters its power"]
            }
        ],
        "world_building": {
            "rules": ["Magic requires amulet", "Amulet glows when active"]
        }
    }

@pytest.mark.asyncio
async def test_continuity_analysis(test_state):
    agent = ContinuityChecker()
    result = await agent.invoke(test_state)
    
    # Verify structure
    assert "continuity_analysis" in result
    analysis = result["continuity_analysis"]
    
    assert "plot_threads" in analysis
    assert "character_arcs" in analysis
    assert "world_rule_violations" in analysis
    
    # Check plot threads
    for thread in analysis["plot_threads"]:
        assert all(key in thread for key in ["thread_id", "elements", "status", "issues"])

@pytest.mark.asyncio
async def test_consistency_metrics(test_state):
    agent = ContinuityChecker()
    result = await agent.invoke(test_state)
    
    # Verify metrics
    assert "consistency_metrics" in result
    metrics = result["consistency_metrics"]
    
    for metric_name, value in metrics.items():
        assert 0.0 <= value <= 1.0

@pytest.mark.asyncio
async def test_continuity_checker_error_handling():
    agent = ContinuityChecker()
    with pytest.raises(Exception):
        await agent.invoke({})