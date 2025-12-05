"""
Clinical Trials Agent
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

def search_trials(condition, phase=None, status=None, top_n=10, database_name="pharma_hub"):
    """
    Search clinical trials by condition
    
    Args:
        condition (str): Medical condition to search for
        phase (str): Optional phase filter (e.g., "Phase 1", "Phase 2")
        status (str): Optional status filter (e.g., "Recruiting", "Completed")
        top_n (int): Number of results to return
        database_name (str): Name of the MongoDB database
    
    Returns:
        list: List of clinical trials
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Check if we have data in the database
        count = db["clinical_trials"].count_documents({})
        if count == 0:
            print("No clinical trials data found in database, returning mock data")
            return get_mock_trials(condition, phase, status, top_n)
        
        # Build query
        query = {"condition": {"$regex": condition, "$options": "i"}}
        if phase:
            query["phase"] = {"$regex": phase, "$options": "i"}
        if status:
            query["status"] = {"$regex": status, "$options": "i"}
        
        # Find trials
        trials = list(db["clinical_trials"].find(query).limit(top_n))
        
        # Format results
        formatted_trials = []
        for trial in trials:
            formatted_trial = {
                "nct_id": trial.get("nct_id"),
                "title": trial.get("title"),
                "condition": trial.get("condition"),
                "phase": trial.get("phase"),
                "status": trial.get("status"),
                "sponsor": trial.get("sponsor")
            }
            formatted_trials.append(formatted_trial)
        
        return formatted_trials
        
    except Exception as e:
        print(f"Error in Trials agent: {str(e)}")
        # Return mock data as fallback
        return get_mock_trials(condition, phase, status, top_n)
    finally:
        if 'client' in locals():
            client.close()

def get_trial_statistics(database_name="pharma_hub"):
    """
    Get statistics about clinical trials in the database
    
    Args:
        database_name (str): Name of the MongoDB database
    
    Returns:
        dict: Statistics about clinical trials
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Check if we have data in the database
        count = db["clinical_trials"].count_documents({})
        if count == 0:
            print("No clinical trials data found in database, returning mock statistics")
            return get_mock_trial_statistics()
        
        # Get total count
        total_trials = db["clinical_trials"].count_documents({})
        
        # Get phase distribution
        phase_pipeline = [
            {"$group": {"_id": "$phase", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        phase_distribution = list(db["clinical_trials"].aggregate(phase_pipeline))
        
        # Get status distribution
        status_pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        status_distribution = list(db["clinical_trials"].aggregate(status_pipeline))
        
        # Get top sponsors
        sponsor_pipeline = [
            {"$group": {"_id": "$sponsor", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        top_sponsors = list(db["clinical_trials"].aggregate(sponsor_pipeline))
        
        stats = {
            "total_trials": total_trials,
            "phase_distribution": [{"phase": item["_id"], "count": item["count"]} for item in phase_distribution],
            "status_distribution": [{"status": item["_id"], "count": item["count"]} for item in status_distribution],
            "top_sponsors": [{"sponsor": item["_id"], "count": item["count"]} for item in top_sponsors]
        }
        
        return stats
        
    except Exception as e:
        print(f"Error in Trials agent statistics: {str(e)}")
        # Return mock data as fallback
        return get_mock_trial_statistics()
    finally:
        if 'client' in locals():
            client.close()

def get_mock_trials(condition, phase=None, status=None, top_n=10):
    """
    Generate mock clinical trials data for testing
    
    Args:
        condition (str): Medical condition to search for
        phase (str): Optional phase filter
        status (str): Optional status filter
        top_n (int): Number of results to return
    
    Returns:
        list: Mock clinical trials data
    """
    # Extract clean medical condition from query
    clean_condition = extract_medical_condition(condition)
    
    # Medical conditions for better mock data
    medical_conditions = [
        "Type 2 Diabetes", "Hypertension", "Breast Cancer", "Alzheimer's Disease",
        "Rheumatoid Arthritis", "Asthma", "Major Depressive Disorder", "Osteoporosis",
        "Chronic Obstructive Pulmonary Disease", "Heart Failure", "Multiple Sclerosis",
        "Parkinson's Disease", "Crohn's Disease", "Psoriasis", "Migraine"
    ]
    
    # If we couldn't extract a good condition, use a medical condition
    if clean_condition == "medical condition" or len(clean_condition) < 2:
        clean_condition = random.choice(medical_conditions)
    
    mock_phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
    mock_statuses = ["Recruiting", "Active, not recruiting", "Completed", "Terminated", "Not yet recruiting"]
    mock_sponsors = [
        "National Institutes of Health", "Pfizer Inc.", "Johnson & Johnson", 
        "Roche Pharmaceuticals", "Novartis AG", "Merck & Co.",
        "AbbVie Inc.", "Sanofi S.A.", "GlaxoSmithKline plc", "AstraZeneca"
    ]
    
    # More diverse study titles
    title_templates = [
        f"A Phase {phase or random.choice(mock_phases)} Study of Novel Treatment for {clean_condition}",
        f"Efficacy and Safety of Investigational Drug in {clean_condition} Patients",
        f"Randomized Controlled Trial: {clean_condition} Treatment Outcomes",
        f"Long-term Follow-up Study of {clean_condition} Therapy",
        f"Comparative Effectiveness of Treatments for {clean_condition}",
        f"Biomarker Analysis in {clean_condition} Clinical Trial",
        f"Dose-ranging Study for {clean_condition} Management",
        f"Real-world Evidence Study of {clean_condition} Interventions"
    ]
    
    mock_trials = []
    for i in range(min(top_n, 15)):  # Limit to 15 for realistic results
        # Generate more realistic NCT IDs
        nct_number = random.randint(1000000, 9999999)
        
        mock_trials.append({
            "nct_id": f"NCT{nct_number:08d}",
            "title": random.choice(title_templates),
            "condition": clean_condition.title(),
            "phase": phase or random.choice(mock_phases),
            "status": status or random.choice(mock_statuses),
            "sponsor": random.choice(mock_sponsors)
        })
    
    return mock_trials

def get_mock_trial_statistics():
    """
    Generate mock clinical trials statistics for testing
    
    Returns:
        dict: Mock clinical trials statistics
    """
    mock_phases = [
        {"phase": "Phase 3", "count": 45},
        {"phase": "Phase 2", "count": 38},
        {"phase": "Phase 1", "count": 32},
        {"phase": "Phase 4", "count": 15}
    ]
    
    mock_statuses = [
        {"status": "Recruiting", "count": 52},
        {"status": "Active, not recruiting", "count": 38},
        {"status": "Completed", "count": 25},
        {"status": "Terminated", "count": 5},
        {"status": "Not yet recruiting", "count": 12}
    ]
    
    mock_sponsors = [
        {"sponsor": "National Institutes of Health", "count": 28},
        {"sponsor": "Pfizer Inc.", "count": 18},
        {"sponsor": "Johnson & Johnson", "count": 15},
        {"sponsor": "Roche Pharmaceuticals", "count": 12},
        {"sponsor": "Novartis AG", "count": 10},
        {"sponsor": "Merck & Co.", "count": 8},
        {"sponsor": "AbbVie Inc.", "count": 7}
    ]
    
    stats = {
        "total_trials": 120,
        "phase_distribution": mock_phases,
        "status_distribution": mock_statuses,
        "top_sponsors": mock_sponsors
    }
    
    return stats

# Example usage:
# trials = search_trials("diabetes", phase="Phase 2", top_n=5)
# stats = get_trial_statistics()