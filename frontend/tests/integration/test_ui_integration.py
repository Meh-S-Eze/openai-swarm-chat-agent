import pytest
import panel as pn
from typing import Dict, List

from frontend.components.chat.ChatInterface import SwarmChatInterface
from frontend.components.utils.context_manager import ContextManager
from frontend.components.utils.agent_handler import AgentHandler
from frontend.integrations.support_bot.panel_interface import SupportBotInterface
from frontend.integrations.support_bot.agent_wrapper import SupportBotAgents

class TestUIIntegration:
    """
    Integration tests for Panel UI components with Swarm agents.
    Verifies end-to-end functionality of the chat interface with support bot.
    """
    
    @pytest.fixture
    def support_bot(self):
        """Fixture providing configured support bot interface"""
        return SupportBotInterface()
    
    @pytest.fixture
    def chat_interface(self, support_bot):
        """Fixture providing chat interface with support bot integration"""
        return SwarmChatInterface(swarm_client=support_bot.swarm)
    
    @pytest.fixture
    def agents(self):
        """Fixture providing support bot agents"""
        return SupportBotAgents()
    
    def test_end_to_end_conversation(self, chat_interface, support_bot):
        """Test complete conversation flow with agent handoffs"""
        # Initialize conversation with user name
        response = chat_interface.process_message(
            contents="John Doe",
            user="User",
            instance=None
        )
        assert chat_interface.context_variables["customer_name"] == "John Doe"
        
        # Test product inquiry
        response = chat_interface.process_message(
            contents="What products do you offer?",
            user="User",
            instance=None
        )
        assert response is not None
        assert len(chat_interface.messages) > 2
        
        # Verify agent handoff occurred
        last_message = chat_interface.messages[-1]
        assert "product" in last_message["content"].lower()
    
    def test_tool_integration(self, chat_interface, support_bot):
        """Test integration of support tools"""
        # Set up user context
        chat_interface.process_message("Jane Doe", "User", None)
        
        # Test documentation query
        response = chat_interface.process_message(
            contents="Can you check the documentation about refunds?",
            user="User",
            instance=None
        )
        
        # Verify tool usage
        messages = chat_interface.messages
        tool_used = any(
            "query_docs" in str(msg.get("tool_calls", []))
            for msg in messages
        )
        assert tool_used
    
    def test_context_persistence(self, chat_interface, support_bot):
        """Test context maintenance across agent handoffs"""
        # Initialize conversation
        chat_interface.process_message("Alice Smith", "User", None)
        
        # Simulate multiple agent interactions
        queries = [
            "What products do you have?",
            "Check my order status",
            "I need a refund"
        ]
        
        for query in queries:
            chat_interface.process_message(query, "User", None)
            
        # Verify context persistence
        assert chat_interface.context_variables["customer_name"] == "Alice Smith"
    
    @pytest.mark.asyncio
    async def test_streaming_response(self, chat_interface, support_bot):
        """Test streaming response functionality"""
        # Initialize conversation
        chat_interface.process_message("Bob Wilson", "User", None)
        
        # Test streaming response
        chunks = []
        async for chunk in chat_interface.process_message_async(
            "Tell me about your return policy",
            "User",
            None
        ):
            chunks.append(chunk)
            
        # Verify streaming behavior
        assert len(chunks) > 0
        assert any(isinstance(chunk, (str, dict)) for chunk in chunks)
    
    def test_error_recovery(self, chat_interface, support_bot):
        """Test system recovery from errors"""
        # Force an error condition
        response = chat_interface.process_message(
            contents=None,  # Invalid input
            user="User",
            instance=None
        )
        
        # Verify system remains functional
        recovery_response = chat_interface.process_message(
            contents="Hello",
            user="User",
            instance=None
        )
        assert recovery_response is not None
