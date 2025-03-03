import pytest
from agents.executive_director import ExecutiveDirectorAgent
from agents.human_feedback import HumanFeedbackManager

@pytest.fixture
def test_state():
    return {
        "title": "The Mystery of the Hidden Key",
        "genre": "mystery",
        "length": "novel",
        "current_phase": "initialization"
    }

@pytest.mark.asyncio
async def test_executive_director(test_state):
    agent = ExecutiveDirectorAgent()
    result = await agent.invoke(test_state)
    
    assert "vision" in result
    assert "outline" in result
    assert "themes" in result
    assert "quality_metrics" in result
    assert isinstance(result["quality_metrics"], dict)

@pytest.mark.asyncio
async def test_human_feedback_manager(test_state):
    agent = HumanFeedbackManager()
    test_state.update({
        "vision": "A compelling mystery novel...",
        "outline": ["Chapter 1: Discovery", "Chapter 2: Investigation"],
        "themes": ["Trust", "Betrayal"]
    })
    
    result = await agent.invoke(test_state)
    
    assert "feedback_requests" in result
    assert "critical_areas" in result
    assert "human_feedback_confidence" in result