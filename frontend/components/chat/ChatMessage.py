import panel as pn
from typing import Optional, Dict

class ChatMessage:
    """Individual message component for the chat interface"""
    
    def __init__(self, content: str, user: str, avatar: Optional[str] = None, 
                 timestamp: Optional[str] = None, message_type: str = "text"):
        """
        Initialize a chat message component
        
        Args:
            content: The message content
            user: Username/agent name
            avatar: Emoji or image URL for avatar
            timestamp: Message timestamp (optional)
            message_type: Type of message ("text", "error", "system")
        """
        self.content = content
        self.user = user
        self.avatar = avatar or self._get_default_avatar(user)
        self.timestamp = timestamp
        self.message_type = message_type
        
        # Create the message component
        self.message = self._create_message()
        
    def _get_default_avatar(self, user: str) -> str:
        """Return default avatar based on user type"""
        avatars = {
            "System": "ℹ️",
            "Support Bot": "🤖",
            "Error": "⚠️",
            "User": "👤"
        }
        return avatars.get(user, "👤")
        
    def _create_message(self) -> pn.Column:
        """Create and style the message component"""
        # Message container
        message = pn.Column(
            sizing_mode="stretch_width",
            margin=(5, 10),
            css_classes=[f"chat-message-{self.message_type}"]
        )
        
        # Header with user and timestamp
        header = pn.Row(
            pn.pane.Markdown(f"**{self.avatar} {self.user}**", margin=(0, 5)),
            pn.pane.Markdown(self.timestamp, css_classes=["timestamp"]) if self.timestamp else None,
            sizing_mode="stretch_width"
        )
        
        # Message content
        content = pn.pane.Markdown(
            self.content,
            sizing_mode="stretch_width",
            css_classes=["message-content"]
        )
        
        message.extend([header, content])
        return message
    
    def get_panel(self) -> pn.viewable.Viewable:
        """Return the Panel component for rendering"""
        return self.message
