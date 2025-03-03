from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Any
import time

# Story metrics
story_creation_counter = Counter(
    'story_creations_total',
    'Total number of stories created',
    ['status']
)

story_phase_duration = Histogram(
    'story_phase_duration_seconds',
    'Time spent in each story phase',
    ['phase_name']
)

active_stories = Gauge(
    'active_stories',