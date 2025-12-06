"""
Script to populate internal documents in the database
"""
import os
import random
from datetime import datetime, timedelta
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

def populate_internal_docs():
    """Populate the database with sample internal documents"""
    client = None
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        collection = db["internal_docs"]
        
        # Sample internal documents
        sample_docs = [
            {
                "doc_id": "mins_2025_q1",
                "title": "Q1 2025 Market Insights Meeting Notes",
                "text": "Discussed emerging trends in diabetes treatment. Key findings: 1) Increased investment in continuous glucose monitoring tech, 2) Growing demand for personalized medicine approaches, 3) Regulatory updates on biosimilar approvals. Action items: Review competitor pipeline analysis and prepare briefing for executive team.",
                "uploaded_by": "Market Intelligence Team",
                "uploaded_at": (datetime.now() - timedelta(days=85)).isoformat()
            },
            {
                "doc_id": "strategy_deck_2025",
                "title": "2025 Strategic Planning Deck - Diabetes Franchise",
                "text": "Comprehensive strategy for diabetes franchise expansion. Market opportunity: $45B global market with 7% CAGR. Competitive landscape: 3 major players control 45% market share. Key initiatives: 1) Launch next-gen insulin delivery system, 2) Expand into emerging markets, 3) Develop companion diagnostics. Budget allocation: R&D 40%, Marketing 35%, Operations 25%.",
                "uploaded_by": "Strategy Planning Group",
                "uploaded_at": (datetime.now() - timedelta(days=120)).isoformat()
            },
            {
                "doc_id": "field_insights_q4_2024",
                "title": "Q4 2024 Field Insights Report",
                "text": "Physician feedback on current diabetes treatments. Key insights: 1) High satisfaction with newer GLP-1 agonists, 2) Concerns about insurance coverage for premium therapies, 3) Demand for simplified dosing regimens. Patient feedback: Preference for once-weekly injections over daily pills. Recommendations: Focus on patient assistance programs and educational materials.",
                "uploaded_by": "Field Research Team",
                "uploaded_at": (datetime.now() - timedelta(days=45)).isoformat()
            },
            {
                "doc_id": "regulatory_update_feb_2025",
                "title": "February 2025 Regulatory Update",
                "text": "FDA guidance on diabetes drug approvals. Recent approvals: 3 new formulations for Type 2 diabetes. Pending submissions: 2 breakthrough therapy designations under review. Compliance reminders: Ensure all promotional materials comply with new advertising standards. Upcoming deadlines: Annual safety reports due March 15th.",
                "uploaded_by": "Regulatory Affairs",
                "uploaded_at": (datetime.now() - timedelta(days=20)).isoformat()
            },
            {
                "doc_id": "competitor_analysis_jan_2025",
                "title": "January 2025 Competitor Analysis - Diabetes Space",
                "text": "Detailed analysis of key competitors in diabetes market. Novo Nordisk: Leading with 35% market share, strong pipeline in oral GLP-1s. Eli Lilly: Rapid growth with 25% market share, aggressive pricing strategy. Sanofi: Stable 20% market share, focusing on combination therapies. Emerging players: Several biotechs developing novel mechanisms of action. Strategic implications: Need to accelerate innovation timeline.",
                "uploaded_by": "Competitive Intelligence",
                "uploaded_at": (datetime.now() - timedelta(days=60)).isoformat()
            },
            {
                "doc_id": "clinical_trial_results_dec_2024",
                "title": "December 2024 Clinical Trial Results Summary",
                "text": "Phase 3 results for investigational diabetes drug XYZ-123. Primary endpoint: Significant reduction in HbA1c vs placebo (p<0.001). Secondary endpoints: 68% of patients achieved target glucose levels vs 32% in control group. Safety profile: Generally well-tolerated with mild GI side effects in 15% of patients. Next steps: Prepare NDA submission package and initiate Phase 4 post-marketing study.",
                "uploaded_by": "Clinical Development Team",
                "uploaded_at": (datetime.now() - timedelta(days=30)).isoformat()
            },
            {
                "doc_id": "financial_forecast_2025",
                "title": "2025 Financial Forecast - Diabetes Division",
                "text": "Revenue projections for diabetes franchise. Expected growth: 9% YoY to $12.5B. Key drivers: New product launches contributing $2.1B, geographic expansion adding $800M. Cost considerations: Increased R&D spend of $1.8B for pipeline advancement. Margin outlook: Maintaining 72% gross margin with operational efficiencies. Investment priorities: Manufacturing capacity and digital health initiatives.",
                "uploaded_by": "Finance Department",
                "uploaded_at": (datetime.now() - timedelta(days=90)).isoformat()
            }
        ]
        
        # Insert documents
        result = collection.insert_many(sample_docs)
        print(f"Inserted {len(result.inserted_ids)} internal documents")
        
        # Create text index for search functionality
        collection.create_index([("title", "text"), ("text", "text")])
        print("Created text index for search functionality")
        
    except Exception as e:
        print(f"Error populating internal docs: {str(e)}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    populate_internal_docs()