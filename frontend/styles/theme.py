import panel as pn
from typing import Dict, Optional

class SwarmTheme:
    """
    Manages theme and styling configurations for the Swarm Panel interface.
    Provides consistent styling across components with material design principles.
    """
    
    # Default color palette following material design
    DEFAULT_COLORS = {
        'primary': '#1976D2',      # Main brand color
        'secondary': '#424242',    # Secondary elements
        'success': '#4CAF50',      # Success states
        'error': '#F44336',        # Error states
        'warning': '#FF9800',      # Warning states
        'info': '#2196F3',         # Info states
        'background': '#FFFFFF',   # Main background
        'text': '#212121',         # Primary text
        'text-light': '#757575'    # Secondary text
    }
    
    # Default styling for chat components
    CHAT_STYLES = {
        'message': {
            'user': {'background': '#E3F2FD'},     # Light blue for user messages
            'assistant': {'background': '#F5F5F5'}, # Light grey for agent messages
            'system': {'background': '#FFF3E0'},    # Light orange for system messages
            'error': {'background': '#FFEBEE'}      # Light red for error messages
        },
        'input': {
            'border': '1px solid #E0E0E0',
            'border-radius': '4px',
            'padding': '8px'
        }
    }
    
    @classmethod
    def initialize(cls, custom_colors: Optional[Dict] = None) -> None:
        """
        Initialize Panel with theme settings
        
        Args:
            custom_colors: Optional dictionary of custom colors to override defaults
        """
        # Initialize Panel with material design
        pn.extension(
            design="material",
            sizing_mode="stretch_width"
        )
        
        # Apply custom CSS
        cls._apply_custom_css(cls.DEFAULT_COLORS)
    
    @staticmethod
    def _apply_custom_css(colors: Dict) -> None:
        """
        Apply custom CSS styles
        
        Args:
            colors: Color palette dictionary
        """
        pn.config.raw_css.append(f"""
            .chat-message {{
                margin: 8px 0;
                padding: 12px;
                border-radius: 8px;
            }}
            
            .chat-message-user {{
                background: {SwarmTheme.CHAT_STYLES['message']['user']['background']};
                margin-left: 20%;
            }}
            
            .chat-message-assistant {{
                background: {SwarmTheme.CHAT_STYLES['message']['assistant']['background']};
                margin-right: 20%;
            }}
            
            .chat-message-system {{
                background: {SwarmTheme.CHAT_STYLES['message']['system']['background']};
                font-style: italic;
            }}
            
            .chat-message-error {{
                background: {SwarmTheme.CHAT_STYLES['message']['error']['background']};
                color: {colors['error']};
            }}
            
            .timestamp {{
                color: {colors['text-light']};
                font-size: 0.8em;
            }}
        """)
