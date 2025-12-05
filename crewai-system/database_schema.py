"""
MongoDB Schema Definitions for Pharma Hub
"""

# Database: pharma_hub
DATABASE_NAME = "pharma_hub"

# Collections with their schemas
COLLECTIONS = {
    "trade_wits": {
        "hs_code": str,
        "year": int,
        "reporter_country": str,
        "partner_country": str,
        "value": float,
        "quantity": float,
        "source_file": str,
        "last_updated": str  # ISO format datetime
    },
    
    "comtrade": {
        "hs_code": str,
        "year": int,
        "reporter": str,
        "partner": str,
        "value": float,
        "unit": str,
        "last_updated": str  # ISO format datetime
    },
    
    "clinical_trials": {
        "nct_id": str,
        "title": str,
        "condition": str,
        "phase": str,
        "status": str,
        "sponsor": str,
        "locations": list,  # Array of strings
        "raw_json": dict,   # Original JSON data
        "last_updated": str  # ISO format datetime
    },
    
    "patents": {
        "patent_id": str,
        "title": str,
        "assignee": str,
        "filing_date": str,  # ISO format date
        "grant_date": str,   # ISO format date
        "ipc_codes": list,   # Array of strings
        "claims_text": str,
        "expiry_date": str,  # ISO format date
        "raw_json": dict,    # Original JSON data
        "last_updated": str  # ISO format datetime
    },
    
    "internal_docs": {
        "doc_id": str,
        "title": str,
        "text": str,
        "uploaded_by": str,
        "uploaded_at": str  # ISO format datetime
    },
    
    "embeddings_meta": {
        "doc_id": str,
        "mongo_collection": str,
        "ref_id": str,
        "vector_id": str,
        "text_excerpt": str,
        "created_at": str  # ISO format datetime
    },
    
    "users": {
        "name": str,
        "email": str,
        "password": str,  # hashed
        "role": str,
        "created_at": str  # ISO format datetime
    },
    
    "reports": {
        "report_id": str,
        "query": str,
        "report_type": str,  # pdf, excel, text
        "file_path": str,
        "file_data": bytes,  # Binary data for the report
        "generated_at": str,  # ISO format datetime
        "generated_by": str,  # User ID if available
        "metadata": dict      # Additional metadata
    }
}

# Recommended indexes for performance
INDEXES = {
    "trade_wits": ["hs_code", "year", "reporter_country"],
    "comtrade": ["hs_code", "year", "reporter"],
    "clinical_trials": ["nct_id", "condition", "phase", "sponsor"],
    "patents": ["patent_id", "assignee", "ipc_codes"],
    "internal_docs": ["doc_id", "uploaded_at"],
    "embeddings_meta": ["doc_id", "mongo_collection", "vector_id"],
    "users": ["email"],
    "reports": ["report_id", "query", "generated_at", "generated_by"]
}