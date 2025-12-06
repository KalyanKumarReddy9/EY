"""
Example usage of the Pharma Mind Nexus system
"""
import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:4000"

def demo_exim_agent():
    """Demonstrate EXIM agent usage"""
    print("=== EXIM Agent Demo ===")
    
    # Get trade data for HS code 3004 (pharmaceutical products)
    url = f"{BASE_URL}/api/exim"
    params = {
        "hs_code": "3004",
        "year_from": "2020",
        "top_n": "5"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Results: {json.dumps(data['data'], indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error calling EXIM agent: {str(e)}")

def demo_trials_agent():
    """Demonstrate Clinical Trials agent usage"""
    print("\n=== Clinical Trials Agent Demo ===")
    
    # Search for diabetes-related trials
    url = f"{BASE_URL}/api/trials"
    params = {
        "condition": "diabetes",
        "phase": "Phase 2",
        "top_n": "3"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Results: {json.dumps(data['data'], indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error calling Trials agent: {str(e)}")

def demo_iqvia_agent():
    """Demonstrate IQVIA agent usage"""
    print("\n=== IQVIA Agent Demo ===")
    
    # Get market data for oncology
    url = f"{BASE_URL}/api/iqvia"
    params = {
        "therapy_area": "Oncology"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Market Stats: {json.dumps(data['data']['market_stats'], indent=2)}")
            print(f"Top Competitors: {json.dumps(data['data']['competitors'], indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error calling IQVIA agent: {str(e)}")

def demo_patent_agent():
    """Demonstrate Patent agent usage"""
    print("\n=== Patent Agent Demo ===")
    
    # Search for cancer-related patents
    url = f"{BASE_URL}/api/patents"
    params = {
        "query": "cancer treatment",
        "top_n": "3"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Results: {json.dumps(data['data'], indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error calling Patent agent: {str(e)}")

def demo_web_intel_agent():
    """Demonstrate Web Intelligence agent usage"""
    print("\n=== Web Intelligence Agent Demo ===")
    
    # Search for recent news on immunotherapy
    url = f"{BASE_URL}/api/web-intel"
    params = {
        "query": "immunotherapy breakthrough",
        "num_results": "3"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Results: {json.dumps(data['data'], indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error calling Web Intelligence agent: {str(e)}")

def demo_master_agent():
    """Demonstrate Master agent usage"""
    print("\n=== Master Agent Demo ===")
    
    # Run a complex query through the master agent
    url = f"{BASE_URL}/api/master-agent"
    payload = {
        "query": "What are the market trends for oncology drugs and who are the key players?"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Response: {data['response']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error calling Master agent: {str(e)}")

def demo_report_generation():
    """Demonstrate report generation"""
    print("\n=== Report Generation Demo ===")
    
    # Generate a text summary report
    url = f"{BASE_URL}/api/generate-report"
    payload = {
        "query": "Diabetes treatment market analysis",
        "results": {
            "market_insights": {
                "current_value": "$45 Billion",
                "projected_value": "$75 Billion by 2030",
                "cagr": "5.8%"
            },
            "key_players": [
                {"company": "Novo Nordisk", "market_share": "15%"},
                {"company": "Eli Lilly", "market_share": "12%"},
                {"company": "Sanofi", "market_share": "10%"}
            ]
        },
        "type": "text"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data['query']}")
            print(f"Summary: {data['summary']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    print(f"Pharma Mind Nexus Demo - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Run demos
    demo_exim_agent()
    demo_trials_agent()
    demo_iqvia_agent()
    demo_patent_agent()
    demo_web_intel_agent()
    demo_master_agent()
    demo_report_generation()
    
    print("\nDemo completed!")