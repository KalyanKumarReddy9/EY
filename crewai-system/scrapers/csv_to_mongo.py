"""
Generic CSV-to-Mongo loader
"""
import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

def load_csv_to_mongo(csv_path, collection_name, database_name="pharma_hub", transform_fn=None):
    """
    Load CSV data into MongoDB collection
    
    Args:
        csv_path (str): Path to the CSV file
        collection_name (str): Name of the MongoDB collection
        database_name (str): Name of the MongoDB database
        transform_fn (callable): Optional function to transform each record
    
    Returns:
        int: Number of records inserted
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        records = df.to_dict(orient="records")
        
        # Apply transformation function if provided
        if transform_fn:
            records = [transform_fn(r) for r in records]
        
        # Add timestamp to each record
        for record in records:
            record["last_updated"] = datetime.utcnow().isoformat()
        
        # Connect to MongoDB
        client = get_mongo_client()
        db = client[database_name]
        collection = db[collection_name]
        
        # Insert records
        if records:
            result = collection.insert_many(records)
            print(f"Inserted {len(result.inserted_ids)} records into {collection_name}")
            return len(result.inserted_ids)
        else:
            print(f"No records to insert into {collection_name}")
            return 0
            
    except Exception as e:
        print(f"Error loading CSV to MongoDB: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def update_record(collection_name, database_name="pharma_hub", query={}, update_data={}):
    """
    Update records in MongoDB collection
    
    Args:
        collection_name (str): Name of the MongoDB collection
        database_name (str): Name of the MongoDB database
        query (dict): Query to find records to update
        update_data (dict): Data to update the records with
    
    Returns:
        int: Number of records modified
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        collection = db[collection_name]
        
        # Add timestamp to update data
        update_data["last_updated"] = datetime.utcnow().isoformat()
        
        result = collection.update_many(query, {"$set": update_data})
        print(f"Updated {result.modified_count} records in {collection_name}")
        return result.modified_count
        
    except Exception as e:
        print(f"Error updating records: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def delete_records(collection_name, database_name="pharma_hub", query={}):
    """
    Delete records from MongoDB collection
    
    Args:
        collection_name (str): Name of the MongoDB collection
        database_name (str): Name of the MongoDB database
        query (dict): Query to find records to delete
    
    Returns:
        int: Number of records deleted
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        collection = db[collection_name]
        
        result = collection.delete_many(query)
        print(f"Deleted {result.deleted_count} records from {collection_name}")
        return result.deleted_count
        
    except Exception as e:
        print(f"Error deleting records: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

# Example usage:
# load_csv_to_mongo("data/wits_3004_2018_2023.csv", "trade_wits")