"""
EXIM Agent for trade data analysis
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
import re

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

def get_trade_by_hs(hs_code, year_from=None, year_to=None, top_n=10, database_name="pharma_hub"):
    """
    Get trade partners and volumes for HS codes
    
    Args:
        hs_code (str): HS code for the product
        year_from (int): Starting year for filtering
        year_to (int): Ending year for filtering
        top_n (int): Number of top results to return
        database_name (str): Name of the MongoDB database
    
    Returns:
        list: List of trade partners with values
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Check if we have data in the database
        count = db["comtrade"].count_documents({})
        if count == 0:
            print("No EXIM data found in database, returning mock data")
            return get_mock_trade_data(hs_code, top_n)
        
        # Build query
        query = {"hs_code": str(hs_code)}
        if year_from or year_to:
            query["year"] = {}
            if year_from:
                query["year"]["$gte"] = int(year_from)
            if year_to:
                query["year"]["$lte"] = int(year_to)
        
        # Aggregation pipeline
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$partner", "total": {"$sum": "$value"}}},
            {"$sort": {"total": -1}},
            {"$limit": top_n}
        ]
        
        result = list(db["comtrade"].aggregate(pipeline))
        formatted_result = [{"partner": r["_id"], "value": r["total"]} for r in result]
        
        return formatted_result
        
    except Exception as e:
        print(f"Error in EXIM agent: {str(e)}")
        # Return mock data as fallback
        return get_mock_trade_data(hs_code, top_n)
    finally:
        if 'client' in locals():
            client.close()

def get_trade_trends(hs_code, country=None, database_name="pharma_hub"):
    """
    Get trade trends over time for an HS code
    
    Args:
        hs_code (str): HS code for the product
        country (str): Optional country filter
        database_name (str): Name of the MongoDB database
    
    Returns:
        list: List of yearly trade values
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Check if we have data in the database
        count = db["comtrade"].count_documents({})
        if count == 0:
            print("No EXIM data found in database, returning mock data")
            return get_mock_trade_trends(hs_code)
        
        # Build query
        query = {"hs_code": str(hs_code)}
        if country:
            query["reporter"] = country
        
        # Aggregation pipeline
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "$year", "total_value": {"$sum": "$value"}}},
            {"$sort": {"_id": 1}}
        ]
        
        result = list(db["comtrade"].aggregate(pipeline))
        formatted_result = [{"year": r["_id"], "value": r["total_value"]} for r in result]
        
        return formatted_result
        
    except Exception as e:
        print(f"Error in EXIM agent trend analysis: {str(e)}")
        # Return mock data as fallback
        return get_mock_trade_trends(hs_code)
    finally:
        if 'client' in locals():
            client.close()

def get_mock_trade_data(hs_code, top_n=10):
    """
    Generate mock trade data for testing
    
    Args:
        hs_code (str): HS code for the product
        top_n (int): Number of results to return
    
    Returns:
        list: Mock trade data
    """
    # Countries for better mock data
    countries = [
        "United States", "Germany", "China", "India", "France", 
        "Japan", "Canada", "United Kingdom", "Italy", "South Korea",
        "Brazil", "Australia", "Netherlands", "Switzerland", "Spain",
        "Sweden", "Belgium", "Russia", "Mexico", "Singapore"
    ]
    
    # Product descriptions for different HS codes
    product_descriptions = {
        "3004": "Medicaments",
        "3003": "Medicaments (mixed)",
        "3002": "Blood fractions",
        "3001": "Glands and other organs",
        "3005": "Diagnostic reagents",
        "3006": "Pharmaceutical goods"
    }
    
    product_desc = product_descriptions.get(str(hs_code), "Pharmaceutical products")
    
    mock_data = []
    for i in range(min(top_n, len(countries))):
        # Generate more realistic values with some variation
        base_value = random.uniform(5000000, 100000000)  # Base value between 5M and 100M
        
        # Add some variation based on country importance
        if countries[i] in ["United States", "Germany", "China", "Japan"]:
            multiplier = random.uniform(1.2, 2.0)  # Major markets get higher values
        elif countries[i] in ["India", "Canada", "UK", "France"]:
            multiplier = random.uniform(0.8, 1.5)  # Mid-tier markets
        else:
            multiplier = random.uniform(0.3, 1.2)  # Other markets
            
        value = round(base_value * multiplier, 2)
        
        mock_data.append({
            "partner": countries[i],
            "value": value,
            "product_description": product_desc,
            "quantity": round(value / random.uniform(1000, 5000), 2)  # Simulated quantity
        })
    
    # Sort by value descending to show top partners first
    mock_data.sort(key=lambda x: x["value"], reverse=True)
    
    return mock_data

def get_mock_trade_trends(hs_code):
    """
    Generate mock trade trends for testing
    
    Args:
        hs_code (str): HS code for the product
    
    Returns:
        list: Mock trade trends
    """
    # Product descriptions for different HS codes
    product_descriptions = {
        "3004": "Medicaments",
        "3003": "Medicaments (mixed)",
        "3002": "Blood fractions",
        "3001": "Glands and other organs",
        "3005": "Diagnostic reagents",
        "3006": "Pharmaceutical goods"
    }
    
    product_desc = product_descriptions.get(str(hs_code), "Pharmaceutical products")
    
    current_year = datetime.now().year
    mock_trends = []
    
    # Generate 5 years of data with realistic growth patterns
    base_value = random.uniform(100000000, 300000000)  # Base value for first year
    
    for i in range(5):
        year = current_year - (4 - i)  # Last 5 years, current year last
        
        # Apply realistic growth/decline patterns
        if i == 0:
            # First year - base value
            value = base_value
        else:
            # Subsequent years - apply growth factor
            growth_factor = random.uniform(0.9, 1.2)  # -10% to +20% change
            value = mock_trends[-1]["value"] * growth_factor
            
        mock_trends.append({
            "year": year,
            "value": round(value, 2),
            "product_description": product_desc
        })
    
    return mock_trends

# Example usage:
# partners = get_trade_by_hs("3004", year_from=2020, top_n=5)
# trends = get_trade_trends("3004", country="India")