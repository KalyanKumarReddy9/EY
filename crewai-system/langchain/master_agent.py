"""
LangChain Master Agent for orchestrating worker agents
"""
import os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
from agents import exim_agent, trials_agent, iqvia_agent, patent_agent, webintel_agent, internal_agent

# Load environment variables
load_dotenv()

def get_llm():
    """
    Initialize and return the LLM
    
    Returns:
        HuggingFaceHub: Initialized LLM
    """
    try:
        # Get Hugging Face token
        hf_token = os.environ.get("HF_TOKEN")
        if not hf_token:
            raise ValueError("HF_TOKEN not found in environment variables")
        
        # Initialize Hugging Face LLM
        # Using a smaller model for faster inference
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-base",  # You can change this to a different model
            model_kwargs={"temperature": 0.7, "max_length": 900},
            huggingfacehub_api_token=hf_token
        )
        
        return llm
    except Exception as e:
        print(f"Error initializing LLM: {str(e)}")
        raise

def get_tools():
    """
    Create and return the tools for the agent
    
    Returns:
        list: List of Tool objects
    """
    tools = [
        Tool(
            name="EXIMQuery",
            func=lambda x: exim_agent.get_trade_by_hs(x.split('|')[0], 
                                                     year_from=x.split('|')[1] if '|' in x and len(x.split('|')) > 1 else None,
                                                     top_n=int(x.split('|')[2]) if '|' in x and len(x.split('|')) > 2 else 10),
            description="Get trade partners and volumes for HS codes. Input format: 'hs_code|year_from|top_n' (year_from and top_n are optional)"
        ),
        Tool(
            name="TrialsQuery",
            func=lambda x: trials_agent.search_trials(x.split('|')[0],
                                                    phase=x.split('|')[1] if '|' in x and len(x.split('|')) > 1 else None,
                                                    status=x.split('|')[2] if '|' in x and len(x.split('|')) > 2 else None,
                                                    top_n=int(x.split('|')[3]) if '|' in x and len(x.split('|')) > 3 else 10),
            description="Search clinical trials by condition. Input format: 'condition|phase|status|top_n' (phase, status, and top_n are optional)"
        ),
        Tool(
            name="IQVIAQuery",
            func=lambda x: iqvia_agent.get_market_stats(x),
            description="Get market size and CAGR for therapy areas. Input: therapy area name"
        ),
        Tool(
            name="PatentQuery",
            func=lambda x: patent_agent.search_patents(x.split('|')[0],
                                                     assignee=x.split('|')[1] if '|' in x and len(x.split('|')) > 1 else None,
                                                     ipc_code=x.split('|')[2] if '|' in x and len(x.split('|')) > 2 else None,
                                                     top_n=int(x.split('|')[3]) if '|' in x and len(x.split('|')) > 3 else 10),
            description="Search patents by query, assignee, or IPC code. Input format: 'query|assignee|ipc_code|top_n' (assignee, ipc_code, and top_n are optional)"
        ),
        Tool(
            name="WebQuery",
            func=lambda x: webintel_agent.search_web(x, num_results=5),
            description="Run web intelligence search (news/guidelines). Input: search query"
        ),
        Tool(
            name="InternalDocsQuery",
            func=lambda x: internal_agent.search_internal_documents(x, top_n=5),
            description="Search internal documents. Input: search query"
        )
    ]
    
    return tools

def initialize_master_agent():
    """
    Initialize and return the master agent
    
    Returns:
        AgentExecutor: Initialized agent
    """
    try:
        # Get LLM
        llm = get_llm()
        
        # Get tools
        tools = get_tools()
        
        # Initialize agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True
        )
        
        return agent
    except Exception as e:
        print(f"Error initializing master agent: {str(e)}")
        raise

def run_master_agent(query):
    """
    Run the master agent with a query
    
    Args:
        query (str): User query
    
    Returns:
        str: Agent response
    """
    try:
        # Initialize agent
        agent = initialize_master_agent()
        
        # Run agent
        response = agent.run(query)
        return response
    except Exception as e:
        print(f"Error running master agent: {str(e)}")
        return f"Error processing query: {str(e)}"

# Example usage:
# response = run_master_agent("What are the top trading partners for HS code 3004 in 2022?")