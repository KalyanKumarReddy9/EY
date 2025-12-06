import requests
import json
from datetime import datetime
from pymongo import MongoClient
import os

# Test data
test_results = {
    "exim_data": [
        {"country": "USA", "value": 1000000, "year": 2023},
        {"country": "Germany", "value": 750000, "year": 2023}
    ],
    "clinical_trials": [
        {"title": "Phase III Trial for New Diabetes Drug", "status": "Recruiting", "phase": "Phase 3"},
        {"title": "Safety Study of Gene Therapy", "status": "Active", "phase": "Phase 1"}
    ],
    "patent_data": [
        {"patent_id": "US12345678B2", "title": "Novel Pharmaceutical Compound", "assignee": "Big Pharma Inc."},
        {"patent_id": "EP8765432A1", "title": "Drug Delivery System", "assignee": "Medical Devices Ltd."}
    ]
}

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(MONGO_URI)

def count_reports_before():
    """Count reports before generating a new one"""
    client = get_mongo_client()
    db = client["pharma_hub"]
    reports_collection = db["reports"]
    count = reports_collection.count_documents({})
    client.close()
    return count

def count_reports_after():
    """Count reports after generating a new one"""
    client = get_mongo_client()
    db = client["pharma_hub"]
    reports_collection = db["reports"]
    count = reports_collection.count_documents({})
    client.close()
    return count

def find_latest_report():
    """Find the latest report in the database"""
    client = get_mongo_client()
    db = client["pharma_hub"]
    reports_collection = db["reports"]
    # Sort by _id descending to get the most recent
    report = reports_collection.find_one(sort=[("_id", -1)])
    client.close()
    return report

# Test report generation with storage
def test_report_generation():
    # Count reports before
    before_count = count_reports_before()
    print(f"Reports before generation: {before_count}")
    
    url = "http://localhost:4000/api/generate-report"
    
    payload = {
        "query": "Comprehensive analysis of diabetes treatments market",
        "results": test_results,
        "type": "pdf",
        "user_id": "test_user_123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Testing report generation and storage...")
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            print("Report generated and downloaded successfully!")
            print(f"Response headers: {response.headers}")
            
            # Save the PDF to verify it was generated
            with open("test_report.pdf", "wb") as f:
                f.write(response.content)
            print("PDF saved as test_report.pdf")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
    
    # Count reports after
    after_count = count_reports_after()
    print(f"Reports after generation: {after_count}")
    
    # Find the latest report
    latest_report = find_latest_report()
    print(f"Latest report in database: {latest_report}")

if __name__ == "__main__":
    test_report_generation()