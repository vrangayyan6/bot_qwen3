"""
Test script for conversation database functionality.
Run this to verify the database is working correctly.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent.database import ConversationDatabase


def test_database():
    """Test basic database operations."""
    print("🧪 Testing Conversation Database...\n")
    
    # Initialize database
    db = ConversationDatabase("test_conversations.db")
    print("✅ Database initialized")
    
    # Create a conversation
    conv = db.create_conversation(
        conversation_id="test-123",
        title="Test Conversation",
        metadata={"test": True}
    )
    print(f"✅ Created conversation: {conv['id']}")
    
    # Add messages
    msg1 = db.add_message(
        conversation_id="test-123",
        role="human",
        content="Hello, how are you?"
    )
    print(f"✅ Added human message: {msg1['id']}")
    
    msg2 = db.add_message(
        conversation_id="test-123",
        role="ai",
        content="I'm doing great! How can I help you today?"
    )
    print(f"✅ Added AI message: {msg2['id']}")
    
    # Get conversation
    retrieved = db.get_conversation("test-123")
    print(f"✅ Retrieved conversation: {retrieved['title']}")
    
    # Get messages
    messages = db.get_messages("test-123")
    print(f"✅ Retrieved {len(messages)} messages")
    
    # Get all conversations
    all_convs = db.get_all_conversations()
    print(f"✅ Found {len(all_convs)} total conversations")
    
    # Update title
    db.update_conversation_title("test-123", "Updated Test Title")
    updated = db.get_conversation("test-123")
    print(f"✅ Updated title to: {updated['title']}")
    
    # Delete conversation
    deleted = db.delete_conversation("test-123")
    print(f"✅ Deleted conversation: {deleted}")
    
    # Verify deletion
    after_delete = db.get_all_conversations()
    print(f"✅ Conversations after delete: {len(after_delete)}")
    
    print("\n🎉 All tests passed!")
    
    # Cleanup
    Path("test_conversations.db").unlink(missing_ok=True)
    print("🧹 Cleaned up test database")


if __name__ == "__main__":
    test_database()
