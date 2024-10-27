import pytest
import panel as pn
from typing import Dict, List

from frontend.components.chat.ChatInterface import SwarmChatInterface
from frontend.components.utils.context_manager import ContextManager
from frontend.components.utils.agent_handler import AgentHandler
from frontend.tests.utils.mock_swarm import MockSwarm

class TestSwarmChatInterface:
    """
    Test suite for SwarmChatInterface component.
    Tests core functionality, message handling, and UI interactions.
    """
    
    @pytest.fixture
    def chat_interface(self):
        """Fixture providing configured chat interface with mock swarm"""
        return SwarmChatInterface(swarm_client=MockSwarm())
    
    @pytest.fixture
    def context_manager(self):
        """Fixture providing context manager for tests"""
        return ContextManager()
    
    @pytest.fixture
    def agent_handler(self):
        """Fixture providing agent handler for tests"""
        return AgentHandler()
    
    def test_initialization(self, chat_interface):
        """Test proper initialization of chat interface"""
        # Verify core components are initialized
        assert chat_interface.chat_interface is not None
        assert isinstance(chat_interface.messages, list)
        assert isinstance(chat_interface.context_variables, dict)
        
        # Verify welcome message
        messages = chat_interface.messages
        assert len(messages) == 1
        assert "Welcome" in messages[0]["content"]
    
    def test_process_message(self, chat_interface):
        """Test message processing functionality"""
        # Test initial name collection
        response = chat_interface.process_message(
            contents="John Doe",
            user="User",
            instance=None
        )
        assert chat_interface.context_variables["customer_name"] == "John Doe"
        
        # Test regular message processing
        response = chat_interface.process_message(
            contents="Hello, I need help",
            user="User",
            instance=None
        )
        assert len(chat_interface.messages) > 1
        assert response is not None
    
    def test_error_handling(self, chat_interface):
        """Test error handling in message processing"""
        # Force an error by passing invalid message
        response = chat_interface.process_message(
            contents=None,
            user="User",
            instance=None
        )
        
        # Verify error is handled gracefully
        assert "error" in response.lower() if response else True
    
    def test_context_integration(self, chat_interface, context_manager):
        """Test integration with context manager"""
        # Update context
        context_manager.update("customer_name", "Jane Doe")
        chat_interface.context_variables = context_manager.get_all_context()
        
        # Verify context is properly integrated
        assert chat_interface.context_variables["customer_name"] == "Jane Doe"
    
    def test_agent_integration(self, chat_interface, agent_handler):
        """Test integration with agent handler"""
        # Process message through agent
        response = chat_interface.process_message(
            contents="What are your products?",
            user="User",
            instance=None
        )
        
        # Verify agent response
        assert response is not None
        assert len(chat_interface.messages) > 1
    
    def test_ui_components(self, chat_interface):
        """Test UI component rendering"""
        panel = chat_interface.get_panel()
        
        # Verify Panel component is returned
        assert isinstance(panel, pn.viewable.Viewable)
        
        # Verify core UI elements
        assert hasattr(panel, "send")
        assert hasattr(panel, "clear")
    
    @pytest.mark.asyncio
    async def test_async_message_processing(self, chat_interface):
        """Test asynchronous message processing"""
        # Simulate async message processing
        messages = []
        async for chunk in chat_interface.process_message_async(
            "Hello, how are you?",
            "User",
            None
        ):
            messages.append(chunk)
        
        # Verify streaming response
        assert len(messages) > 0
        assert all(isinstance(m, (str, dict)) for m in messages)
