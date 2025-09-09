from src.langgraphagenticai.state.state import State
class ChatbotWithToolNode:
    def __init__(self,model):
        self.llm=model
    def process(self,state:State)->dict:
        """
        Processes the inpit state and generate a response with tool intgration
        """
        user_input=state['messages'][-1] if state['messages'] else ""
        llm_response=self.llm.invoke([{"role":"user","content":user_input}])
        tools_response=f"Tool integration for: {user_input}"
        return {"messages":[llm_response,tools_response]}
    def create_chatbot(self,tools):
        llm_with_tools=self.llm.bind_tools(tools)
        def chatbot_node(state:State):
            return {"messages":[llm_with_tools.invoke(state["messages"])]}
        return chatbot_node