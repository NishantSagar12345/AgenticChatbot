from src.langgraphagenticai.state.state import State


class BasicChatbotNode:
    """
    Basic Chatbot login Implementation
    
    """
    def __init__(self,model):
       self.llm=model

    def process(self,state:State)->dict:   
        """
        Processs the structure if the state used in the graph
        """
        return {"messages":self.llm.invoke(state['messages'])}