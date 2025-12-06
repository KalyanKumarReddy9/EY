import requests
import json
from datetime import datetime

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

# Test report generation with storage
def test_report_generation():
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

if __name__ == "__main__":
    test_report_generation()