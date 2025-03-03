import pytest

def test_basic_setup():
    """Verify pytest is working"""
    assert True

@pytest.mark.asyncio
async def test_state_fixture(test_state):
    """Verify test state fixture"""
    assert "title" in test_state
    assert "genre" in test_state