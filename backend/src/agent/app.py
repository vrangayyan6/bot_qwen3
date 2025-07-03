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

    print(f"DEBUG: __file__ is {__file__}")
    print(f"DEBUG: build_dir is {build_dir}")
    print(f"DEBUG: Calculated build_path is {build_path}")
    try:
        abs_build_path = build_path.resolve()
        print(f"DEBUG: Absolute build_path is {abs_build_path}")
        print(f"DEBUG: build_path exists: {abs_build_path.exists()}")
        print(f"DEBUG: build_path is_dir: {abs_build_path.is_dir()}")
        index_html_path = abs_build_path / "index.html"
        print(f"DEBUG: index_html_path is {index_html_path}")
        print(f"DEBUG: index_html_path exists: {index_html_path.exists()}")
        print(f"DEBUG: index_html_path is_file: {index_html_path.is_file()}")

        # Try to list directories - this might fail if paths are incorrect or due to permissions
        try:
            frontend_dir_to_list = pathlib.Path("C:/AI-Programmi/new/gemini-fullstack-langgraph-quickstart/frontend")
            print(f"DEBUG: Listing {frontend_dir_to_list}: {list(frontend_dir_to_list.iterdir()) if frontend_dir_to_list.exists() else 'DOES NOT EXIST'}")
            frontend_dist_dir_to_list = pathlib.Path("C:/AI-Programmi/new/gemini-fullstack-langgraph-quickstart/frontend/dist")
            print(f"DEBUG: Listing {frontend_dist_dir_to_list}: {list(frontend_dist_dir_to_list.iterdir()) if frontend_dist_dir_to_list.exists() else 'DOES NOT EXIST'}")
        except Exception as e:
            print(f"DEBUG: Error listing directories: {e}")

    except Exception as e:
        print(f"DEBUG: Error resolving or checking build_path: {e}")


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
