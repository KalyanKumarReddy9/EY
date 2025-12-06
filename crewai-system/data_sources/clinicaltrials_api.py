"""
ClinicalTrials.gov API integration
"""
import requests
import json
from urllib.parse import urlencode
import time
import random

# Base URL for ClinicalTrials.gov API
BASE_URL = "https://clinicaltrials.gov/api/v2"

def search_studies(query, max_results=10):
    """
    Search for clinical studies using the ClinicalTrials.gov API
    
    Args:
        query (str): Search query (condition, intervention, etc.)
        max_results (int): Maximum number of results to return
        
    Returns:
        dict: API response with studies data
    """
    try:
        # Endpoint for searching studies
        url = f"{BASE_URL}/studies"
        
        # Parameters for the search
        params = {
            "query.term": query,
            "pageSize": min(max_results, 100),  # API limit is 100 per page
            "sort": "LastUpdatePostDate"  # Sort by last update date
        }
        
        # Make the request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to ClinicalTrials.gov API: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response from ClinicalTrials.gov API: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in ClinicalTrials.gov API search: {str(e)}")
        raise

def get_study_details(nct_id):
    """
    Get detailed information for a specific study by NCT ID
    
    Args:
        nct_id (str): NCT ID of the study
        
    Returns:
        dict: Study details
    """
    try:
        # Endpoint for getting a single study
        url = f"{BASE_URL}/studies/{nct_id}"
        
        # Make the request
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to ClinicalTrials.gov API: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response from ClinicalTrials.gov API: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in ClinicalTrials.gov API study details: {str(e)}")
        raise

def get_search_areas():
    """
    Get available search areas from ClinicalTrials.gov API
    
    Returns:
        dict: Search areas data
    """
    try:
        url = f"{BASE_URL}/studies/search-areas"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error getting search areas: {str(e)}")
        raise

def get_enums():
    """
    Get available enums from ClinicalTrials.gov API
    
    Returns:
        dict: Enums data
    """
    try:
        url = f"{BASE_URL}/studies/enums"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error getting enums: {str(e)}")
        raise

def get_study_statistics():
    """
    Get study statistics from ClinicalTrials.gov API
    
    Returns:
        dict: Statistics data
    """
    try:
        url = f"{BASE_URL}/stats/size"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error getting study statistics: {str(e)}")
        raise

def format_study_for_display(study_data):
    """
    Format study data for display in the agent response
    
    Args:
        study_data (dict): Raw study data from API
        
    Returns:
        dict: Formatted study data
    """
    try:
        # Extract protocol section which contains most of the study information
        protocol_section = study_data.get("protocolSection", {})
        
        # Extract identification module
        identification_module = protocol_section.get("identificationModule", {})
        
        # Extract status module
        status_module = protocol_section.get("statusModule", {})
        
        # Extract description module
        description_module = protocol_section.get("descriptionModule", {})
        
        # Extract sponsor collaborators module
        sponsor_collaborators_module = protocol_section.get("sponsorCollaboratorsModule", {})
        
        # Extract design module
        design_module = protocol_section.get("designModule", {})
        
        # Format the study data
        formatted_study = {
            "nct_id": identification_module.get("nctId", ""),
            "title": identification_module.get("briefTitle", identification_module.get("officialTitle", "")),
            "brief_title": identification_module.get("briefTitle", ""),
            "official_title": identification_module.get("officialTitle", ""),
            "condition": ", ".join(description_module.get("conditions", [])),
            "phase": ", ".join(design_module.get("phases", [])),
            "study_type": design_module.get("studyType", ""),
            "status": status_module.get("overallStatus", ""),
            "sponsor": sponsor_collaborators_module.get("leadSponsor", {}).get("name", ""),
            "last_update": status_module.get("lastUpdateSubmitDate", ""),
            "start_date": status_module.get("startDateStruct", {}).get("date", ""),
            "completion_date": status_module.get("completionDateStruct", {}).get("date", ""),
            "enrollment": design_module.get("enrollmentInfo", {}).get("count", ""),
            "brief_summary": description_module.get("briefSummary", ""),
            "detailed_description": description_module.get("detailedDescription", "")
        }
        
        return formatted_study
        
    except Exception as e:
        print(f"Error formatting study data: {str(e)}")
        # Return a basic structure if formatting fails
        return {
            "nct_id": study_data.get("nctId", ""),
            "title": study_data.get("title", "Unknown Title"),
            "condition": "Unknown Condition",
            "phase": "Unknown Phase",
            "status": "Unknown Status",
            "sponsor": "Unknown Sponsor"
        }

def search_clinical_trials(query, max_results=10):
    """
    Search for clinical trials and format results for the agent
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        list: Formatted list of clinical trials
    """
    try:
        # Search for studies
        search_results = search_studies(query, max_results)
        
        # Extract studies from the response
        studies = search_results.get("studies", [])
        
        # Format each study for display
        formatted_studies = []
        for study in studies:
            # Get detailed information for each study
            try:
                nct_id = study.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
                if nct_id:
                    # Get detailed study information
                    detailed_study = get_study_details(nct_id)
                    formatted_study = format_study_for_display(detailed_study)
                    formatted_studies.append(formatted_study)
                else:
                    # If we can't get NCT ID, format the basic study data
                    basic_data = format_study_for_display(study)
                    formatted_studies.append(basic_data)
            except Exception as e:
                print(f"Error getting details for study: {str(e)}")
                # Continue with basic study data
                basic_data = format_study_for_display(study)
                formatted_studies.append(basic_data)
            
            # Add a small delay to respect API rate limits
            time.sleep(0.1)
        
        return formatted_studies
        
    except Exception as e:
        print(f"Error in clinical trials search: {str(e)}")
        raise

# Example usage:
# studies = search_clinical_trials("diabetes", max_results=5)
# for study in studies:
#     print(f"NCT ID: {study['nct_id']}")
#     print(f"Title: {study['title']}")
#     print(f"Condition: {study['condition']}")
#     print(f"Phase: {study['phase']}")
#     print(f"Status: {study['status']}")
#     print(f"Sponsor: {study['sponsor']}")
#     print("-" * 50)