from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

import uvicorn
import os
import time

# --- Configuration ---
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")

# --- OpenTelemetry setup ---
resource = Resource(attributes={"service.name": "energy-demo"})
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)

# Send traces to the collector
otlp_exporter = OTLPSpanExporter(endpoint=f"{OTEL_ENDPOINT}/v1/traces")
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# --- FastAPI setup ---
app = FastAPI(title="Energy Demo", version="1.0.0")

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

# --- Routes ---
@app.get("/")
async def root():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("root-handler"):
        return {"message": "Hello from Energy Demo!"}

@app.get("/simulate")
async def simulate():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("simulate-work"):
        time.sleep(0.5)
        return {"status": "ok", "details": "simulated processing"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)