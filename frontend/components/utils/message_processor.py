from typing import Dict, List, Optional
from datetime import datetime

class MessageProcessor:
    """Utility class for processing chat messages"""
    
    @staticmethod
    def format_message(content: str, user: str, timestamp: bool = True) -> Dict:
        """
        Format a message for display and storage
        
        Args:
            content: Message content
            user: Username/agent name
            timestamp: Whether to include timestamp
        """
        message = {
            "role": "user" if user == "User" else "assistant",
            "content": content,
            "sender": user
        }
        
        if timestamp:
            message["timestamp"] = datetime.now().strftime("%H:%M")
            
        return message
    
    @staticmethod
    def prepare_for_swarm(messages: List[Dict]) -> List[Dict]:
        """
        Prepare messages for Swarm processing
        
        Args:
            messages: List of message dictionaries
        """
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in messages
            if msg["content"].strip()  # Filter out empty messages
        ]
    
    @staticmethod
    def extract_tool_calls(message: Dict) -> List[Dict]:
        """
        Extract tool calls from a message
        
        Args:
            message: Message dictionary containing potential tool calls
        """
        if "tool_calls" not in message:
            return []
            
        return [
            {
                "name": tool["function"]["name"],
                "args": tool["function"]["arguments"]
            }
            for tool in message["tool_calls"]
        ]
