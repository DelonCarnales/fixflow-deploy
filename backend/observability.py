"""Prometheus-compatible application metrics and OpenTelemetry exporters."""
import logging
import os

from opentelemetry import metrics, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "fixflow-api")
RESOURCE = Resource.create({
    "service.name": SERVICE_NAME,
    "deployment.environment": os.getenv("APP_ENV", "development"),
})
HTTP_REQUESTS = Counter("fixflow_http_requests_total", "Total HTTP requests handled by FixFlow", ["method", "path", "status"])
HTTP_DURATION = Histogram("fixflow_http_request_duration_seconds", "HTTP request duration in seconds", ["method", "path"], buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10))

endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").rstrip("/")
trace_provider = TracerProvider(resource=RESOURCE)
if endpoint:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")))
trace.set_tracer_provider(trace_provider)

readers = []
if endpoint:
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    readers.append(PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics"), export_interval_millis=15000))
meter_provider = MeterProvider(resource=RESOURCE, metric_readers=readers)
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(SERVICE_NAME)
OTEL_REQUESTS = meter.create_counter("fixflow.http.requests", description="HTTP requests")
OTEL_DURATION = meter.create_histogram("fixflow.http.request.duration", unit="s", description="HTTP request duration")

if endpoint:
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    logger_provider = LoggerProvider(resource=RESOURCE)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=f"{endpoint}/v1/logs")))
    set_logger_provider(logger_provider)
    logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))

logger = logging.getLogger("fixflow.observability")
logger.setLevel(logging.INFO)

def record_request(method: str, path: str, status: int, duration: float) -> None:
    HTTP_REQUESTS.labels(method=method, path=path, status=str(status)).inc()
    HTTP_DURATION.labels(method=method, path=path).observe(duration)
    attributes = {"http.request.method": method, "http.route": path, "http.response.status_code": status}
    OTEL_REQUESTS.add(1, attributes)
    OTEL_DURATION.record(duration, attributes)
    logger.info("HTTP request completed", extra={"http_method": method, "http_route": path, "http_status_code": status, "duration_seconds": round(duration, 4)})

def prometheus_metrics() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
