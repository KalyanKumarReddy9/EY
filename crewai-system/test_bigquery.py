"""
Test script for BigQuery patent data integration
"""
from data_sources import bigquery_patents

# Test BigQuery patent search
print("Testing BigQuery patent search...")
try:
    # This will only work if you have Google Cloud credentials configured
    patents = bigquery_patents.search_patents_bigquery("pharmaceutical", limit=5)
    if patents:
        print(f"Found {len(patents)} patents:")
        for i, patent in enumerate(patents):
            print(f"  {i+1}. {patent['publication_number']}: {patent['title']}")
            print(f"     Assignee: {patent['assignee']}")
            print(f"     Priority Date: {patent['priority_date']}")
            print()
    else:
        print("BigQuery integration not configured or no data found.")
except Exception as e:
    print(f"Error testing BigQuery patent search: {e}")

# Test BigQuery patent statistics
print("\nTesting BigQuery patent statistics...")
try:
    # This will only work if you have Google Cloud credentials configured
    stats = bigquery_patents.get_patent_statistics_bigquery("pharmaceutical")
    if stats:
        print("Patent statistics retrieved successfully:")
        if "top_assignees" in stats:
            print("Top assignees:")
            for assignee in stats["top_assignees"][:5]:
                print(f"  {assignee['assignee']}: {assignee['count']} patents")
        if "top_cpc_codes" in stats:
            print("Top CPC codes:")
            for cpc in stats["top_cpc_codes"][:5]:
                print(f"  {cpc['cpc_code']}: {cpc['count']} patents")
    else:
        print("BigQuery integration not configured or no data found.")
except Exception as e:
    print(f"Error testing BigQuery patent statistics: {e}")

print("\nTest completed.")