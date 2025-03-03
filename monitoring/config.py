from pydantic_settings import BaseSettings

class MonitoringSettings(BaseSettings):
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    LANGSMITH_API_KEY: str
    OTEL_TRACES_SAMPLER: str = "parentbased_traceidratio"
    OTEL_TRACES_SAMPLER_ARG: float = 1.0
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"