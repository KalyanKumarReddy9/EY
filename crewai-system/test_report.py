"""
Test script for report generation
"""
import json
from reports import report_generator

# Test data
test_data = {
    "Clinical Trials": [
        {
            "nct_id": "NCT00000001",
            "title": "A Study of Diabetes Treatment",
            "condition": "Diabetes",
            "phase": "Phase 2",
            "status": "Recruiting",
            "sponsor": "National Institutes of Health"
        },
        {
            "nct_id": "NCT00000002",
            "title": "Another Study of Diabetes Treatment",
            "condition": "Diabetes",
            "phase": "Phase 3",
            "status": "Active, not recruiting",
            "sponsor": "Pfizer Inc."
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

# Test text report generation
print("Testing text report generation...")
try:
    text_summary = report_generator.generate_text_summary("Diabetes Treatment Research", test_data)
    print("Text report generated successfully:")
    print(text_summary[:500] + "..." if len(text_summary) > 500 else text_summary)
except Exception as e:
    print(f"Error generating text report: {e}")

# Test PDF report generation
print("\nTesting PDF report generation...")
try:
    pdf_path = report_generator.generate_pdf_report("Diabetes Treatment Research", test_data)
    print(f"PDF report generated successfully: {pdf_path}")
except Exception as e:
    print(f"Error generating PDF report: {e}")

# Test Excel report generation
print("\nTesting Excel report generation...")
try:
    excel_path = report_generator.generate_excel_report("Diabetes Treatment Research", test_data)
    print(f"Excel report generated successfully: {excel_path}")
except Exception as e:
    print(f"Error generating Excel report: {e}")

print("\nTest completed.")