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

def test_mongo_connection():
    try:
        client = get_mongo_client()
        print("Connected to MongoDB successfully")
        
        # Test database and collection
        db = client["pharma_hub"]
        reports_collection = db["reports"]
        
        # Insert a test document
        test_doc = {
            "report_id": str(uuid.uuid4()),
            "query": "Test query",
            "report_type": "pdf",
            "generated_at": datetime.now().isoformat(),
            "test_field": "test_value"
        }
        
        result = reports_collection.insert_one(test_doc)
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Retrieve the document
        retrieved_doc = reports_collection.find_one({"_id": result.inserted_id})
        print(f"Retrieved document: {retrieved_doc}")
        
        client.close()
        print("MongoDB test completed successfully")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mongo_connection()