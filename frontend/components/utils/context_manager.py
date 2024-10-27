from typing import Dict, Any, Optional
from datetime import datetime

class ContextManager:
    """
    Manages context variables and state for the chat session.
    Provides a centralized way to handle user context, session data, and agent states.
    """
    
    def __init__(self):
        # Initialize core context variables
        self._context: Dict[str, Any] = {
            'customer_name': None,          # Store user's name
            'last_order_id': None,          # Track last referenced order
            'session_start': datetime.now() # Session start timestamp
        }
        
        # Track current agent and conversation state
        self._current_agent: str = "System"
        self._is_authenticated: bool = False
    
    def update(self, key: str, value: Any) -> None:
        """
        Update a specific context variable
        
        Args:
            key: Context variable name
            value: New value to store
        """
        self._context[key] = value
        
        # Set authentication state when customer name is set
        if key == 'customer_name' and value:
            self._is_authenticated = True
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a context variable
        
        Args:
            key: Context variable name
            default: Default value if key doesn't exist
        """
        return self._context.get(key, default)
    
    def set_current_agent(self, agent_name: str) -> None:
        """
        Update the currently active agent
        
        Args:
            agent_name: Name of the current agent
        """
        self._current_agent = agent_name
    
    def get_current_agent(self) -> str:
        """Return the name of the currently active agent"""
        return self._current_agent
    
    def is_authenticated(self) -> bool:
        """Check if user has provided their name"""
        return self._is_authenticated
    
    def get_session_duration(self) -> float:
        """Return current session duration in minutes"""
        duration = datetime.now() - self._context['session_start']
        return duration.total_seconds() / 60
    
    def get_all_context(self) -> Dict[str, Any]:
        """Return complete context dictionary"""
        return self._context.copy()
