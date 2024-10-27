import panel as pn
from typing import Optional, Dict, List
from swarm import Swarm, Agent

class SwarmChatInterface:
    def __init__(self, swarm_client: Optional[Swarm] = None):
        # Initialize Panel with material design
        pn.extension(design="material")
        
        # Initialize Swarm client and default agent
        self.swarm = swarm_client or Swarm()
        self.default_agent = Agent(
            name="Support Bot",
            instructions="You are a helpful support bot. Be friendly and professional."
        )
        
        # Initialize chat interface
        self.chat_interface = pn.chat.ChatInterface(
            callback=self.process_message,
            show_rerun=False,
            show_undo=False,
            show_clear=True,
            sizing_mode="stretch_width",
            height=600
        )
        
        # Initialize message history and context
        self.messages: List[Dict] = []
        self.context_variables: Dict = {
            'customer_name': None,
            'last_order_id': None
        }
        
        # Send welcome message
        self.chat_interface.send(
            "Welcome! Please enter your name to begin.",
            user="System",
            respond=False
        )

    def process_message(self, contents: str, user: str, instance: pn.chat.ChatInterface):
        """Process incoming messages and handle agent responses"""
        if not contents.strip():
            return
            
        if self.context_variables['customer_name'] is None:
            # Handle initial name collection
            self.context_variables['customer_name'] = contents
            self.chat_interface.send(
                f"Hello {contents}! How can I help you today?",
                user="Support Bot",
                avatar="🤖",
                respond=False
            )
            return

        # Add user message to history
        self.messages.append({"role": "user", "content": contents})
        
        try:
            # Get response from Swarm with default agent
            response = self.swarm.run(
                agent=self.default_agent,
                messages=self.messages,
                context_variables=self.context_variables
            )
            
            # Process agent response
            if response.messages:
                last_message = response.messages[-1]
                self.chat_interface.send(
                    last_message["content"],
                    user=response.agent.name if response.agent else "Support Bot",
                    avatar="🤖",
                    respond=False
                )
                
                # Update message history and context
                self.messages = response.messages
                if response.context_variables:
                    self.context_variables.update(response.context_variables)
                    
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.chat_interface.send(
                error_msg,
                user="System",
                avatar="⚠️",
                respond=False
            )

    def get_panel(self) -> pn.viewable.Viewable:
        """Return the Panel component for rendering"""
        return self.chat_interface

    def servable(self):
        """Make the chat interface servable by Panel"""
        return self.chat_interface.servable()
