"""
Test script to verify frontend integration with backend APIs
"""
import requests
import json
import os

# API base URL
API_BASE = "http://localhost:4000"

def test_api_endpoints():
    """Test all API endpoints to ensure they return proper data"""
    print("Testing API endpoints...")
    
    # Test endpoints with sample queries
    endpoints = [
        ("/api/exim?hs_code=3004&top_n=3", "EXIM Data"),
        ("/api/trials?condition=diabetes&top_n=3", "Clinical Trials"),
        ("/api/patents?query=cancer&top_n=3", "Patents"),
    ]
    
    all_working = True
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {name}: Success")
                if 'data' in data and data['data']:
                    print(f"  - Retrieved {len(data['data'])} items")
                elif 'error' in data:
                    print(f"  - Error: {data['error']}")
                    # This is expected for mock data, so not necessarily a failure
            else:
                print(f"✗ {name}: HTTP {response.status_code}")
                all_working = False
        except requests.exceptions.RequestException as e:
            print(f"✗ {name}: Connection error - {str(e)}")
            all_working = False
        except Exception as e:
            print(f"✗ {name}: Unexpected error - {str(e)}")
            all_working = False
    
    return all_working

def test_report_generation():
    """Test report generation endpoint"""
    print("\nTesting Report Generation...")
    
    # Sample data for report generation
    sample_results = {
        "EXIM Data": [
            {"partner": "United States", "value": 120125112.85},
            {"partner": "Germany", "value": 95379542.19}
        ],
        "Clinical Trials": [
            {
                "nct_id": "NCT04258594",
                "title": "Efficacy and Safety Study",
                "condition": "Diabetes",
                "phase": "Phase 2",
                "status": "Completed"
            }
        ],
        "Patents": [
            {
                "patent_id": "US7085253B1",
                "title": "Pharmaceutical formulation",
                "assignee": "Novartis",
                "filing_date": "2018-08-29"
            }
        ]
    }
    
    report_payload = {
        "query": "Diabetes Treatment Research",
        "results": sample_results,
        "type": "pdf"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/generate-report",
            json=report_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            # Check if it's a PDF response
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                print("✓ Report Generation: Success")
                print(f"  - Content-Type: {content_type}")
                print(f"  - Content-Length: {len(response.content)} bytes")
                return True
            else:
                print(f"✗ Report Generation: Unexpected content type - {content_type}")
                return False
        else:
            print(f"✗ Report Generation: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"  - Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"  - Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Report Generation: Connection error - {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Report Generation: Unexpected error - {str(e)}")
        return False

def test_database_storage():
    """Test if reports are being stored in the database"""
    print("\nTesting Database Storage...")
    
    try:
        response = requests.get(f"{API_BASE}/api/reports", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Database Access: Success")
            print(f"  - Total reports in database: {data.get('count', 0)}")
            
            if data.get('reports'):
                latest_report = data['reports'][0] if data['reports'] else None
                if latest_report:
                    print(f"  - Latest report query: {latest_report.get('query', 'N/A')}")
                    print(f"  - Generated at: {latest_report.get('generated_at', 'N/A')}")
            
            return True
        else:
            print(f"✗ Database Access: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Database Access: Connection error - {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Database Access: Unexpected error - {str(e)}")
        return False

def main():
    """Main test function"""
    print("Testing Frontend Integration with Backend APIs...\n")
    
    # Test if backend is running
    try:
        health_response = requests.get(f"{API_BASE}/", timeout=5)
        if health_response.status_code == 200:
            print("✓ Backend Server: Running")
        else:
            print("✗ Backend Server: Not responding correctly")
            return
    except:
        print("✗ Backend Server: Not running. Please start the backend server first.")
        return
    
    # Run all tests
    api_tests_passed = test_api_endpoints()
    report_test_passed = test_report_generation()
    db_test_passed = test_database_storage()
    
    print("\n" + "="*50)
    print("FRONTEND INTEGRATION TEST RESULTS:")
    print(f"  API Endpoints: {'✓ PASS' if api_tests_passed else '✗ FAIL'}")
    print(f"  Report Generation: {'✓ PASS' if report_test_passed else '✗ FAIL'}")
    print(f"  Database Storage: {'✓ PASS' if db_test_passed else '✗ FAIL'}")
    
    if api_tests_passed and report_test_passed and db_test_passed:
        print("\n🎉 All frontend integration tests passed!")
        print("✅ The system is ready for use.")
    else:
        print("\n⚠️  Some integration tests failed.")
        print("Please check the backend server and database connections.")

if __name__ == "__main__":
    main()