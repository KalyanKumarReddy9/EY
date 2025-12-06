"""
Test script to verify all API integrations are working correctly
"""
import os
from dotenv import load_dotenv
from agents import patent_agent, trials_agent, webintel_agent
from data_sources import pubmed_patents, openalex_papers, clinicaltrials_api

# Load environment variables
load_dotenv()

def test_all_apis():
    """Test all API integrations"""
    print("Testing all API integrations...\n")
    
    # Test 1: PubMed API
    print("1. Testing PubMed API...")
    try:
        pubmed_results = pubmed_patents.search_patents_pubmed("diabetes treatment", 2)
        print(f"   ✓ PubMed API working - Found {len(pubmed_results)} results")
        if pubmed_results:
            print(f"   ✓ First result: {pubmed_results[0].get('title', '')[:50]}...")
    except Exception as e:
        print(f"   ✗ PubMed API error: {str(e)}")
    
    # Test 2: OpenAlex API
    print("\n2. Testing OpenAlex API...")
    try:
        openalex_results = openalex_papers.search_papers_openalex("diabetes treatment", 2)
        print(f"   ✓ OpenAlex API working - Found {len(openalex_results)} results")
        if openalex_results:
            print(f"   ✓ First result: {openalex_results[0].get('title', '')[:50]}...")
    except Exception as e:
        print(f"   ✗ OpenAlex API error: {str(e)}")
    
    # Test 3: ClinicalTrials.gov API
    print("\n3. Testing ClinicalTrials.gov API...")
    try:
        ct_results = clinicaltrials_api.search_clinical_trials("diabetes", max_results=2)
        print(f"   ✓ ClinicalTrials.gov API working - Found {len(ct_results)} results")
        if ct_results:
            print(f"   ✓ First result: {ct_results[0].get('title', '')[:50]}...")
    except Exception as e:
        print(f"   ✗ ClinicalTrials.gov API error: {str(e)}")
    
    # Test 4: Patent Agent (uses PubMed + OpenAlex)
    print("\n4. Testing Patent Agent...")
    try:
        patent_results = patent_agent.search_patents("diabetes treatment", top_n=2)
        # Patent agent returns a dict with "data" key
        if isinstance(patent_results, dict):
            source = patent_results.get("source", "Unknown")
            data = patent_results.get("data", [])
            print(f"   ✓ Patent Agent working - Source: {source}, Found {len(data)} results")
            if data:
                print(f"   ✓ First result: {data[0].get('title', '')[:50]}...")
        else:
            # Handle case where it returns a list directly
            data = patent_results if isinstance(patent_results, list) else []
            print(f"   ✓ Patent Agent working - Found {len(data)} results")
            if data:
                print(f"   ✓ First result: {data[0].get('title', '')[:50]}...")
    except Exception as e:
        print(f"   ✗ Patent Agent error: {str(e)}")
    
    # Test 5: Clinical Trials Agent (uses ClinicalTrials.gov API)
    print("\n5. Testing Clinical Trials Agent...")
    try:
        trials_results = trials_agent.search_trials("diabetes", top_n=2)
        # Clinical trials agent returns a dict with "data" key
        if isinstance(trials_results, dict):
            source = trials_results.get("source", "Unknown")
            data = trials_results.get("data", [])
            print(f"   ✓ Clinical Trials Agent working - Source: {source}, Found {len(data)} results")
            if data:
                title = data[0].get('brief_title', data[0].get('title', '')) if isinstance(data[0], dict) else "Unknown"
                print(f"   ✓ First result: {title[:50]}...")
        elif isinstance(trials_results, list):
            # Handle case where it returns a list directly
            data = trials_results
            print(f"   ✓ Clinical Trials Agent working - Found {len(data)} results")
            if data:
                title = data[0].get('brief_title', data[0].get('title', '')) if isinstance(data[0], dict) else "Unknown"
                print(f"   ✓ First result: {title[:50]}...")
        else:
            print(f"   ✗ Unexpected return type from Clinical Trials Agent: {type(trials_results)}")
    except Exception as e:
        print(f"   ✗ Clinical Trials Agent error: {str(e)}")
    
    # Test 6: Web Intel Agent
    print("\n6. Testing Web Intel Agent...")
    try:
        web_results = webintel_agent.search_web("diabetes treatment", num_results=2)
        # Web intel agent returns a list directly
        if isinstance(web_results, list):
            data = web_results
            print(f"   ✓ Web Intel Agent working - Found {len(data)} results")
            if data:
                title = data[0].get('title', '') if isinstance(data[0], dict) else "Unknown"
                print(f"   ✓ First result: {title[:50]}...")
        elif isinstance(web_results, dict):
            # Handle case where it returns a dict
            data = web_results.get("data", [])
            print(f"   ✓ Web Intel Agent working - Found {len(data)} results")
            if data:
                title = data[0].get('title', '') if isinstance(data[0], dict) else "Unknown"
                print(f"   ✓ First result: {title[:50]}...")
        else:
            print(f"   ✗ Unexpected return type from Web Intel Agent: {type(web_results)}")
    except Exception as e:
        print(f"   ✗ Web Intel Agent error: {str(e)}")
    
    # Test 7: API Keys Verification
    print("\n7. Verifying API Keys...")
    api_keys = {
        "PINECONE_API_KEY": os.environ.get("PINECONE_API_KEY"),
        "HF_TOKEN": os.environ.get("HF_TOKEN"),
        "PUBMED_API_KEY": os.environ.get("PUBMED_API_KEY"),
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY"),
        "SUDO_DEV_API_KEY": os.environ.get("SUDO_DEV_API_KEY"),
        "OPENFDA_API_KEY": os.environ.get("OPENFDA_API_KEY")
    }
    
    for key_name, key_value in api_keys.items():
        if key_value:
            print(f"   ✓ {key_name}: Configured ({key_value[:10]}...)")
        else:
            print(f"   ✗ {key_name}: Not found")
    
    print("\n" + "="*50)
    print("API Integration Test Complete!")
    print("="*50)

if __name__ == "__main__":
    test_all_apis()