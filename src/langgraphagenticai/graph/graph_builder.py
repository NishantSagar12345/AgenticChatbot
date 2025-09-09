from langgraph.graph import StateGraph,START,END  # Replace 'Graph' with the actual object you need from langgraph
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import ToolNode,tools_condition
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
class GraphBuilder:
    def __init__(self,model):
          self.llm=model
          self.graph_builder=StateGraph(State)  

    def basic_chatbot_build_graph(self):
          """
          Build a basic chatbot graph using langgrapgh
          """ 
          self.basic_chatbot_node=BasicChatbotNode(self.llm)                     
          self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
          self.graph_builder.add_edge(START,"chatbot")
          self.graph_builder.add_edge("chatbot",END)
    def chatbot_with_tools_build_graph(self):
          """
          Chatbot with advanced integration
          """    
          tools=get_tools()
          tool_node=create_tool_node(tools)
          #Define the LLM
          llm=self.llm
          ##Define the chatbot node
          obj_chatbot_with_node=ChatbotWithToolNode(llm)
          chatbot_node=obj_chatbot_with_node.create_chatbot(tools)
          #Add node
          self.graph_builder.add_node("chatbot",chatbot_node) 
          self.graph_builder.add_node("tools",tool_node)
          self.graph_builder.add_edge(START,"chatbot")
          self.graph_builder.add_conditional_edges("chatbot",tools_condition)
          self.graph_builder.add_edge("tools","chatbot")
          self.graph_builder.add_edge("chatbot",END)
    
    def ai_news_builder_graph(self):
         ai_news_node=AINewsNode(self.llm)
         self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
         self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
         self.graph_builder.add_node("save_results",ai_news_node.save_result)
         #added edges
         self.graph_builder.add_edge(START,"fetch_news")
         self.graph_builder.add_edge("fetch_news","summarize_news")
         self.graph_builder.add_edge("summarize_news","save_results")
         self.graph_builder.add_edge("save_results",END)   
         
    
    
    def setup_graph(self,usecase: str):
         if usecase=="Basic Chatbot":
              self.basic_chatbot_build_graph()
         if usecase=="Chatbot With Web":
              self.chatbot_with_tools_build_graph()    
         if usecase=="AI News":
              self.ai_news_builder_graph()    
         return self.graph_builder.compile()    