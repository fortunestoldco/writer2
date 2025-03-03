from prometheus_client import Counter, Histogram, Gauge
import time

# Story metrics
story_phases = Counter(
    'story_phases_total',
    'Total number of story phases completed',
    ['phase', 'status']
)

agent_duration = Histogram(
    'agent_duration_seconds',
    'Time taken by agents to process',
    ['agent_type']
)

class MetricsCollector:
    @classmethod
    def track_phase(cls, phase_name: str, status: str):
        story_phases.labels(phase=phase_name, status=status).inc()

    @classmethod
    def track_agent_duration(cls, agent_type: str, duration: float):
        agent_duration.labels(agent_type=agent_type).observe(duration)