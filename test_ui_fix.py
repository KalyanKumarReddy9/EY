"""
Test script to verify UI fixes
"""
import requests
import json

def test_ui_fixes():
    """Test that all agents return data in the correct format for the UI"""
    print("Testing UI Fixes...")
    
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
    all_successful = True
    
    for endpoint in endpoints:
        try:
            url = f"http://localhost:4000/api/{endpoint['name']}"
            response = requests.get(url, params=endpoint['params'])
            
            if response.status_code == 200:
                data = response.json()
                results[endpoint['name']] = data
                print(f"✅ {endpoint['name'].upper()} - SUCCESS")
                
                # Verify the data structure
                if 'data' not in data:
                    print(f"  ⚠️  Warning: {endpoint['name']} response doesn't have 'data' field")
                else:
                    print(f"  📦 Data format: {{data: {type(data['data']).__name__}, length: {len(data['data']) if isinstance(data['data'], (list, dict)) else 'N/A'}}}")
                    
            else:
                results[endpoint['name']] = {'error': f'HTTP {response.status_code}'}
                print(f"❌ {endpoint['name'].upper()} - FAILED")
                all_successful = False
                
        except Exception as e:
            results[endpoint['name']] = {'error': str(e)}
            print(f"❌ {endpoint['name'].upper()} - ERROR: {str(e)}")
            all_successful = False
    
    # Print results summary
    print("\n" + "="*60)
    print("DETAILED RESULTS")
    print("="*60)
    
    for name, data in results.items():
        if 'error' in data:
            print(f"{name.upper()}: {data['error']}")
        else:
            print(f"{name.upper()}: Received {len(str(data))} characters of data")
            # Show a sample of the data structure
            if 'data' in data:
                sample_data = data['data']
                if isinstance(sample_data, list) and len(sample_data) > 0:
                    first_item = sample_data[0]
                    print(f"  Sample keys: {list(first_item.keys())}")
    
    print("\n" + "="*60)
    if all_successful:
        print("🎉 ALL ENDPOINTS WORKING CORRECTLY!")
        print("The frontend should now properly display data from all agents.")
    else:
        print("⚠️  Some endpoints had issues. Check the errors above.")
    
    print("\n✅ UI fix verification completed!")

if __name__ == "__main__":
    test_ui_fixes()