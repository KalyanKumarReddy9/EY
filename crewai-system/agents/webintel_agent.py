"""
Web Intelligence Agent for online research
"""
import requests
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
import re

# Import Gemini web search integration
from data_sources import gemini_websearch

# Load environment variables
load_dotenv()

def extract_medical_condition(query):
    """
    Extract medical condition from user query
    
    Args:
        query (str): User query
        
    Returns:
        str: Extracted medical condition
    """
    # Common patterns to extract medical conditions
    patterns = [
        r'for\s+(.+?)\s+treatment',
        r'for\s+(.+?)\s+patients',
        r'for\s+(.+?)\s+therapy',
        r'clinical trials for\s+(.+)',
        r'diabetes\s+(.+?)\s+treatment',
        r'treatment\s+for\s+(.+)',
        r'(diabetes|cancer|alzheimer|parkinson|cardiovascular|autoimmune)\s*(?:treatment|therapy|disease|condition)?'
    ]
    
    query_lower = query.lower().strip()
    
    # Try each pattern
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            condition = match.group(1).strip()
            # Clean up the extracted condition
            condition = re.sub(r'\s+', ' ', condition)  # Remove extra spaces
            condition = re.sub(r'[^\w\s]', '', condition)  # Remove punctuation
            if condition and len(condition) > 1:
                return condition
    
    # If no pattern matches, use common medical terms
    medical_terms = [
        "diabetes", "cancer", "alzheimer", "parkinson", "cardiovascular", 
        "autoimmune", "infectious disease", "gene therapy", "immunotherapy",
        "antibody", "vaccine", "neurological disorder", "metabolic disorder",
        "chronic pain", "mental health", "rare disease", "pediatric medicine"
    ]
    
    for term in medical_terms:
        if term in query_lower:
            return term
    
    # Default fallback
    return "medical research"

def search_web(query, num_results=5):
    """
    Perform web search using Google Gemini API
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
    
    Returns:
        list: List of search results
    """
    try:
        # Extract clean medical condition from query
        clean_query = extract_medical_condition(query)
        
        # Use Gemini web search integration with cleaned query
        results = gemini_websearch.search_with_gemini(clean_query, num_results)
        return results
        
    except Exception as e:
        print(f"Error in Web Intelligence agent: {str(e)}")
        # Return mock data as fallback
        return get_mock_web_results(query, num_results)

def get_mock_web_results(query, num_results=5):
    """
    Generate mock web search results for testing
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
    
    Returns:
        list: List of mock search results
    """
    # Extract clean medical condition from query
    clean_query = extract_medical_condition(query)
    
    mock_sources = [
        "Nature Medicine", "Science Translational Medicine", "The Lancet", "New England Journal of Medicine",
        "Journal of Clinical Investigation", "Cell", "BMJ", "Mayo Clinic Proceedings",
        "Cleveland Clinic Journal of Medicine", "Harvard Health Publishing"
    ]
    
    # Different types of research topics for variety
    research_topics = [
        f"breakthrough {clean_query} treatment discovery",
        f"latest {clean_query} clinical research findings",
        f"innovative {clean_query} therapy approaches",
        f"new {clean_query} drug development",
        f"emerging {clean_query} treatment protocols"
    ]
    
    mock_results = []
    
    for i in range(min(num_results, 10)):
        # Select a research topic
        topic = random.choice(research_topics)
        
        mock_result = {
            "title": f"Recent Advances in {clean_query.title()} Treatment - {random.choice(['Study', 'Research', 'Analysis', 'Review'])}",
            "snippet": f"Scientists have made significant progress in {clean_query} treatment with new therapeutic approaches showing promising results in recent clinical trials. This research focuses on improving patient outcomes through innovative methodologies.",
            "link": f"https://www.{random.choice(['nature.com', 'science.org', 'thelancet.com'])}/research/{clean_query.replace(' ', '-')}-{i+1}",
            "source": random.choice(mock_sources)
        }
        mock_results.append(mock_result)
    
    return mock_results

def get_news_articles(topic, days_back=7):
    """
    Get recent news articles about a topic
    
    Args:
        topic (str): Topic to search for
        days_back (int): Number of days to look back
    
    Returns:
        list: List of news articles
    """
    # For now, return mock data
    # In a real implementation, you might use a news API
    return get_mock_web_results(f"{topic} news", 3)

def get_guidelines(topic):
    """
    Get medical guidelines about a topic
    
    Args:
        topic (str): Medical topic to search for guidelines
    
    Returns:
        list: List of guideline documents
    """
    # For now, return mock data
    return get_mock_web_results(f"{topic} medical guidelines", 2)

# Example usage:
# results = search_web("diabetes treatment", num_results=5)
# news = get_news_articles("cancer research")
# guidelines = get_guidelines("hypertension")