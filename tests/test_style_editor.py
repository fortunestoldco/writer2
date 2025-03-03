import pytest
from agents.style_editor import StyleEditor

@pytest.fixture
def test_state():
    return {
        "creative_direction": {
            "tone": "darkly humorous",
            "style": "sharp and witty"
        },
        "scenes": [
            {
                "id": "scene_001",
                "content": "The room was dark and quiet."
            }
        ],
        "style_guidelines": {
            "voice": "third person limited",
            "tone": "sardonic"
        }
    }

@pytest.mark.asyncio
async def test_style_analysis(test_state):
    agent = StyleEditor()
    result = await agent.invoke(test_state)
    
    assert "style_analysis" in result
    analysis = result["style_analysis"]
    
    # Verify structure
    assert all(key in analysis for key in [
        "tone_assessment",
        "prose_quality",
        "voice_consistency"
    ])
    
    # Check revisions
    revisions = analysis["prose_quality"]["suggested_revisions"]
    assert len(revisions) > 0
    for revision in revisions:
        assert all(key in revision for key in [
            "scene_id", "original", "revised", "reasoning"
        ])

@pytest.mark.asyncio
async def test_style_metrics(test_state):
    agent = StyleEditor()
    result = await agent.invoke(test_state)
    
    assert "style_metrics" in result
    metrics = result["style_metrics"]
    
    # Verify metric ranges
    for metric_value in metrics.values():
        assert 0.0 <= metric_value <= 1.0

@pytest.mark.asyncio
async def test_style_editor_error_handling():
    agent = StyleEditor()
    with pytest.raises(Exception):
        await agent.invoke({})