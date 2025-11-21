# Conversation History Implementation

This document describes the conversation history feature that has been added to the application.

## Overview

The application now supports persistent conversation history using SQLite database. Users can:
- Save conversations automatically
- View all previous conversations
- Resume any previous conversation
- Delete conversations
- Start new conversations

## Backend Changes

### 1. Database Layer (`backend/src/agent/database.py`)

Created a `ConversationDatabase` class that manages:
- **Conversations table**: Stores conversation metadata (id, title, timestamps)
- **Messages table**: Stores individual messages with role (human/ai) and content
- SQLite database with proper indexing for performance

Key methods:
- `create_conversation()`: Create a new conversation
- `get_conversation()`: Get conversation by ID
- `get_all_conversations()`: List all conversations
- `add_message()`: Add a message to a conversation
- `get_messages()`: Get all messages for a conversation
- `delete_conversation()`: Delete a conversation
- `update_conversation_title()`: Update conversation title

### 2. API Endpoints (`backend/src/agent/app.py`)

Added REST API endpoints:

```
GET  /api/conversations                    - List all conversations
GET  /api/conversation/{id}                - Get specific conversation
POST /api/conversation                     - Create new conversation
POST /api/conversation/{id}/message        - Add message to conversation
GET  /api/conversation/{id}/messages       - Get all messages
DELETE /api/conversation/{id}              - Delete conversation
PATCH /api/conversation/{id}/title         - Update title
```

### 3. State Management (`backend/src/agent/state.py`)

Added `conversation_id` field to `OverallState` to track which conversation the agent is processing.

### 4. Utilities (`backend/src/agent/utils.py`)

Added `load_conversation_history()` function to load previous messages from database and convert them to LangChain message format.

## Frontend Changes

### 1. ConversationHistory Component (`frontend/src/components/ConversationHistory.tsx`)

A modal component that displays:
- List of all conversations with titles and timestamps
- Message count for each conversation
- Delete button for each conversation
- Click to resume any conversation
- Beautiful space-themed UI matching the app design

Features:
- Formatted timestamps (Today, Yesterday, date)
- Current conversation highlighting
- Confirmation before deletion
- Loading and error states

### 2. App.tsx Updates

Integrated conversation history with:
- **History Button**: Fixed position button to open history modal
- **New Chat Button**: Start a fresh conversation
- **Auto-save**: Messages are automatically saved to database
- **Resume**: Load previous conversations with all messages
- **State Management**: Track current conversation ID

Key functions added:
- `createNewConversation()`: Create a new conversation when user starts chatting
- `saveMessage()`: Save each message (human and AI) to database
- `loadConversation()`: Load a previous conversation and restore state

## Usage

### Starting a New Conversation

1. Open the app (welcome screen)
2. Type a message and submit
3. A new conversation is automatically created
4. All messages are saved as they arrive

### Viewing History

1. Click the "History" button (top-left)
2. See list of all previous conversations
3. Click any conversation to resume it
4. Delete unwanted conversations with the trash icon

### Resuming a Conversation

1. Open History
2. Click on a conversation
3. All previous messages load
4. Continue the conversation from where you left off

### Starting Fresh

Click "New Chat" button to start a new conversation while keeping the previous one saved.

## Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT
)
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT,
    role TEXT,
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
)
```

## File Structure

```
backend/src/agent/
├── database.py          # New: SQLite database manager
├── app.py              # Updated: Added API endpoints
├── state.py            # Updated: Added conversation_id field
└── utils.py            # Updated: Added load_conversation_history()

frontend/src/
├── components/
│   ├── ConversationHistory.tsx  # New: History modal component
│   └── ...
└── App.tsx             # Updated: Integrated conversation history
```

## Future Enhancements

Potential improvements:
1. Search conversations by content
2. Rename conversations with custom titles
3. Export conversations
4. Share conversations
5. Conversation folders/tags
6. Automatic title generation from first message
7. Conversation analytics

## Notes

- Database file is created at `backend/conversations.db`
- Messages are saved immediately after being sent/received
- Deleting a conversation cascades to delete all its messages
- The database is persistent across app restarts
