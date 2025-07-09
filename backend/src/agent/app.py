# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
import fastapi.exceptions
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Define the FastAPI app
app = FastAPI()

# Configure OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
# Ensure an OTLP endpoint is available, e.g., from an OpenTelemetry Collector
# For local testing, you might run a collector in Docker:
# docker run -d -p 4317:4317 -p 4318:4318 otel/opentelemetry-collector:latest
otlp_exporter = OTLPSpanExporter(
    # endpoint="http://localhost:4317",  # Uncomment and set if your collector is not on localhost
    # insecure=True  # Set to False if using TLS
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)


def create_frontend_router(build_dir="../frontend/dist"):
    """Creates a router to serve the React frontend.

    Args:
        build_dir: Path to the React build directory relative to this file.

    Returns:
        A Starlette application serving the frontend.
    """
    build_path = pathlib.Path(__file__).parent.parent.parent / build_dir

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        print(
            f"WARN: Frontend build directory not found or incomplete at {build_path}. Serving frontend will likely fail."
        )
        # Return a dummy router if build isn't ready
        from starlette.routing import Route

        async def dummy_frontend(request):
            return Response(
                "Frontend not built. Run 'npm run build' in the frontend directory.",
                media_type="text/plain",
                status_code=503,
            )

        return Route("/{path:path}", endpoint=dummy_frontend)

    return StaticFiles(directory=build_path, html=True)


# Mount the frontend under /app to not conflict with the LangGraph API routes
app.mount(
    "/app",
    create_frontend_router(),
    name="frontend",
)
