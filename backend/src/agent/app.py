# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
import uuid
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.database import ConversationDatabase

# Initialize database globally
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    global db
    # Startup: Initialize database
    # Use absolute path to backend directory for the database
    backend_dir = pathlib.Path(__file__).parent.parent.parent
    db_path = backend_dir / "conversations.db"
    db = ConversationDatabase(db_path=str(db_path))
    await db._init_db()
    print(f"Database initialized at: {db_path}")
    yield
    # Shutdown: cleanup if needed
    pass


# Define the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# Pydantic models for request/response
class CreateConversationRequest(BaseModel):
    title: Optional[str] = "New Conversation"
    metadata: Optional[dict] = None


class AddMessageRequest(BaseModel):
    role: str  # "human" or "ai"
    content: str
    metadata: Optional[dict] = None


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: Optional[int] = None
    metadata: dict


class MessageResponse(BaseModel):
    id: int
    conversation_id: str
    role: str
    content: str
    timestamp: str
    metadata: dict


# API Endpoints
@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations(limit: int = 50):
    """Get all conversations."""
    conversations = await db.get_all_conversations(limit=limit)
    return conversations


@app.get("/api/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    """Get a specific conversation."""
    conversation = await db.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@app.post("/api/conversation", response_model=ConversationResponse)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    conversation = await db.create_conversation(
        conversation_id=conversation_id,
        title=request.title or "New Conversation",
        metadata=request.metadata
    )
    return conversation


@app.post("/api/conversation/{conversation_id}/message", response_model=MessageResponse)
async def add_message_to_conversation(conversation_id: str, request: AddMessageRequest):
    """Add a message to a conversation."""
    # Check if conversation exists
    conversation = await db.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Add message
    message = await db.add_message(
        conversation_id=conversation_id,
        role=request.role,
        content=request.content,
        metadata=request.metadata
    )
    return message


@app.get("/api/conversation/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(conversation_id: str):
    """Get all messages for a conversation."""
    # Check if conversation exists
    conversation = await db.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = await db.get_messages(conversation_id)
    return messages


@app.delete("/api/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    deleted = await db.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "message": "Conversation deleted"}


@app.patch("/api/conversation/{conversation_id}/title")
async def update_conversation_title(conversation_id: str, title: str):
    """Update conversation title."""
    updated = await db.update_conversation_title(conversation_id, title)
    if not updated:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "message": "Title updated"}


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
