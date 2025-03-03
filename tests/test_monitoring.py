import pytest
import asyncio
from monitoring.metrics import MetricsCollector
from prometheus_client import REGISTRY
from langsmith import Client
from unittest.mock import patch

@pytest.fixture
def metrics_collector():
    return MetricsCollector()

def test_story_metrics_registration():
    """Test that story metrics are properly registered"""
    metrics = [m.name for m in REGISTRY.collect()]
    
    assert 'story_creations_total' in metrics
    assert 'story_phase_duration_seconds' in metrics
    assert 'active_stories' in metrics

@pytest.mark.asyncio
async def test_phase_duration_tracking():
    """Test phase duration tracking"""
    async with MetricsCollector.track_phase_duration("test_phase"):
        await asyncio.sleep(0.1)
    
    # Verify metrics were recorded
    samples = REGISTRY.get_sample_value(
        'story_phase_duration_seconds_count',
        {'phase_name': 'test_phase'}
    )
    assert samples is not None
    assert samples > 0

@pytest.mark.asyncio
async def test_active_stories_gauge():
    """Test active stories gauge updates"""
    MetricsCollector.update_active_stories(1)
    value = REGISTRY.get_sample_value('active_stories')
    assert value == 1
    
    MetricsCollector.update_active_stories(-1)
    value = REGISTRY.get_sample_value('active_stories')
    assert value == 0

@pytest.mark.asyncio
async def test_langsmith_integration():
    """Test LangSmith metrics collection"""
    with patch.object(Client, 'create_run') as mock_create_run:
        mock_create_run.return_value = {"id": "test-run-id"}
        
        async with MetricsCollector.track_llm_call("test_model"):
            await asyncio.sleep(0.1)
        
        samples = REGISTRY.get_sample_value(
            'llm_calls_total',
            {'model': 'test_model'}
        )
        assert samples == 1

def test_error_metrics():
    """Test error tracking metrics"""
    MetricsCollector.track_error("validation_error")
    
    value = REGISTRY.get_sample_value(
        'story_errors_total',
        {'error_type': 'validation_error'}
    )
    assert value == 1
