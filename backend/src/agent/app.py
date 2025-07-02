# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
from typing import List, Any
from fastapi import FastAPI, Response, Body
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Define the FastAPI app
app = FastAPI()

# In-memory store for sessions
sessions_db: List[Any] = []


class SessionItem(BaseModel):
    session_id: str
    messages: List[Any] # Replace Any with your Message model if available
    historicalActivities: Any # Replace Any with your Activity model if available

@app.post("/sessions")
async def save_session(session_item: SessionItem = Body(...)):
    sessions_db.append(session_item.dict())
    return {"status": "ok", "session_id": session_item.session_id}

@app.get("/sessions")
async def get_sessions() -> List[Any]:
    return sessions_db


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
