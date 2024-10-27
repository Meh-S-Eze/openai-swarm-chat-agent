import panel as pn
from typing import Callable, Optional

class ChatInput:
    """Message input component for the chat interface"""
    
    def __init__(self, on_submit: Callable[[str], None], placeholder: str = "Type a message..."):
        """
        Initialize the chat input component
        
        Args:
            on_submit: Callback function when message is submitted
            placeholder: Placeholder text for input field
        """
        # Create input widgets
        self.text_input = pn.widgets.TextInput(
            placeholder=placeholder,
            sizing_mode="stretch_width"
        )
        
        self.send_button = pn.widgets.Button(
            name="Send",
            button_type="primary",
            icon="paper-plane"
        )
        
        # Set up event handlers
        self.text_input.on_change('value', self._handle_enter)
        self.send_button.on_click(self._handle_click)
        
        # Store callback
        self.on_submit = on_submit
        
        # Create layout
        self.layout = self._create_layout()
        
    def _handle_enter(self, event) -> None:
        """Handle enter key press"""
        if event.new and event.new.strip():
            self._submit_message(event.new)
            
    def _handle_click(self, event) -> None:
        """Handle send button click"""
        if self.text_input.value and self.text_input.value.strip():
            self._submit_message(self.text_input.value)
            
    def _submit_message(self, message: str) -> None:
        """Submit message and clear input"""
        self.on_submit(message)
        self.text_input.value = ""
        
    def _create_layout(self) -> pn.Row:
        """Create the input layout"""
        return pn.Row(
            self.text_input,
            self.send_button,
            sizing_mode="stretch_width",
            css_classes=["chat-input"]
        )
        
    def get_panel(self) -> pn.viewable.Viewable:
        """Return the Panel component for rendering"""
        return self.layout
