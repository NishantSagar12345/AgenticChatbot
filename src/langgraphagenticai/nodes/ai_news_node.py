from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
class AINewsNode:
    def __init__(self,llm):
       """
       Initialize the AINewsNode with API Keys for Tavily and GROQ
       """
       self.tavily=TavilyClient()
       self.llm=llm
       self.state={}

    def fetch_news(self,state:dict)->dict:
        """
        Fetch AI news based on the specified frequency
        args:
            state (dict): The state dictionary containing 'frequency'

        Returns:
            dict: Uodated state with news data key containing fetched news     
        """   
        frequency=state['messages'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map={'daily':'d','weekly':'w','monthly':'m','year':'y'}
        days_map={'daily':1,'weekly':7,'monthly':30,'year':366}
        response=self.tavily.search(
            query="Top Artificial Intelligence (AI) Technology news India adn globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
        )
        state['news_data']=response.get('results',[])
        self.state['news_data']=state['news_data']
        return state
    def summarize_news(self,state:dict)->dict:
        """
        Summarize the fetched news using an LLM
        Args:
           state (dict): The state dictionary containing 'news data'
        Returns:
           dict: Updated state with summary key containing the summarized news   
        """
        news_items = self.state['news_data']

        # Create the prompt template with proper structure
        prompt_template = ChatPromptTemplate.from_messages([
            {"role": "system", "content": """Summarize AI News articles into markdown format. For each item include:
            - Date in **DD-MM-YYYY** format in IST timezone
            - Concise sentence summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link and keep it seperate form summary
            - Write the news from the same day into same section
            Use format:
            [Date] 
            - [Summary] [URL]"""},

            {"role": "user", "content": "Articles:\n{articles}"}
        ])

        # Join the articles into one string
        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        # Format the prompt
        formatted_prompt = prompt_template.format_prompt(articles=articles_str)

        # Send the prompt to the LLM
        response = self.llm.invoke(formatted_prompt)
 
        clean_content = response.content.replace('\u2011', '-')

# Optionally, replace other problematic characters too
# Example: remove characters that can't be encoded in 'ascii'
        clean_content = clean_content.encode('ascii', errors='ignore').decode('ascii')

# Save the cleaned response
        self.state['summary'] = clean_content
        self.state['summary'] = clean_content

        return self.state

    def save_result(self,state):
        frequency=self.state['frequency']
        summary=self.state['summary']
        filename=f"./AINews/{frequency}_summary.md"
        with open(filename,"w") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary")
            f.write(summary)
        self.state['filename']=filename
        return self.state        



