import pytest
from agents.quality_assessor import QualityAssessor

@pytest.fixture
def test_state():
    return {
        "title": "The Last Guardian",
        "plot_coherence_score": 0.85,
        "character_development_score": 0.78,
        "style_metrics": {"overall_style_score": 0.82},
        "scenes": [
            {"id": "scene_001", "quality_score": 0.88}
        ]
    }

@pytest.mark.asyncio
async def test_quality_assessment(test_state):
    agent = QualityAssessor()
    result = await agent.invoke(test_state)
    
    assert "quality_assessment" in result
    assessment = result["quality_assessment"]
    
    # Verify structure
    assert "overall_evaluation" in assessment
    assert "component_scores" in assessment
    assert "improvement_recommendations" in assessment
    assert "market_readiness" in assessment
    
    # Check component scores
    scores = assessment["component_scores"]
    assert all(0.0 <= score <= 1.0 for score in scores.values())

@pytest.mark.asyncio
async def test_improvement_recommendations(test_state):
    agent = QualityAssessor()
    result = await agent.invoke(test_state)
    
    recommendations = result["quality_assessment"]["improvement_recommendations"]
    assert len(recommendations) > 0
    
    for rec in recommendations:
        assert all(key in rec for key in [
            "category", "issue", "suggestion", "priority"
        ])
        assert rec["priority"] in ["high", "medium", "low"]

@pytest.mark.asyncio
async def test_quality_assessor_error_handling():
    agent = QualityAssessor()
    with pytest.raises(Exception):
        await agent.invoke({})