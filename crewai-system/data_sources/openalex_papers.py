"""
OpenAlex integration for fetching academic papers as an alternative to PubMed
"""
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

def search_papers_openalex(query_term, limit=10):
    """
    Search for academic papers using OpenAlex API
    
    Args:
        query_term (str): Term to search for in paper titles/abstracts
        limit (int): Maximum number of results to return
        
    Returns:
        list: List of paper records
    """
    try:
        # Get base URL from environment
        base_url = os.environ.get("OPENALEX_API_BASE", "https://api.openalex.org")
        
        # Construct URL for works endpoint
        url = f"{base_url}/works"
        
        # Parameters for search
        params = {
            "search": query_term,
            "per-page": min(limit, 25),  # OpenAlex limit is 25 per page
            "sort": "cited_by_count:desc"  # Sort by citations
        }
        
        # Make request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse results
        data = response.json()
        papers = []
        
        for work in data.get("results", []):
            # Extract relevant information
            paper = {
                "paper_id": work.get("id", ""),
                "doi": work.get("doi", ""),
                "title": work.get("title", ""),
                "abstract": work.get("abstract", "")[:500] + "..." if work.get("abstract") and len(work.get("abstract", "")) > 500 else work.get("abstract", ""),
                "publication_date": work.get("publication_date", ""),
                "authorships": [],
                "concepts": [],
                "cited_by_count": work.get("cited_by_count", 0),
                "journal": work.get("primary_location", {}).get("source", {}).get("display_name", "") if work.get("primary_location") else "",
                "type": work.get("type", "")
            }
            
            # Extract authors
            for authorship in work.get("authorships", []):
                author = authorship.get("author", {})
                institution = authorship.get("institutions", [{}])[0] if authorship.get("institutions") else {}
                
                paper["authorships"].append({
                    "author_name": author.get("display_name", ""),
                    "institution": institution.get("display_name", ""),
                    "position": authorship.get("author_position", "")
                })
            
            # Extract concepts (topics)
            for concept in work.get("concepts", []):
                if concept.get("level") <= 2:  # Only top-level concepts
                    paper["concepts"].append({
                        "name": concept.get("display_name", ""),
                        "score": concept.get("score", 0)
                    })
            
            papers.append(paper)
            
        return papers
        
    except Exception as e:
        print(f"Error searching papers in OpenAlex: {str(e)}")
        return []

def get_paper_statistics_openalex(query_term):
    """
    Get statistics about papers from OpenAlex
    
    Args:
        query_term (str): Term to search for in paper titles/abstracts
        
    Returns:
        dict: Statistics about papers
    """
    try:
        # Get base URL from environment
        base_url = os.environ.get("OPENALEX_API_BASE", "https://api.openalex.org")
        
        # Search for papers
        papers = search_papers_openalex(query_term, limit=50)
        
        if not papers:
            return None
            
        # Calculate statistics
        total_papers = len(papers)
        total_citations = sum(paper["cited_by_count"] for paper in papers)
        avg_citations = total_citations / total_papers if total_papers > 0 else 0
        
        # Top journals
        journal_counts = {}
        for paper in papers:
            journal = paper.get("journal", "")
            if journal:
                journal_counts[journal] = journal_counts.get(journal, 0) + 1
                
        top_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Top concepts
        concept_counts = {}
        for paper in papers:
            for concept in paper.get("concepts", []):
                name = concept.get("name", "")
                if name:
                    concept_counts[name] = concept_counts.get(name, 0) + 1
                    
        top_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        stats = {
            "total_papers": total_papers,
            "total_citations": total_citations,
            "average_citations_per_paper": round(avg_citations, 2),
            "top_journals": [{"journal": j[0], "count": j[1]} for j in top_journals],
            "top_concepts": [{"concept": c[0], "count": c[1]} for c in top_concepts]
        }
        
        return stats
        
    except Exception as e:
        print(f"Error getting paper statistics from OpenAlex: {str(e)}")
        return None

# Example usage:
# papers = search_papers_openalex("diabetes treatment", limit=5)
# stats = get_paper_statistics_openalex("diabetes treatment")