import pytest
from datetime import datetime
from typing import Dict, List

from frontend.components.utils.message_processor import MessageProcessor

class TestMessageProcessor:
    """
    Test suite for MessageProcessor utility.
    Verifies message formatting, preparation, and tool call extraction functionality.
    """
    
    @pytest.fixture
    def processor(self):
        """Fixture providing MessageProcessor instance"""
        return MessageProcessor()
    
    @pytest.fixture
    def sample_message(self):
        """Fixture providing sample message data"""
        return {
            "role": "assistant",
            "content": "Hello, how can I help?",
            "sender": "Support Bot",
            "tool_calls": [
                {
                    "function": {
                        "name": "query_docs",
                        "arguments": '{"query": "product info"}'
                    }
                }
            ]
        }
    
    def test_format_message(self, processor):
        """Test message formatting functionality"""
        # Test user message formatting
        user_message = processor.format_message(
            content="Hello!",
            user="User",
            timestamp=True
        )
        
        # Verify message structure
        assert user_message["role"] == "user"
        assert user_message["content"] == "Hello!"
        assert user_message["sender"] == "User"
        assert "timestamp" in user_message
        
        # Test assistant message formatting
        assistant_message = processor.format_message(
            content="Hi there!",
            user="Support Bot",
            timestamp=False
        )
        
        assert assistant_message["role"] == "assistant"
        assert "timestamp" not in assistant_message
    
    def test_prepare_for_swarm(self, processor):
        """Test message preparation for Swarm processing"""
        messages = [
            {"role": "user", "content": "Hello", "sender": "User"},
            {"role": "assistant", "content": "Hi!", "sender": "Bot"},
            {"role": "user", "content": "  ", "sender": "User"}  # Empty message
        ]
        
        prepared = processor.prepare_for_swarm(messages)
        
        # Verify message preparation
        assert len(prepared) == 2  # Empty message should be filtered
        assert all("sender" not in msg for msg in prepared)
        assert all(key in ["role", "content"] for msg in prepared for key in msg)
    
    def test_extract_tool_calls(self, processor, sample_message):
        """Test tool call extraction from messages"""
        tool_calls = processor.extract_tool_calls(sample_message)
        
        # Verify tool call extraction
        assert len(tool_calls) == 1
        assert tool_calls[0]["name"] == "query_docs"
        assert isinstance(tool_calls[0]["args"], str)
        
        # Test message without tool calls
        no_tools_message = {"role": "user", "content": "Hello"}
        assert len(processor.extract_tool_calls(no_tools_message)) == 0
    
    def test_timestamp_format(self, processor):
        """Test timestamp formatting in messages"""
        message = processor.format_message(
            content="Test",
            user="User",
            timestamp=True
        )
        
        # Verify timestamp format
        timestamp = message["timestamp"]
        assert isinstance(timestamp, str)
        
        # Verify time format (HH:MM)
        try:
            datetime.strptime(timestamp, "%H:%M")
        except ValueError:
            pytest.fail("Timestamp format is incorrect")
    
    def test_empty_content_handling(self, processor):
        """Test handling of empty or whitespace-only content"""
        messages = [
            {"role": "user", "content": ""},
            {"role": "user", "content": "  "},
            {"role": "user", "content": "\n"}
        ]
        
        prepared = processor.prepare_for_swarm(messages)
        assert len(prepared) == 0
