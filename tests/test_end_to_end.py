import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_story_creation_workflow():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/story/create", json={
            "title": "The Last Echo",
            "genre": "science fiction",
            "length": "novel"
        })
        
        assert response.status_code == 200
        result = response.json()
        
        # Verify workflow completion
        assert result["status"] == "success"
        story = result["story"]
        
        # Check phase completions
        assert story["initialization_complete"]
        assert story["world_building_complete"]
        assert story["character_development_complete"]
        assert story["plot_development_complete"]
        assert story["scene_creation_complete"]
        assert story["refinement_complete"]
        assert story["final_review_complete"]