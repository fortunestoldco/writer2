import pytest
from agents.pacing_editor import PacingEditor

@pytest.fixture
def test_state():
    return {
        "scenes": [
            {
                "id": "scene_001",
                "title": "Opening Chase",
                "pacing": "fast"
            },
            {
                "id": "scene_002",
                "title": "Aftermath Discussion",
                "pacing": "slow"
            }
        ],
        "plot_structure": {
            "act_one": {
                "setup": ["Initial situation"],
                "inciting_incident": "The chase begins"
            }
        }
    }

@pytest.mark.asyncio
async def test_pacing_analysis(test_state):
    agent = PacingEditor()
    result = await agent.invoke(test_state)
    
    assert "pacing_analysis" in result
    analysis = result["pacing_analysis"]
    
    # Verify tension curve
    assert "tension_curve" in analysis
    for point in analysis["tension_curve"]:
        assert 0 <= float(point["position"]) <= 100
        assert 1 <= int(point["tension_level"]) <= 10
    
    # Verify scene adjustments
    assert "scene_adjustments" in analysis
    for adjustment in analysis["scene_adjustments"]:
        assert "scene_id" in adjustment
        assert "recommended_changes" in adjustment

@pytest.mark.asyncio
async def test_pacing_metrics(test_state):
    agent = PacingEditor()
    result = await agent.invoke(test_state)
    
    assert "pacing_metrics" in result
    metrics = result["pacing_metrics"]
    
    # Verify metric ranges
    for metric_value in metrics.values():
        assert 0.0 <= metric_value <= 1.0

@pytest.mark.asyncio
async def test_pacing_editor_error_handling():
    agent = PacingEditor()
    with pytest.raises(Exception):
        await agent.invoke({})