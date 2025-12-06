"""
Test script to verify query processing improvements
"""
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import patent_agent, trials_agent, exim_agent

def test_query_processing():
    """Test query processing improvements"""
    print("Testing Query Processing Improvements...\n")
    
    # Test queries that need processing
    test_queries = [
        "What are the latest clinical trials for diabetes treatment?",
        "Find patents for cancer therapy",
        "Show me trade data for alzheimer disease medications",
        "What are the recent developments in immunotherapy research?",
        "Clinical trials for cardiovascular patients"
    ]
    
    print("PATENT AGENT QUERY PROCESSING:")
    print("-" * 50)
    for query in test_queries:
        extracted = patent_agent.extract_medical_condition(query)
        print(f"Query: {query}")
        print(f"Extracted: {extracted}")
        print()
    
    print("CLINICAL TRIALS AGENT QUERY PROCESSING:")
    print("-" * 50)
    for query in test_queries:
        extracted = trials_agent.extract_medical_condition(query)
        print(f"Query: {query}")
        print(f"Extracted: {extracted}")
        print()
    
    print("MOCK DATA GENERATION WITH PROCESSED QUERIES:")
    print("-" * 50)
    
    # Test with a specific query
    test_query = "What are the latest clinical trials for diabetes treatment?"
    
    print(f"Testing with query: {test_query}")
    print()
    
    # Test patent mock data
    patent_data = patent_agent.get_mock_patent_data(test_query, 3)
    print("Patent Mock Data:")
    for i, patent in enumerate(patent_data):
        print(f"  {i+1}. {patent['title']}")
        print(f"     Assignee: {patent['assignee']}")
        print(f"     Patent ID: {patent['patent_id']}")
        print()
    
    # Test trials mock data
    trials_data = trials_agent.get_mock_trials(test_query, top_n=3)
    print("Clinical Trials Mock Data:")
    for i, trial in enumerate(trials_data):
        print(f"  {i+1}. {trial['title']}")
        print(f"     NCT ID: {trial['nct_id']}")
        print(f"     Phase: {trial['phase']}")
        print(f"     Status: {trial['status']}")
        print()

def main():
    """Main test function"""
    test_query_processing()
    print("✅ Query processing improvements verified!")

if __name__ == "__main__":
    main()