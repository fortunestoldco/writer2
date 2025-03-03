import pytest
from workflows import create_initialization_graph

@pytest.mark.asyncio
async def test_initialization_graph():
    graph = create_initialization_graph()
    input_data = {
        "title": "Test Story",
        "genre": "mystery"
    }
    
    result = await graph.ainvoke(input_data)
    
    assert result["status"] == "initialized"
    assert result["initialization_complete"] is True