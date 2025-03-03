from typing import Dict, Any
import pytest
from datetime import datetime

def get_test_story_state() -> Dict[str, Any]:
    """Generate a complete test story state."""
    return {
        "title": "Test Story",
        "genre": "mystery",
        "created_at": datetime.utcnow(),
        "current_phase": "initialization",
        "creative_direction": {
            "tone": "suspenseful",
            "style": "noir"
        },
        "world_building": {
            "setting": "modern city",
            "time_period": "present day"
        },
        "characters": [
            {
                "name": "Detective Smith",
                "role": "protagonist"
            }
        ]
    }

async def verify_agent_output(result: Dict[str, Any], expected_keys: list) -> None:
    """Verify agent output contains required keys and valid values."""
    assert all(key in result for key in expected_keys)
    assert result.get("status") in ["success", "error"]