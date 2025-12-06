"""
Test script for complete report generation with BigQuery integration
"""
import json
from reports import report_generator

# Test data with patent information
test_data = {
    "Clinical Trials": [
        {
            "nct_id": "NCT00000001",
            "title": "Study of Diabetes Treatment",
            "condition": "Diabetes",
            "phase": "Phase 2",
            "status": "Recruiting",
            "sponsor": "National Institutes of Health"
        },
        {
            "nct_id": "NCT00000002",
            "title": "Cancer Immunotherapy Trial",
            "condition": "Cancer",
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
            "publication_number": "US12345678B2",
            "title": "Methods for Treating Diabetes Using Novel Compounds",
            "assignee": "Johnson & Johnson",
            "priority_date": "2020-01-15",
            "abstract": "This invention relates to novel compounds for treating diabetes...",
            "cpc_codes": "A61K31/125"
        },
        {
            "publication_number": "US87654321A1",
            "title": "Pharmaceutical Composition for Cancer Treatment",
            "assignee": "Pfizer Inc.",
            "priority_date": "2019-03-22",
            "abstract": "A pharmaceutical composition for cancer treatment comprising...",
            "cpc_codes": "A61K31/40"
        }
    ],
    "EXIM Trade Data": [
        {
            "partner": "United States",
            "value": 15000000.00
        },
        {
            "partner": "Germany",
            "value": 8500000.50
        }
    ]
}

# Test PDF report generation
print("Testing PDF report generation...")
try:
    pdf_path = report_generator.generate_pdf_report("Pharmaceutical Research", test_data)
    print(f"PDF report generated successfully: {pdf_path}")
except Exception as e:
    print(f"Error generating PDF report: {e}")

# Test Excel report generation
print("\nTesting Excel report generation...")
try:
    excel_path = report_generator.generate_excel_report("Pharmaceutical Research", test_data)
    print(f"Excel report generated successfully: {excel_path}")
except Exception as e:
    print(f"Error generating Excel report: {e}")

# Test text summary generation
print("\nTesting text summary generation...")
try:
    text_summary = report_generator.generate_text_summary("Pharmaceutical Research", test_data)
    print("Text summary generated successfully:")
    print(text_summary[:500] + "..." if len(text_summary) > 500 else text_summary)
except Exception as e:
    print(f"Error generating text summary: {e}")

print("\nTest completed.")