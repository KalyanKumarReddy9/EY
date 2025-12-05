"""
Main application file for Pharma Mind Nexus
"""
import os
from dotenv import load_dotenv
from api.server import app
from init_db import create_indexes, create_text_indexes

# Load environment variables
load_dotenv()

def initialize_system():
    """Initialize the entire system"""
    try:
        print("Initializing Pharma Mind Nexus system...")
        
        # Initialize database
        print("Setting up database indexes...")
        create_indexes()
        create_text_indexes()
        
        print("System initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during system initialization: {str(e)}")
        raise

def start_server():
    """Start the Flask server"""
    try:
        PORT = int(os.environ.get("PORT", 4000))
        print(f"Starting Pharma Mind Nexus server on port {PORT}...")
        app.run(host='0.0.0.0', port=PORT, debug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        raise

if __name__ == "__main__":
    # Initialize system
    initialize_system()
    
    # Start server
    start_server()