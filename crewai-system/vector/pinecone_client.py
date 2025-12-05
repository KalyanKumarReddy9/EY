"""
Pinecone client for vector operations
"""
import os
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PineconeClient:
    """Pinecone client for vector database operations"""
    
    def __init__(self):
        """Initialize Pinecone client"""
        self.api_key = os.environ.get("PINECONE_API_KEY")
        self.environment = os.environ.get("PINECONE_ENV")
        self.index_name = "pharma-docs"
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        
        # Initialize Pinecone
        pinecone.init(api_key=self.api_key, environment=self.environment)
        
        # Create index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            print(f"Creating Pinecone index: {self.index_name}")
            pinecone.create_index(self.index_name, dimension=384, metric="cosine")
        
        self.index = pinecone.Index(self.index_name)
    
    def upsert_vectors(self, vectors):
        """
        Upsert vectors to Pinecone
        
        Args:
            vectors (list): List of tuples (id, vector, metadata)
        
        Returns:
            dict: Upsert response
        """
        try:
            print(f"Upserting {len(vectors)} vectors to Pinecone")
            response = self.index.upsert(vectors)
            print("Successfully upserted vectors to Pinecone")
            return response
        except Exception as e:
            print(f"Error upserting vectors: {str(e)}")
            raise
    
    def query_vectors(self, vector, top_k=5, include_metadata=True):
        """
        Query vectors from Pinecone
        
        Args:
            vector (list): Query vector
            top_k (int): Number of results to return
            include_metadata (bool): Whether to include metadata
        
        Returns:
            dict: Query response
        """
        try:
            print(f"Querying Pinecone with vector of dimension {len(vector)}")
            response = self.index.query(
                vector=vector,
                top_k=top_k,
                include_metadata=include_metadata
            )
            return response
        except Exception as e:
            print(f"Error querying vectors: {str(e)}")
            raise
    
    def delete_vectors(self, ids):
        """
        Delete vectors from Pinecone
        
        Args:
            ids (list): List of vector IDs to delete
        
        Returns:
            dict: Delete response
        """
        try:
            print(f"Deleting {len(ids)} vectors from Pinecone")
            response = self.index.delete(ids=ids)
            print("Successfully deleted vectors from Pinecone")
            return response
        except Exception as e:
            print(f"Error deleting vectors: {str(e)}")
            raise
    
    def get_stats(self):
        """
        Get index statistics
        
        Returns:
            dict: Index statistics
        """
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            print(f"Error getting index stats: {str(e)}")
            raise

# Example usage:
# client = PineconeClient()
# vectors = [("id1", [0.1, 0.2, 0.3], {"text": "sample"})]
# client.upsert_vectors(vectors)