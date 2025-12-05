"""
Test script to verify report generation
"""
import requests
import json

def test_report_generation():
    """Test report generation functionality"""
    print("Testing Report Generation...")
    
    # Sample data that would come from the agents
    sample_results = {
        "EXIM": {
            "data": [
                {"partner": "China", "value": 79987368.28, "product_description": "Medicaments"},
                {"partner": "Germany", "value": 65234112.75, "product_description": "Medicaments"}
            ]
        },
        "Trials": {
            "data": [
                {
                    "title": "A Phase 2 Study of Novel Treatment for Diabetes",
                    "nct_id": "NCT12345678",
                    "condition": "Diabetes",
                    "phase": "Phase 2",
                    "status": "Recruiting",
                    "sponsor": "National Institutes of Health"
                }
            ]
        },
        "Patents": {
            "data": [
                {
                    "title": "Method for treating diabetes using novel compounds",
                    "patent_id": "US1234567B2",
                    "assignee": "PharmaCorp",
                    "filing_date": "2020-01-15",
                    "grant_date": "2022-03-22",
                    "ipc_codes": ["A61K31/00", "A61K31/125"]
                }
            ]
        },
        "IQVIA": {
            "data": {
                "market_stats": {
                    "therapy_area": "Diabetes",
                    "current_value": "$40 Billion",
                    "projected_value": "$57.2 Billion",
                    "cagr": "7.4%"
                },
                "competitors": [
                    {"name": "Pfizer Inc.", "market_share": "17.2%", "revenue": "$76.6B"},
                    {"name": "Johnson & Johnson", "market_share": "14.3%", "revenue": "$93.4B"}
                ]
            }
        }
    }
    
    # Prepare the request payload
    payload = {
        "query": "What are the latest clinical trials for diabetes treatment?",
        "results": sample_results,
        "type": "text"  # Request text report
    }
    
    try:
        # Make the request to generate a report
        response = requests.post(
            "http://localhost:4000/api/generate-report",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Report generation SUCCESS")
            print(f"Generated summary: {result.get('summary', 'No summary found')[:200]}...")
            print("\n✅ Report generation test completed successfully!")
            return True
        else:
            print(f"❌ Report generation FAILED with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Report generation ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_report_generation()