from typing import Dict, List, Optional, Any
from swarm import Swarm, Agent, Response

class AgentHandler:
    """
    Manages interactions with Swarm agents.
    Handles agent initialization, message routing, and response processing.
    """
    
    def __init__(self, swarm_client: Optional[Swarm] = None):
        # Initialize Swarm client or use provided one
        self.swarm = swarm_client or Swarm()
        
        # Track current active agent
        self._current_agent: Optional[Agent] = None
        
        # Store last response for context
        self._last_response: Optional[Response] = None
        
    def process_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user message through the appropriate Swarm agent
        
        Args:
            message: User's input message
            context: Current context variables
            
        Returns:
            Dict containing:
                - content: Agent's response text
                - agent_name: Name of responding agent
                - tool_calls: Any tools called during processing
        """
        try:
            # Prepare message format for Swarm
            formatted_message = {"role": "user", "content": message}
            
            # Get response from Swarm
            response = self.swarm.run(
                agent=self._current_agent,  # Will use default if None
                messages=[formatted_message],
                context_variables=context
            )
            
            # Store response and update current agent
            self._last_response = response
            self._current_agent = response.agent
            
            # Extract relevant information
            return {
                "content": response.messages[-1]["content"],
                "agent_name": response.agent.name if response.agent else "System",
                "tool_calls": self._extract_tool_calls(response.messages[-1])
            }
            
        except Exception as e:
            # Handle errors gracefully
            return {
                "content": f"Error processing message: {str(e)}",
                "agent_name": "System",
                "tool_calls": []
            }
            
    def _extract_tool_calls(self, message: Dict) -> List[Dict]:
        """
        Extract tool calls from agent message
        
        Args:
            message: Message dictionary potentially containing tool calls
            
        Returns:
            List of tool call dictionaries
        """
        if "tool_calls" not in message:
            return []
            
        return [
            {
                "name": tool["function"]["name"],
                "arguments": tool["function"]["arguments"]
            }
            for tool in message["tool_calls"]
        ]
        
    def get_current_agent(self) -> Optional[Agent]:
        """Return currently active agent"""
        return self._current_agent
        
    def get_last_response(self) -> Optional[Response]:
        """Return last Swarm response"""
        return self._last_response
