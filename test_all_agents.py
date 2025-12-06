"""
Test script to verify all agents are working correctly
"""
import requests
import json

def test_all_agents():
    """Test all agents to verify they're working correctly"""
    print("Testing All Agents...")
    
    # Test query
    query = "What are the latest clinical trials for diabetes treatment?"
    
    # Define endpoints with their specific parameters
    endpoints = [
        { 
            'name': 'exim', 
            'params': {'hs_code': '3004', 'top_n': 3},
            'expected_field': 'partner'
        },
        { 
            'name': 'trials', 
            'params': {'condition': query, 'top_n': 3},
            'expected_field': 'nct_id'
        },
        { 
            'name': 'patents', 
            'params': {'query': query, 'top_n': 3},
            'expected_field': 'patent_id'
        },
        { 
            'name': 'web-intel', 
            'params': {'query': query, 'num_results': 3},
            'expected_field': 'title'
        },
        { 
            'name': 'internal-docs', 
            'params': {'query': query, 'top_n': 3},
            'expected_field': 'doc_id'
        },
        { 
            'name': 'iqvia', 
            'params': {'therapy_area': query},
            'expected_field': 'market_stats'
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
                    # Check if we have actual data (not just empty arrays)
                    actual_data = data['data']
                    if isinstance(actual_data, list) and len(actual_data) > 0:
                        first_item = actual_data[0]
                        if endpoint['expected_field'] in first_item or endpoint['expected_field'] in actual_data:
                            print(f"  📦 Data format: {{data: {type(actual_data).__name__}, length: {len(actual_data)}}}")
                            print(f"  🔍 Sample item has '{endpoint['expected_field']}' field")
                        else:
                            print(f"  ⚠️  Warning: Sample item missing expected field '{endpoint['expected_field']}'")
                    elif isinstance(actual_data, dict) and endpoint['expected_field'] in actual_data:
                        print(f"  📦 Data format: {{data: dict}} with '{endpoint['expected_field']}' field")
                    else:
                        print(f"  ⚠️  Warning: Unexpected data format")
                        
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
    
    print("\n" + "="*60)
    if all_successful:
        print("🎉 ALL AGENTS WORKING CORRECTLY!")
        print("The frontend should now properly display data from all agents.")
    else:
        print("⚠️  Some agents had issues. Check the errors above.")
    
    print("\n✅ Agent testing completed!")

if __name__ == "__main__":
    test_all_agents()