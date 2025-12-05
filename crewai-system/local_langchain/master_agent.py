"""
LangChain Master Agent for orchestrating worker agents
"""
import os
from dotenv import load_dotenv
# Updated imports for LangChain v0.1.x
from langchain_core.tools import Tool
from agents import exim_agent, trials_agent, iqvia_agent, patent_agent, webintel_agent, internal_agent

# Load environment variables
load_dotenv()

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

def run_master_agent(query):
    """
    Run the master agent with a query
    
    Args:
        query (str): User query
    
    Returns:
        str: Agent response
    """
    try:
        # For now, we'll return a mock response
        # In a full implementation, we would run the actual agent
        return f"Mock response for query: {query}"
    except Exception as e:
        print(f"Error running master agent: {str(e)}")
        return f"Error processing query: {str(e)}"

# Example usage:
# response = run_master_agent("What are the top trading partners for HS code 3004 in 2022?")