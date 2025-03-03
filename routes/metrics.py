from fastapi import APIRouter, Depends
from prometheus_client import (
    generate_latest, 
    CONTENT_TYPE_LATEST, 
    Counter, 
    Histogram, 
    Gauge
)
from fastapi.responses import Response
from typing import Dict
from dependencies import get_mongodb

# Define metrics
story_phases = Counter(
    'story_phases_total',
    'Number of story phases completed',
    ['phase_name']
)

processing_time = Histogram(
    'processing_time_seconds',
    'Time spent processing requests',
    ['endpoint']
)

active_projects = Gauge(
    'active_projects',
    'Number of currently active story projects'
)

router = APIRouter(prefix="/metrics", tags=["monitoring"])

@router.get("")
async def metrics():
    """Endpoint for Prometheus metrics"""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@router.get("/health")
async def health_check(
    mongodb = Depends(get_mongodb)
) -> Dict[str, str]:
    """Health check endpoint"""
    try:
        await mongodb.ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}