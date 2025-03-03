import pytest
from config import Settings, get_settings

def test_settings_validation():
    with pytest.raises(ValueError):
        Settings(
            MONGODB_URL="",
            MONGODB_DB="",
            LANGCHAIN_API_KEY=""
        ).validate()

def test_settings_defaults():
    settings = get_settings()
    assert settings.DEBUG is False
    assert settings.APP_ENV == "development"
    assert settings.WORKFLOW_TIMEOUT == 600
    assert settings.MAX_RETRIES == 3