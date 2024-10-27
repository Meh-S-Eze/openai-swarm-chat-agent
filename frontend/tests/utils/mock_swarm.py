from typing import Dict, List, Optional
from swarm import Agent, Response

class MockSwarm:
    """Mock Swarm client for testing"""
    
    def __init__(self):
        self.messages = []
        self.context = {}
        
    def run(self, 
            agent: Optional[Agent] = None,
            messages: List[Dict] = None,
            context_variables: Dict = None) -> Response:
        """Mock run method"""
        messages = messages or []
        context_variables = context_variables or {}
        
        # Store the messages and context
        self.messages.extend(messages)
        self.context.update(context_variables)
        
        # Return a mock response
        return Response(
            messages=[{
                "role": "assistant",
                "content": "Mock response",
                "sender": "Mock Agent"
            }],
            agent=agent or Agent(name="Mock Agent"),
            context_variables=context_variables
        )
