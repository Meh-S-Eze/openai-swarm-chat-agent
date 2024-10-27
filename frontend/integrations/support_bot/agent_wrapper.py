from typing import Dict, List, Optional
from swarm import Agent, Result

class SupportBotAgents:
    """
    Wrapper for managing Support Bot agents.
    Provides configuration and initialization of specialized support agents.
    """
    
    def __init__(self):
        """Initialize support bot agents and their configurations"""
        # Initialize agents dictionary
        self.agents: Dict[str, Agent] = {}
        
        # Set up all support agents
        self._initialize_agents()
        
    def _initialize_agents(self) -> None:
        """Configure and initialize all support agents"""
        # Create triage agent
        self.agents['triage'] = Agent(
            name="Triage Agent",
            instructions=self._get_triage_instructions(),
            functions=[
                self.transfer_to_product_info,
                self.transfer_to_order_status,
                self.transfer_to_refunds
            ]
        )
        
        # Create specialized support agents
        self.agents['product_info'] = Agent(
            name="Product Information Agent",
            instructions=self._get_product_info_instructions(),
            functions=[self.query_docs]
        )
        
        self.agents['order_status'] = Agent(
            name="Order Status Agent",
            instructions=self._get_order_status_instructions(),
            functions=[self.get_order_status]
        )
        
        self.agents['refunds'] = Agent(
            name="Returns and Refunds Agent",
            instructions=self._get_refunds_instructions(),
            functions=[self.process_refund]
        )
    
    # Agent instruction methods
    def _get_triage_instructions(self) -> str:
        """Get instructions for triage agent"""
        return """
        You are a triage agent for customer support. Direct inquiries to:
        - Product Information Agent for product details
        - Order Status Agent for order tracking
        - Returns and Refunds Agent for refund requests
        Greet customers and clarify their needs before transferring.
        """
    
    def _get_product_info_instructions(self) -> str:
        """Get instructions for product information agent"""
        return """
        You are a product information specialist.
        Use the query_docs function to find and provide accurate product details.
        Be helpful and informative about product features and specifications.
        """
    
    def _get_order_status_instructions(self) -> str:
        """Get instructions for order status agent"""
        return """
        You are an order status specialist.
        Use get_order_status to check and explain order status to customers.
        Provide clear updates and estimated delivery times.
        """
    
    def _get_refunds_instructions(self) -> str:
        """Get instructions for refunds agent"""
        return """
        You are a returns and refunds specialist.
        Use process_refund to handle refund requests.
        Explain the refund policy and process clearly.
        """
    
    # Agent handoff functions
    def transfer_to_product_info(self, context: Dict) -> Result:
        """Transfer to product information agent"""
        return Result(agent=self.agents['product_info'], context_variables=context)
    
    def transfer_to_order_status(self, context: Dict) -> Result:
        """Transfer to order status agent"""
        return Result(agent=self.agents['order_status'], context_variables=context)
    
    def transfer_to_refunds(self, context: Dict) -> Result:
        """Transfer to refunds agent"""
        return Result(agent=self.agents['refunds'], context_variables=context)
    
    # Agent tool functions
    def query_docs(self, query: str) -> Dict:
        """Query product documentation"""
        return {"status": "success", "action": "query_docs", "query": query}
    
    def get_order_status(self, order_id: str) -> Dict:
        """Get order status"""
        return {"status": "success", "action": "get_order_status", "order_id": order_id}
    
    def process_refund(self, order_id: str) -> Dict:
        """Process refund request"""
        return {"status": "success", "action": "process_refund", "order_id": order_id}
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Get agent by name"""
        return self.agents.get(agent_name)
    
    def get_default_agent(self) -> Agent:
        """Get default (triage) agent"""
        return self.agents['triage']
