"""
Comtrade downloader & loader
"""
import requests
import io
import pandas as pd
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

def download_comtrade_csv(url, save_path=None):
    """
    Download CSV data from Comtrade API
    
    Args:
        url (str): URL to download data from
        save_path (str): Optional path to save the downloaded file
    
    Returns:
        io.BytesIO: BytesIO object containing the CSV data
    """
    try:
        print(f"Downloading data from: {url}")
        r = requests.get(url)
        r.raise_for_status()
        
        if save_path:
            with open(save_path, "wb") as f:
                f.write(r.content)
            print(f"Saved data to: {save_path}")
        
        return io.BytesIO(r.content)
    except Exception as e:
        print(f"Error downloading Comtrade CSV: {str(e)}")
        raise

def download_and_load_comtrade(cmdCode="3004", reporter="356", database_name="pharma_hub"):
    """
    Download and load Comtrade data into MongoDB
    
    Args:
        cmdCode (str): HS code for the product
        reporter (str): Reporter country code
        database_name (str): Name of the MongoDB database
    """
    try:
        # Construct URL for Comtrade API
        url = f"https://comtradeapi.un.org/public/v1/preview?reporterCode={reporter}&cmdCode={cmdCode}"
        print(f"Fetching data from Comtrade API: {url}")
        
        # Get data from API
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        
        # Transform data to records
        records = []
        for r in data.get("dataset", []):
            record = {
                "hs_code": r.get("cmdCode"),
                "year": r.get("yr"),
                "reporter": r.get("rtTitle"),
                "partner": r.get("ptTitle"),
                "value": r.get("TradeValue"),
                "quantity": r.get("TradeQuantity"),
                "unit": r.get("TradeQuantityUnit"),
                "source": "comtrade_api_preview",
                "last_updated": datetime.utcnow().isoformat()
            }
            records.append(record)
        
        if not records:
            print("No records found in Comtrade data")
            return
        
        # Connect to MongoDB and insert records
        client = get_mongo_client()
        db = client[database_name]
        collection = db["comtrade"]
        
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} records into comtrade collection")
        
    except Exception as e:
        print(f"Error downloading and loading Comtrade data: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def load_comtrade_csv_to_mongo(csv_path, database_name="pharma_hub"):
    """
    Load Comtrade CSV data into MongoDB
    
    Args:
        csv_path (str): Path to the CSV file
        database_name (str): Name of the MongoDB database
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Transform data to match our schema
        records = []
        for _, row in df.iterrows():
            record = {
                "hs_code": str(row.get("cmdCode", row.get("HS_CODE", ""))),
                "year": int(row.get("yr", row.get("YEAR", 0))),
                "reporter": str(row.get("rtTitle", row.get("REPORTER", ""))),
                "partner": str(row.get("ptTitle", row.get("PARTNER", ""))),
                "value": float(row.get("TradeValue", row.get("VALUE", 0))),
                "quantity": float(row.get("TradeQuantity", row.get("QUANTITY", 0))),
                "unit": str(row.get("TradeQuantityUnit", row.get("UNIT", ""))),
                "source": "comtrade_csv",
                "last_updated": datetime.utcnow().isoformat()
            }
            records.append(record)
        
        if not records:
            print("No records found in CSV file")
            return
        
        # Connect to MongoDB and insert records
        client = get_mongo_client()
        db = client[database_name]
        collection = db["comtrade"]
        
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} records into comtrade collection from CSV")
        
    except Exception as e:
        print(f"Error loading Comtrade CSV to MongoDB: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

# Example usage:
# download_and_load_comtrade("3004", "356")
# load_comtrade_csv_to_mongo("data/comtrade_sample.csv")