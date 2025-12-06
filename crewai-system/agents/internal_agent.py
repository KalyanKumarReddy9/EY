"""
Internal Documents Agent for processing internal knowledge
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

def search_internal_documents(query, top_n=5, database_name="pharma_hub"):
    """
    Search internal documents by query
    
    Args:
        query (str): Search query
        top_n (int): Number of results to return
        database_name (str): Name of the MongoDB database
    
    Returns:
        list: List of documents
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Build text search query
        mongo_query = {"$text": {"$search": query}}
        
        # Find documents
        documents = list(db["internal_docs"].find(mongo_query).limit(top_n))
        
        # Format results
        formatted_docs = []
        for doc in documents:
            formatted_doc = {
                "doc_id": doc.get("doc_id"),
                "title": doc.get("title"),
                "text_excerpt": doc.get("text")[:200] + "..." if len(doc.get("text", "")) > 200 else doc.get("text"),
                "uploaded_by": doc.get("uploaded_by"),
                "uploaded_at": doc.get("uploaded_at")
            }
            formatted_docs.append(formatted_doc)
        
        return formatted_docs
        
    except Exception as e:
        print(f"Error in Internal Documents agent: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def get_document_by_id(doc_id, database_name="pharma_hub"):
    """
    Get a specific document by ID
    
    Args:
        doc_id (str): Document ID
        database_name (str): Name of the MongoDB database
    
    Returns:
        dict: Document data
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Find document
        document = db["internal_docs"].find_one({"doc_id": doc_id})
        
        if document:
            return {
                "doc_id": document.get("doc_id"),
                "title": document.get("title"),
                "text": document.get("text"),
                "uploaded_by": document.get("uploaded_by"),
                "uploaded_at": document.get("uploaded_at")
            }
        else:
            return None
        
    except Exception as e:
        print(f"Error retrieving document: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def upload_document(title, text, uploaded_by, database_name="pharma_hub"):
    """
    Upload a new document to the internal documents collection
    
    Args:
        title (str): Document title
        text (str): Document content
        uploaded_by (str): User who uploaded the document
        database_name (str): Name of the MongoDB database
    
    Returns:
        str: Document ID of the uploaded document
    """
    try:
        client = get_mongo_client()
        db = client[database_name]
        
        # Create document
        doc_id = f"doc_{random.randint(100000, 999999)}"
        document = {
            "doc_id": doc_id,
            "title": title,
            "text": text,
            "uploaded_by": uploaded_by,
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
        # Insert document
        db["internal_docs"].insert_one(document)
        print(f"Uploaded document with ID: {doc_id}")
        
        return doc_id
        
    except Exception as e:
        print(f"Error uploading document: {str(e)}")
        raise
    finally:
        if 'client' in locals():
            client.close()

def get_mock_internal_documents(query, count=3):
    """
    Generate mock internal documents for testing
    
    Args:
        query (str): Query term to include in mock data
        count (int): Number of mock documents to generate
    
    Returns:
        list: List of mock documents
    """
    mock_docs = []
    
    for i in range(count):
        mock_doc = {
            "doc_id": f"mock_doc_{i+1}",
            "title": f"Internal Report on {query} - Version {i+1}",
            "text_excerpt": f"This internal document discusses the latest findings on {query}. Key findings include improved efficacy rates and reduced side effects...",
            "uploaded_by": f"Researcher {random.choice(['Alice', 'Bob', 'Charlie', 'Diana'])}",
            "uploaded_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
        }
        mock_docs.append(mock_doc)
    
    return mock_docs

# Example usage:
# docs = search_internal_documents("clinical trial results", top_n=3)
# doc = get_document_by_id("doc_123456")
# doc_id = upload_document("New Research Findings", "This document contains...", "Dr. Smith")