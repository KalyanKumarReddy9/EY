"""
Test script to verify patent data formatting and report generation
"""
import requests
import json
import os
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:4000"

def test_patent_search():
    """Test patent search endpoint"""
    print("Testing patent search endpoint...")
    
    # Test with a query
    query = "gene therapy"
    params = {
        "query": query,
        "top_n": 5
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/patents", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Patent search successful")
            print(f"  Query: {data.get('query')}")
            print(f"  Source: {data.get('source')}")
            print(f"  Data items: {len(data.get('data', []))}")
            
            # Check if text_summary is present
            if 'text_summary' in data:
                print(f"  ✓ Text summary available ({len(data['text_summary'])} characters)")
                print(f"  Sample text summary:\n{data['text_summary'][:200]}...")
            else:
                print("  ✗ Text summary missing")
                
            return data
        else:
            print(f"✗ Patent search failed with status {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"✗ Patent search error: {str(e)}")
        return None

def test_report_generation(patent_data):
    """Test report generation"""
    print("\nTesting report generation...")
    
    # Prepare test data
    test_results = {
        "Patents": patent_data
    }
    
    # Test text report generation
    report_payload = {
        "query": "Gene therapy research",
        "results": test_results,
        "type": "text"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate-report", json=report_payload)
        if response.status_code == 200:
            data = response.json()
            print("✓ Text report generation successful")
            print(f"  Report ID: {data.get('report_id')}")
            print(f"  Summary length: {len(data.get('summary', ''))} characters")
            return data.get('report_id')
        else:
            print(f"✗ Text report generation failed with status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Text report generation error: {str(e)}")
    
    return None

def test_report_download(report_id):
    """Test report download"""
    if not report_id:
        print("Skipping report download test (no report ID)")
        return
        
    print("\nTesting report download...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/reports/{report_id}/download")
        if response.status_code == 200:
            data = response.json()
            print("✓ Report download successful")
            print(f"  Query: {data.get('query')}")
            print(f"  Summary length: {len(data.get('summary', ''))} characters")
        else:
            print(f"✗ Report download failed with status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ Report download error: {str(e)}")

def main():
    """Main test function"""
    print("=" * 50)
    print("PHARMA MIND NEXUS - PATENT DATA TEST")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print()
    
    # Test patent search
    patent_data = test_patent_search()
    
    if patent_data:
        # Test report generation
        report_id = test_report_generation(patent_data)
        
        # Test report download
        test_report_download(report_id)
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()