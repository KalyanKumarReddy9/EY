"""
Patent Agent for intellectual property analysis
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
import re

# Import data sources
from data_sources import bigquery_patents, pubmed_patents

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

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
    return "medical condition"

def search_patents(query, assignee=None, ipc_code=None, top_n=10, database_name="pharma_hub"):
    """
    Search patents by query, assignee, or IPC code
    
    Args:
        query (str): Search query for patent titles/abstracts
        assignee (str): Optional assignee filter
        ipc_code (str): Optional IPC code filter
        top_n (int): Number of results to return
        database_name (str): Name of the MongoDB database
    
    Returns:
        list: List of patents
    """
    try:
        # First try to get real data from BigQuery
        bigquery_patents_data = bigquery_patents.search_patents_bigquery(query, limit=top_n)
        if bigquery_patents_data:
            return bigquery_patents_data
            
        # If BigQuery fails, try PubMed
        pubmed_patents_data = pubmed_patents.search_patents_pubmed(query, top_n)
        if pubmed_patents_data:
            return pubmed_patents_data
            
        # If PubMed fails, fall back to MongoDB
        client = get_mongo_client()
        db = client[database_name]
        
        # Check if we have data in the database
        count = db["patents"].count_documents({})
        if count == 0:
            print("No patent data found in database, returning mock data")
            return get_mock_patent_data(query, top_n)
        
        # Build query
        mongo_query = {"$text": {"$search": query}} if query else {}
        if assignee:
            mongo_query["assignee"] = {"$regex": assignee, "$options": "i"}
        if ipc_code:
            mongo_query["ipc_codes"] = {"$regex": ipc_code, "$options": "i"}
        
        # Find patents
        patents = list(db["patents"].find(mongo_query).limit(top_n))
        
        # Format results
        formatted_patents = []
        for patent in patents:
            formatted_patent = {
                "patent_id": patent.get("patent_id"),
                "title": patent.get("title"),
                "assignee": patent.get("assignee"),
                "filing_date": patent.get("filing_date"),
                "grant_date": patent.get("grant_date"),
                "expiry_date": patent.get("expiry_date"),
                "ipc_codes": patent.get("ipc_codes", [])
            }
            formatted_patents.append(formatted_patent)
        
        return formatted_patents
        
    except Exception as e:
        print(f"Error in Patent agent: {str(e)}")
        # Return mock data as fallback
        return get_mock_patent_data(query, top_n)
    finally:
        if 'client' in locals():
            client.close()

def get_patent_statistics(database_name="pharma_hub"):
    """
    Get statistics about patents in the database
    
    Args:
        database_name (str): Name of the MongoDB database
    
    Returns:
        dict: Statistics about patents
    """
    try:
        # Try to get real data from BigQuery (using a default query term)
        bigquery_stats = bigquery_patents.get_patent_statistics_bigquery("pharmaceutical")
        if bigquery_stats:
            return bigquery_stats
            
        # If BigQuery fails, fall back to MongoDB
        client = get_mongo_client()
        db = client[database_name]
        
        # Check if we have data in the database
        count = db["patents"].count_documents({})
        if count == 0:
            print("No patent data found in database, returning mock statistics")
            return get_mock_patent_statistics()
        
        # Get total count
        total_patents = db["patents"].count_documents({})
        
        # Get assignee distribution
        assignee_pipeline = [
            {"$group": {"_id": "$assignee", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        top_assignees = list(db["patents"].aggregate(assignee_pipeline))
        
        # Get recent patents (last 5 years)
        five_years_ago = (datetime.now() - timedelta(days=5*365)).strftime("%Y-%m-%d")
        recent_patents = db["patents"].count_documents({"filing_date": {"$gte": five_years_ago}})
        
        # Get expiring patents (next 5 years)
        five_years_ahead = (datetime.now() + timedelta(days=5*365)).strftime("%Y-%m-%d")
        expiring_patents = db["patents"].count_documents({
            "expiry_date": {
                "$gte": datetime.now().strftime("%Y-%m-%d"),
                "$lte": five_years_ahead
            }
        })
        
        stats = {
            "total_patents": total_patents,
            "recent_patents": recent_patents,
            "expiring_patents": expiring_patents,
            "top_assignees": [{"assignee": item["_id"], "count": item["count"]} for item in top_assignees]
        }
        
        return stats
        
    except Exception as e:
        print(f"Error in Patent agent statistics: {str(e)}")
        # Return mock data as fallback
        return get_mock_patent_statistics()
    finally:
        if 'client' in locals():
            client.close()

def get_mock_patent_data(query, count=10):
    """
    Generate mock patent data for testing
    
    Args:
        query (str): Query term to include in mock data
        count (int): Number of mock patents to generate
    
    Returns:
        list: List of mock patents
    """
    # Extract clean medical condition from query
    clean_query = extract_medical_condition(query)
    
    # Medical and pharmaceutical related topics for better mock data
    medical_topics = [
        "diabetes", "cancer", "alzheimer", "parkinson", "cardiovascular", 
        "autoimmune", "infectious disease", "gene therapy", "immunotherapy",
        "antibody", "vaccine", "neurological disorder", "metabolic disorder",
        "chronic pain", "mental health", "rare disease", "pediatric medicine"
    ]
    
    # If we couldn't extract a good condition, use a random medical topic
    if clean_query == "medical condition" or len(clean_query) < 2:
        clean_query = random.choice(medical_topics)
    
    assignees = [
        'Pfizer Inc.', 
        'Johnson & Johnson', 
        'Roche', 
        'Novartis', 
        'Merck & Co.',
        'AbbVie', 
        'Sanofi', 
        'GlaxoSmithKline', 
        'AstraZeneca',
        'Bristol-Myers Squibb',
        'Generic Pharmaceuticals Ltd.',
        'Biotech Innovations Inc.'
    ]
    
    ipc_codes = [
        'A61K31/00', 'A61K31/125', 'A61K31/195', 'A61K31/40', 'A61K31/415',
        'A61K31/44', 'A61K31/47', 'A61K31/55', 'A61K31/60', 'A61K31/70'
    ]
    
    mock_patents = []
    for i in range(count):
        # Generate random dates
        filing_date = (datetime.now() - timedelta(days=random.randint(365, 365*10))).strftime("%Y-%m-%d")
        grant_date = (datetime.strptime(filing_date, "%Y-%m-%d") + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        expiry_date = (datetime.strptime(grant_date, "%Y-%m-%d") + timedelta(days=365*20)).strftime("%Y-%m-%d")
        
        # Create a more realistic title based on the query
        title_templates = [
            f"Method for treating {clean_query} using novel compounds",
            f"Composition for the treatment of {clean_query}",
            f"Therapeutic agent targeting {clean_query} pathways",
            f"Pharmaceutical formulation for {clean_query} therapy",
            f"Methods and compositions for modulating {clean_query} activity",
            f"Antibodies for the treatment of {clean_query}",
            f"Combination therapy for {clean_query} patients",
            f"Novel inhibitors for {clean_query} treatment"
        ]
        
        mock_patent = {
            "patent_id": f"US{random.randint(1000000, 9999999)}{random.choice(['A1', 'B1', 'B2'])}",
            "title": random.choice(title_templates),
            "assignee": random.choice(assignees),
            "filing_date": filing_date,
            "grant_date": grant_date,
            "expiry_date": expiry_date,
            "ipc_codes": random.sample(ipc_codes, k=random.randint(1, 3))
        }
        mock_patents.append(mock_patent)
    
    return mock_patents

def get_mock_patent_statistics():
    """
    Generate mock patent statistics for testing
    
    Returns:
        dict: Mock patent statistics
    """
    mock_assignees = [
        {"assignee": "Pfizer Inc.", "count": 1247},
        {"assignee": "Johnson & Johnson", "count": 982},
        {"assignee": "Roche", "count": 876},
        {"assignee": "Novartis", "count": 754},
        {"assignee": "Merck & Co.", "count": 689},
        {"assignee": "AbbVie", "count": 543},
        {"assignee": "Sanofi", "count": 498},
        {"assignee": "AstraZeneca", "count": 432}
    ]
    
    stats = {
        "total_patents": 15420,
        "recent_patents": 3420,
        "expiring_patents": 1250,
        "top_assignees": mock_assignees
    }
    
    return stats

# Example usage:
# patents = search_patents("cancer", assignee="Pfizer")
# stats = get_patent_statistics()
# mock_patents = get_mock_patent_data("diabetes", count=3)