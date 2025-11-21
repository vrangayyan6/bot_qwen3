import sqlite3
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class ConversationDatabase:
    """Manages conversation history using SQLite."""
    
    def __init__(self, db_path: str = "conversations.db"):
        """Initialize database connection. Call _init_db() separately to create tables."""
        self.db_path = db_path
    
    async def _init_db(self):
        """Create tables if they don't exist."""
        def _create_tables():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create conversations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY,
                        title TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                # Create messages table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id TEXT,
                        role TEXT,
                        content TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                    )
                """)
                
                # Create index for faster queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_conversation_id 
                    ON messages(conversation_id)
                """)
                
                conn.commit()
        
        await asyncio.to_thread(_create_tables)
    
    async def create_conversation(self, conversation_id: str, title: str = "New Conversation", metadata: Optional[Dict] = None) -> Dict:
        """Create a new conversation."""
        def _create():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations (id, title, metadata)
                    VALUES (?, ?, ?)
                """, (conversation_id, title, json.dumps(metadata or {})))
                conn.commit()
                
                return {
                    "id": conversation_id,
                    "title": title,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "metadata": metadata or {}
                }
        
        return await asyncio.to_thread(_create)
    
    async def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get a specific conversation by ID."""
        def _get():
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM conversations WHERE id = ?
                """, (conversation_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        "id": row["id"],
                        "title": row["title"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"],
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
                    }
                return None
        
        return await asyncio.to_thread(_get)
    
    async def get_all_conversations(self, limit: int = 50) -> List[Dict]:
        """Get all conversations, ordered by most recent."""
        def _get_all():
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.*, COUNT(m.id) as message_count
                    FROM conversations c
                    LEFT JOIN messages m ON c.id = m.conversation_id
                    GROUP BY c.id
                    ORDER BY c.updated_at DESC
                    LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
                
                return [
                    {
                        "id": row["id"],
                        "title": row["title"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"],
                        "message_count": row["message_count"],
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
                    }
                    for row in rows
                ]
        
        return await asyncio.to_thread(_get_all)
    
    async def add_message(self, conversation_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Add a message to a conversation."""
        def _add():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Add message
                cursor.execute("""
                    INSERT INTO messages (conversation_id, role, content, metadata)
                    VALUES (?, ?, ?, ?)
                """, (conversation_id, role, content, json.dumps(metadata or {})))
                
                message_id = cursor.lastrowid
                
                # Update conversation's updated_at timestamp
                cursor.execute("""
                    UPDATE conversations 
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (conversation_id,))
                
                conn.commit()
                
                return {
                    "id": message_id,
                    "conversation_id": conversation_id,
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": metadata or {}
                }
        
        return await asyncio.to_thread(_add)
    
    async def get_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages for a conversation."""
        def _get_msgs():
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM messages 
                    WHERE conversation_id = ?
                    ORDER BY timestamp ASC
                """, (conversation_id,))
                rows = cursor.fetchall()
                
                return [
                    {
                        "id": row["id"],
                        "conversation_id": row["conversation_id"],
                        "role": row["role"],
                        "content": row["content"],
                        "timestamp": row["timestamp"],
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
                    }
                    for row in rows
                ]
        
        return await asyncio.to_thread(_get_msgs)
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and all its messages."""
        def _delete():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
                deleted = cursor.rowcount > 0
                conn.commit()
                return deleted
        
        return await asyncio.to_thread(_delete)
    
    async def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """Update the title of a conversation."""
        def _update():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE conversations 
                    SET title = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (title, conversation_id))
                updated = cursor.rowcount > 0
                conn.commit()
                return updated
        
        return await asyncio.to_thread(_update)
