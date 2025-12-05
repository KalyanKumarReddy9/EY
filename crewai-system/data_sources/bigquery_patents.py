"""
Google BigQuery integration for fetching patent data
"""
import os
from google.cloud import bigquery
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def get_bigquery_client():
    """
    Create and return a BigQuery client
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable
    pointing to service account JSON key file
    """
    try:
        # Check if service account key file exists
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path or not os.path.exists(credentials_path):
            print("Google Cloud credentials not found. Returning None.")
            return None
            
        # Create BigQuery client
        client = bigquery.Client.from_service_account_json(credentials_path)
        return client
    except Exception as e:
        print(f"Error creating BigQuery client: {str(e)}")
        return None

def search_patents_bigquery(query_term, limit=10):
    """
    Search for patents using Google BigQuery
    
    Args:
        query_term (str): Term to search for in patent titles
        limit (int): Maximum number of results to return
        
    Returns:
        list: List of patent records
    """
    try:
        client = get_bigquery_client()
        if not client:
            return None
            
        # Construct query
        query = f"""
        SELECT
          publication_number,
          title,
          abstract,
          application_number,
          priority_date,
          assignee_harmonized.name AS assignee,
          inventor_harmonized.name AS inventor,
          cpc.code AS cpc_codes,
          citation,
          priority_claim,
          country_code,
          kind_code
        FROM
          `patents-public-data.patents.publications`
        WHERE
          LOWER(title) LIKE '%{query_term.lower()}%'
        LIMIT {limit};
        """
        
        # Execute query
        query_job = client.query(query)
        results = query_job.result()
        
        # Process results
        patents = []
        for row in results:
            patent = {
                "publication_number": row.publication_number,
                "title": row.title,
                "abstract": row.abstract,
                "application_number": row.application_number,
                "priority_date": row.priority_date.isoformat() if row.priority_date else None,
                "assignee": row.assignee,
                "inventor": row.inventor,
                "cpc_codes": row.cpc_codes,
                "citation": row.citation,
                "priority_claim": row.priority_claim,
                "country_code": row.country_code,
                "kind_code": row.kind_code
            }
            patents.append(patent)
            
        return patents
        
    except Exception as e:
        print(f"Error searching patents in BigQuery: {str(e)}")
        return None

def get_patent_statistics_bigquery(query_term):
    """
    Get statistics about patents from BigQuery
    
    Args:
        query_term (str): Term to search for in patent titles
        
    Returns:
        dict: Statistics about patents
    """
    try:
        client = get_bigquery_client()
        if not client:
            return None
            
        # Query for assignee distribution
        assignee_query = f"""
        SELECT
          assignee_harmonized.name AS assignee,
          COUNT(*) as count
        FROM
          `patents-public-data.patents.publications`
        WHERE
          LOWER(title) LIKE '%{query_term.lower()}%'
          AND assignee_harmonized.name IS NOT NULL
        GROUP BY
          assignee_harmonized.name
        ORDER BY
          count DESC
        LIMIT 10;
        """
        
        assignee_job = client.query(assignee_query)
        assignee_results = assignee_job.result()
        
        top_assignees = []
        for row in assignee_results:
            top_assignees.append({
                "assignee": row.assignee,
                "count": row.count
            })
            
        # Query for CPC code distribution
        cpc_query = f"""
        SELECT
          cpc.code AS cpc_code,
          COUNT(*) as count
        FROM
          `patents-public-data.patents.publications`,
          UNNEST(cpc) AS cpc
        WHERE
          LOWER(title) LIKE '%{query_term.lower()}%'
          AND cpc.code IS NOT NULL
        GROUP BY
          cpc.code
        ORDER BY
          count DESC
        LIMIT 10;
        """
        
        cpc_job = client.query(cpc_query)
        cpc_results = cpc_job.result()
        
        top_cpc_codes = []
        for row in cpc_results:
            top_cpc_codes.append({
                "cpc_code": row.cpc_code,
                "count": row.count
            })
            
        stats = {
            "top_assignees": top_assignees,
            "top_cpc_codes": top_cpc_codes
        }
        
        return stats
        
    except Exception as e:
        print(f"Error getting patent statistics from BigQuery: {str(e)}")
        return None

# Example usage:
# patents = search_patents_bigquery("pharmaceutical", limit=5)
# stats = get_patent_statistics_bigquery("pharmaceutical")