import os
from pymongo import MongoClient
from bson.binary import Binary
import uuid
from datetime import datetime

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    print(f"Connecting to MongoDB at: {MONGO_URI}")
    return MongoClient(MONGO_URI)

def test_direct_insert():
    """Test direct insertion into MongoDB"""
    try:
        client = get_mongo_client()
        print("Connected to MongoDB successfully")
        
        # Test database and collection
        db = client["pharma_hub"]
        reports_collection = db["reports"]
        
        # Insert a test document
        test_doc = {
            "report_id": str(uuid.uuid4()),
            "query": "Direct test query",
            "report_type": "pdf",
            "generated_at": datetime.now().isoformat(),
            "test_field": "direct_insert_test"
        }
        
        print(f"Inserting document: {test_doc}")
        result = reports_collection.insert_one(test_doc)
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Retrieve the document immediately
        retrieved_doc = reports_collection.find_one({"_id": result.inserted_id})
        print(f"Retrieved document immediately: {retrieved_doc}")
        
        # Count total documents
        count = reports_collection.count_documents({})
        print(f"Total documents in collection: {count}")
        
        # List all documents
        all_docs = list(reports_collection.find({}))
        print(f"All documents: {all_docs}")
        
        client.close()
        print("MongoDB test completed successfully")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_insert()