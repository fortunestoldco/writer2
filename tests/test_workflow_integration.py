import pytest
from workflows.manager import WorkflowManager

@pytest.fixture
def initial_state():
    return {
        "title": "The Crystal Key",
        "genre": "fantasy",
        "length": "novel"
    }

@pytest.mark.asyncio
async def test_complete_workflow(initial_state):
    manager = WorkflowManager()
    result = await manager.create_story(initial_state)
    
    assert result["status"] == "success"
    story = result["story"]
    
    # Verify all phases completed
    assert story["initialization_complete"]
    assert story["world_building_complete"]
    assert story["character_development_complete"]
    assert story["plot_development_complete"]
    assert story["scene_creation_complete"]
    assert story["refinement_complete"]
    assert story["final_review_complete"]
    
    # Verify key metrics exist
    assert "quality_assessment" in story
    assert "style_metrics" in story
    assert "consistency_metrics" in story

@pytest.mark.asyncio
async def test_workflow_error_handling():
    manager = WorkflowManager()
    result = await manager.create_story({})  # Empty initial state
    
    assert result["status"] == "error"
    assert "error" in result
    assert "phase" in result