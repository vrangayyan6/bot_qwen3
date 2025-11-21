# Starting the Application with Conversation History

## Quick Start

### 1. Start the Backend Server

Open a terminal in the `backend` directory and run:

```bash
cd backend
langgraph dev
```

This will start the LangGraph server on `http://127.0.0.1:2024` with the new conversation history API endpoints.

**Note:** Make sure you have:
- Installed backend dependencies: `pip install .`
- Set up your `.env` file with `GEMINI_API_KEY`

### 2. Start the Frontend Development Server

Open another terminal in the `frontend` directory and run:

```bash
cd frontend
npm run dev
```

This will start the Vite dev server on `http://localhost:5173/app/`

The frontend is now configured to proxy API requests to the backend server on port 2024.

### 3. Access the Application

Open your browser and navigate to: `http://localhost:5173/app/`

## Features You Can Now Use

### History Button
- Click the "History" button (top-left) to view all your saved conversations
- Each conversation shows:
  - Title
  - Timestamp (formatted as "Today", "Yesterday", or date)
  - Message count
  - Current conversation highlighted

### Starting a Conversation
- Type your question in the welcome screen
- A new conversation is automatically created
- All messages are saved to the SQLite database (`backend/conversations.db`)

### Resuming a Conversation
1. Click "History" button
2. Click on any conversation from the list
3. All previous messages load automatically
4. Continue the conversation where you left off

### Starting a New Chat
- Click "New Chat" button (appears when you're in a conversation)
- Starts a fresh conversation
- Previous conversation remains saved

### Deleting Conversations
- Hover over any conversation in the history
- Click the trash icon that appears
- Confirm deletion

## Troubleshooting

### "Failed to create conversation" Error

This error means the frontend can't reach the backend API. Check:

1. **Backend is running**: Make sure `langgraph dev` is running in the backend directory
2. **Correct port**: Backend should be on port 2024 (check terminal output)
3. **Vite proxy**: The `frontend/vite.config.ts` should proxy `/api` to `http://127.0.0.1:2024`

### WebSocket Connection Errors

These are Vite HMR warnings and won't affect the application functionality. They occur because the app is served under `/app/` path.

### Database Errors

If you see SQLite errors:
1. Make sure the `backend` directory is writable
2. The database file `conversations.db` will be created automatically
3. Delete `conversations.db` to reset all conversations

## Database Location

Conversations are stored in: `backend/conversations.db`

You can:
- Inspect the database with any SQLite browser
- Delete it to start fresh
- Back it up to preserve conversations

## API Endpoints

The backend now serves these additional endpoints:

```
GET  /api/conversations              - List all conversations
GET  /api/conversation/{id}          - Get specific conversation
POST /api/conversation               - Create new conversation
POST /api/conversation/{id}/message  - Add message to conversation
GET  /api/conversation/{id}/messages - Get all messages
DELETE /api/conversation/{id}        - Delete conversation
PATCH /api/conversation/{id}/title   - Update title
```

## Testing the Database

Run the test script to verify the database is working:

```bash
cd backend
python test_database.py
```

You should see: `🎉 All tests passed!`
