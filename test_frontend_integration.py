"""
Test script to simulate frontend integration
"""
import requests
import json

def test_frontend_integration():
    """Test the full frontend integration flow"""
    print("Testing Frontend Integration...")
    
    # Test query
    query = "What are the latest clinical trials for diabetes treatment?"
    
    # Define endpoints with their specific parameters
    endpoints = [
        { 
            'name': 'exim', 
            'params': {'hs_code': '3004', 'top_n': 3}
        },
        { 
            'name': 'trials', 
            'params': {'condition': query, 'top_n': 3}
        },
        { 
            'name': 'patents', 
            'params': {'query': query, 'top_n': 3}
        },
        { 
            'name': 'web-intel', 
            'params': {'query': query, 'num_results': 3}
        },
        { 
            'name': 'internal-docs', 
            'params': {'query': query, 'top_n': 3}
        },
        { 
            'name': 'iqvia', 
            'params': {'therapy_area': query}
        }
    ]
    
    # Make requests to all endpoints
    results = {}
    for endpoint in endpoints:
        try:
            url = f"http://localhost:4000/api/{endpoint['name']}"
            response = requests.get(url, params=endpoint['params'])
            
            if response.status_code == 200:
                results[endpoint['name']] = response.json()
                print(f"✅ {endpoint['name'].upper()} - SUCCESS")
            else:
                results[endpoint['name']] = {'error': f'HTTP {response.status_code}'}
                print(f"❌ {endpoint['name'].upper()} - FAILED")
                
        except Exception as e:
            results[endpoint['name']] = {'error': str(e)}
            print(f"❌ {endpoint['name'].upper()} - ERROR: {str(e)}")
    
    # Print results summary
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    
    for name, data in results.items():
        if 'error' in data:
            print(f"{name.upper()}: {data['error']}")
        else:
            print(f"{name.upper()}: Received {len(str(data))} characters of data")
    
    print("\n✅ Frontend integration test completed!")

if __name__ == "__main__":
    test_frontend_integration()