from time import time
from typing import Callable

import structlog
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from opentelemetry import metrics, trace

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
request_duration = meter.create_histogram(
    name="http_request_duration",
    description="Duration of HTTP requests in seconds",
    unit="s",
)


async def error_handler_middleware(
    request: Request, call_next: Callable
) -> JSONResponse:
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        logger.warning("http_exception", status_code=exc.status_code, detail=exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    except Exception as exc:
        logger.error("unhandled_exception", error=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )


async def telemetry_middleware(request: Request, call_next: Callable) -> JSONResponse:
    start_time = time()

    with tracer.start_as_current_span(
        name=f"{request.method} {request.url.path}",
        attributes={
            "http.method": request.method,
            "http.url": str(request.url),
        },
    ) as span:
        response = await call_next(request)
        duration = time() - start_time

        request_duration.record(
            duration, {"path": request.url.path, "method": request.method}
        )

        span.set_attribute("http.status_code", response.status_code)
        return response
