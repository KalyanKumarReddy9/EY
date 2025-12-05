"""
ClinicalTrials.gov loader
"""
import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import json

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

def fetch_clinical_trials(query, max_trials=100):
    """
    Fetch clinical trials data from ClinicalTrials.gov API
    
    Args:
        query (str): Search query for clinical trials
        max_trials (int): Maximum number of trials to fetch
    
    Returns:
        list: List of clinical trial records
    """
    try:
        # ClinicalTrials.gov API endpoint
        base_url = "https://clinicaltrials.gov/api/v2/studies"
        
        # Parameters for the API request
        params = {
            "query.term": query,
            "pageSize": min(max_trials, 100),  # API limit is 100 per request
            "fields": "protocolSection.identificationModule,protocolSection.statusModule,protocolSection.sponsorCollaboratorsModule,protocolSection.conditionsModule,protocolSection.designModule"
        }
        
        print(f"Fetching clinical trials for query: {query}")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        studies = data.get("studies", [])
        
        # Transform studies to our schema
        records = []
        for study in studies:
            protocol_section = study.get("protocolSection", {})
            identification_module = protocol_section.get("identificationModule", {})
            status_module = protocol_section.get("statusModule", {})
            sponsor_module = protocol_section.get("sponsorCollaboratorsModule", {})
            conditions_module = protocol_section.get("conditionsModule", {})
            design_module = protocol_section.get("designModule", {})
            
            record = {
                "nct_id": identification_module.get("nctId"),
                "title": identification_module.get("briefTitle"),
                "condition": conditions_module.get("conditions", [""])[0] if conditions_module.get("conditions") else "",
                "phase": ", ".join(design_module.get("phases", [])) if design_module.get("phases") else "Not Available",
                "status": status_module.get("overallStatus"),
                "sponsor": sponsor_module.get("leadSponsor", {}).get("name"),
                "locations": [],  # Would need additional API calls to get detailed location data
                "raw_json": study,  # Store the original JSON for reference
                "last_updated": datetime.utcnow().isoformat()
            }
            records.append(record)
        
        print(f"Fetched {len(records)} clinical trials")
        return records
        
    except Exception as e:
        print(f"Error fetching clinical trials: {str(e)}")
        raise

def load_clinical_trials_to_mongo(query, database_name="pharma_hub", max_trials=100):
    """
    Fetch and load clinical trials data into MongoDB
    
    Args:
        query (str): Search query for clinical trials
        database_name (str): Name of the MongoDB database
        max_trials (int): Maximum number of trials to fetch
    """
    try:
        # Fetch clinical trials data
        records = fetch_clinical_trials(query, max_trials)
        
        if not records:
            print("No clinical trials found for the query")
            return
        
        # Connect to MongoDB and insert records
        client = get_mongo_client()
        db = client[database_name]
        collection = db["clinical_trials"]
        
        # Insert records
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} clinical trials into MongoDB")
        
    except Exception as e:
        print(f"Error loading clinical trials to MongoDB: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def update_clinical_trial(nct_id, update_data, database_name="pharma_hub"):
    """
    Update a specific clinical trial record
    
    Args:
        nct_id (str): NCT ID of the trial to update
        update_data (dict): Data to update
        database_name (str): Name of the MongoDB database
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        collection = db["clinical_trials"]
        
        # Add timestamp to update data
        update_data["last_updated"] = datetime.utcnow().isoformat()
        
        result = collection.update_one({"nct_id": nct_id}, {"$set": update_data})
        if result.matched_count > 0:
            print(f"Updated clinical trial {nct_id}")
        else:
            print(f"Clinical trial {nct_id} not found")
            
    except Exception as e:
        print(f"Error updating clinical trial: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

# Example usage:
# load_clinical_trials_to_mongo("diabetes", max_trials=50)