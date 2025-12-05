"""
Database initialization script
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

def create_indexes():
    """Create indexes for better query performance"""
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        
        # Create indexes for trade_wits collection
        db["trade_wits"].create_index([("hs_code", 1)])
        db["trade_wits"].create_index([("year", 1)])
        db["trade_wits"].create_index([("reporter_country", 1)])
        print("Created indexes for trade_wits collection")
        
        # Create indexes for comtrade collection
        db["comtrade"].create_index([("hs_code", 1)])
        db["comtrade"].create_index([("year", 1)])
        db["comtrade"].create_index([("reporter", 1)])
        print("Created indexes for comtrade collection")
        
        # Create indexes for clinical_trials collection
        db["clinical_trials"].create_index([("nct_id", 1)])
        db["clinical_trials"].create_index([("condition", 1)])
        db["clinical_trials"].create_index([("phase", 1)])
        db["clinical_trials"].create_index([("sponsor", 1)])
        print("Created indexes for clinical_trials collection")
        
        # Create indexes for patents collection
        db["patents"].create_index([("patent_id", 1)])
        db["patents"].create_index([("assignee", 1)])
        db["patents"].create_index([("ipc_codes", 1)])
        print("Created indexes for patents collection")
        
        # Create indexes for internal_docs collection
        db["internal_docs"].create_index([("doc_id", 1)])
        db["internal_docs"].create_index([("uploaded_at", 1)])
        db["internal_docs"].create_index([("$**", "text")])  # Text index for search
        print("Created indexes for internal_docs collection")
        
        # Create indexes for embeddings_meta collection
        db["embeddings_meta"].create_index([("doc_id", 1)])
        db["embeddings_meta"].create_index([("mongo_collection", 1)])
        db["embeddings_meta"].create_index([("vector_id", 1)])
        print("Created indexes for embeddings_meta collection")
        
        # Create indexes for users collection
        db["users"].create_index([("email", 1)], unique=True)
        print("Created indexes for users collection")
        
        # Create indexes for reports collection
        db["reports"].create_index([("report_id", 1)])
        db["reports"].create_index([("query", 1)])
        db["reports"].create_index([("generated_at", 1)])
        db["reports"].create_index([("generated_by", 1)])
        print("Created indexes for reports collection")
        
        print("All indexes created successfully")
        
    except Exception as e:
        print(f"Error creating indexes: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def create_text_indexes():
    """Create text indexes for full-text search"""
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        
        # Create text indexes
        db["clinical_trials"].create_index([
            ("title", "text"),
            ("condition", "text"),
            ("sponsor", "text")
        ], name="clinical_trials_text_index")
        print("Created text index for clinical_trials collection")
        
        db["patents"].create_index([
            ("title", "text"),
            ("assignee", "text"),
            ("claims_text", "text")
        ], name="patents_text_index")
        print("Created text index for patents collection")
        
        print("Text indexes created successfully")
        
    except Exception as e:
        print(f"Error creating text indexes: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    print("Initializing Pharma Hub database...")
    create_indexes()
    create_text_indexes()
    print("Database initialization completed!")