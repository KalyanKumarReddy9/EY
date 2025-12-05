"""
Test script for LLM processor
"""
from llm import llm_processor

# Test data
test_data = {
    "Clinical Trials": [
        {
            "nct_id": "NCT00000001",
            "title": "Study of Diabetes Treatment",
            "condition": "Diabetes",
            "phase": "Phase 2",
            "status": "Recruiting",
            "sponsor": "National Institutes of Health"
        }
    ],
    "Market Insights": {
        "market_size": "$42 Billion",
        "projected_value": "$64.9 Billion",
        "cagr": "9.1%"
    },
    "Patents": [
        {
            "patent_id": "US12345678B2",
            "title": "Methods for Treating Diabetes",
            "assignee": "Johnson & Johnson",
            "filing_date": "2020-01-15",
            "grant_date": "2022-03-22"
        }
    ]
}

# Test LLM synthesis
print("Testing LLM report synthesis...")
try:
    report = llm_processor.synthesize_report_with_llm("Diabetes Treatment Research", test_data)
    print("LLM report generated successfully:")
    print(report[:500] + "..." if len(report) > 500 else report)
except Exception as e:
    print(f"Error generating LLM report: {e}")

# Test visualization data generation
print("\nTesting visualization data generation...")
try:
    viz_data = llm_processor.generate_visualization_data(test_data)
    print("Visualization data generated successfully:")
    print(viz_data)
except Exception as e:
    print(f"Error generating visualization data: {e}")

print("\nTest completed.")