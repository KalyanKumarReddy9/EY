"""
Test script for patent agent with mock data
"""
from agents import patent_agent

# Test the patent agent with a gene therapy query
print("Testing patent agent with gene therapy query...")
try:
    # Test search_patents with mock data
    patents = patent_agent.search_patents("gene therapy", top_n=5)
    print(f"Found {len(patents)} patents")
    for i, patent in enumerate(patents):
        print(f"  {i+1}. {patent['title']} (ID: {patent['patent_id']})")
        print(f"     Assignee: {patent['assignee']}")
        print(f"     Filing Date: {patent['filing_date']}")
        print(f"     Grant Date: {patent['grant_date']}")
        print()
    
    # Test get_patent_statistics with mock data
    print("Testing patent statistics...")
    stats = patent_agent.get_patent_statistics()
    print(f"Total patents: {stats['total_patents']}")
    print(f"Recent patents: {stats['recent_patents']}")
    print(f"Expiring patents: {stats['expiring_patents']}")
    print("Top assignees:")
    for assignee in stats['top_assignees']:
        print(f"  {assignee['assignee']}: {assignee['count']}")
        
except Exception as e:
    print(f"Error testing patent agent: {e}")

print("\nTest completed.")