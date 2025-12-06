"""
Patent Agent for searching patent information
"""
import os
from dotenv import load_dotenv
from data_sources import pubmed_patents, openalex_papers

# Load environment variables
load_dotenv()

def search_patents(query, assignee=None, ipc_code=None, top_n=10):
    """
    Search for patents using multiple data sources
    
    Args:
        query (str): Search query
        assignee (str): Assignee name to filter by
        ipc_code (str): IPC code to filter by
        top_n (int): Number of results to return
        
    Returns:
        dict: Search results with metadata
    """
    try:
        # Try to get data from PubMed first
        pubmed_results = pubmed_patents.search_patents_pubmed(query, top_n)
        
        # If PubMed returns results, use them
        if pubmed_results and len(pubmed_results) > 0:
            print(f"Found {len(pubmed_results)} patents from PubMed")
            # Filter by assignee if specified
            if assignee:
                pubmed_results = [p for p in pubmed_results if assignee.lower() in p.get('assignee', '').lower()]
            
            # Filter by IPC code if specified
            if ipc_code:
                pubmed_results = [p for p in pubmed_results if ipc_code in str(p.get('ipc_codes', []))]
            
            return {
                "data": pubmed_results[:top_n],
                "source": "PubMed",
                "query": f"Patent search for {query}",
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
        
        # If no PubMed results, try OpenAlex as fallback
        print("No PubMed results found, trying OpenAlex as fallback")
        openalex_results = openalex_papers.search_papers_openalex(query, top_n)
        
        if openalex_results and len(openalex_results) > 0:
            print(f"Found {len(openalex_results)} papers from OpenAlex")
            # Convert papers to patent-like format
            patent_like_results = []
            for paper in openalex_results[:top_n]:
                patent_entry = {
                    "patent_id": paper.get("paper_id", "").split("/")[-1] if paper.get("paper_id") else f"OA{__import__('random').randint(10000000, 99999999)}",
                    "title": paper.get("title", ""),
                    "assignee": ", ".join([author["author_name"] for author in paper.get("authorships", [])[:3]]) if paper.get("authorships") else "Unknown Authors",
                    "filing_date": paper.get("publication_date", "Unknown"),
                    "grant_date": paper.get("publication_date", "Unknown"),
                    "expiry_date": "N/A (Academic Paper)",
                    "ipc_codes": [concept["name"] for concept in paper.get("concepts", [])[:3]] if paper.get("concepts") else ["Academic Research"]
                }
                patent_like_results.append(patent_entry)
            
            return {
                "data": patent_like_results,
                "source": "OpenAlex (converted to patent format)",
                "query": f"Patent search for {query}",
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
        
        # If no results from either source, return mock data
        print("No results from PubMed or OpenAlex, returning mock data")
        mock_data = pubmed_patents.get_mock_patent_data(query, top_n)
        return {
            "data": mock_data,
            "source": "Mock Data",
            "query": f"Patent search for {query}",
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in patent search: {str(e)}")
        # Return mock data as final fallback
        mock_data = pubmed_patents.get_mock_patent_data(query, top_n)
        return {
            "data": mock_data,
            "source": "Mock Data (Error Fallback)",
            "query": f"Patent search for {query}",
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "error": str(e)
        }

# Example usage:
# results = search_patents("diabetes treatment", top_n=5)
