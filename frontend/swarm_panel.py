import panel as pn
from typing import Optional

# Import our custom components
from components.chat.ChatInterface import SwarmChatInterface
from components.utils.context_manager import ContextManager
from components.utils.agent_handler import AgentHandler
from styles.theme import SwarmTheme

class SwarmPanel:
    """
    Main Panel application for the Swarm chat interface.
    Orchestrates all components and manages the overall application state.
    """
    
    def __init__(self):
        """Initialize the Swarm Panel application"""
        
        # Initialize theme with material design
        SwarmTheme.initialize()
        
        # Initialize core utilities
        self.context_manager = ContextManager()
        self.agent_handler = AgentHandler()
        
        # Create main chat interface
        self.chat_interface = SwarmChatInterface(
            swarm_client=self.agent_handler.swarm
        )
        
        # Create main application layout
        self.app = self._create_layout()
        
    def _create_layout(self) -> pn.Column:
        """
        Create the main application layout
        
        Returns:
            Panel Column containing the complete UI
        """
        # Header section with styling
        header_text = pn.pane.Markdown(
            "# Swarm Chat Interface",
            margin=(10, 5),
            css_classes=['header-text']
        )
        
        header = pn.Row(
            header_text,
            css_classes=['header']
        )
        
        # Main chat area
        chat_container = pn.Column(
            self.chat_interface.get_panel(),
            css_classes=['chat-container'],
            sizing_mode='stretch_both'
        )
        
        # Combine all elements
        layout = pn.Column(
            header,
            chat_container,
            sizing_mode='stretch_both',
            css_classes=['main-container']
        )
        
        return layout
    
    def serve(self, port: Optional[int] = 5006) -> None:
        """
        Serve the Panel application
        
        Args:
            port: Port number for the server
        """
        # Make the app servable
        self.app.servable()
        
        # Log startup message
        print(f"Starting Swarm Panel on http://localhost:{port}")
        
        # Start the server
        pn.serve(
            self.app,
            port=port,
            show=True,
            title="Swarm Chat"
        )

# Create and serve the application when run directly
if __name__ == "__main__":
    app = SwarmPanel()
    app.serve()
