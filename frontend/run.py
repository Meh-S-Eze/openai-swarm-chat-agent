import os
import panel as pn
from swarm_panel import SwarmPanel
from dotenv import load_dotenv

def main():
    """Initialize and run the Panel application"""
    # Load environment variables
    load_dotenv()
    
    # Initialize Panel with material theme
    pn.extension(design="material")
    
    # Create the application
    app = SwarmPanel()
    
    # Get port from environment or use default
    port = int(os.getenv("PANEL_PORT", 5006))
    
    # Start the server
    app.serve(port=port)

if __name__ == "__main__":
    main()
