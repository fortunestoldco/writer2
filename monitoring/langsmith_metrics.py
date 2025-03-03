from contextlib import asynccontextmanager
from langsmith import Client
from prometheus_client import Counter, Histogram
import time
import structlog

logger = structlog.get_logger(__name__)

llm_calls = Counter(
    'llm_calls_total',
    'Total number of LLM API calls',
    ['model']
)

llm_latency = Histogram(
    'llm_latency_seconds',
    'Latency of LLM API calls',
    ['model']
)

class LangSmithMetrics:
    def __init__(self):
        self.client = Client()
    
    @asynccontextmanager
    async def track_run(self, name: str, model: str):
        start_time = time.time()
        llm_calls.labels(model=model).inc()
        
        try:
            run = self.client.create_run(
                name=name,
                inputs={},
                run_type="llm"
            )
            yield run
            
            duration = time.time() - start_time
            llm_latency.labels(model=model).observe(duration)
            
            self.client.update_run(
                run.id,
                outputs={"duration": duration},
                end_time=time.time()
            )
        except Exception as e:
            logger.error("langsmith_error", error=str(e))
            raise