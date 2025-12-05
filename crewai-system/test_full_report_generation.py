"""
Test script to verify full report generation with mock data
"""
import os
import sys
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reports import report_generator

def create_sample_data():
    """Create sample data for testing report generation"""
    return {
        "EXIM Data": [
            {"partner": "United States", "value": 120125112.85, "product_description": "Medicaments"},
            {"partner": "Germany", "value": 95379542.19, "product_description": "Medicaments"},
            {"partner": "China", "value": 75379542.19, "product_description": "Medicaments"}
        ],
        "Clinical Trials": [
            {
                "nct_id": "NCT04258594",
                "title": "Efficacy and Safety of Investigational Drug in Diabetes Patients",
                "condition": "Diabetes",
                "phase": "Phase 2",
                "status": "Terminated",
                "sponsor": "Pfizer Inc."
            },
            {
                "nct_id": "NCT01365045",
                "title": "Randomized Controlled Trial: Diabetes Treatment Outcomes",
                "condition": "Diabetes",
                "phase": "Phase 3",
                "status": "Completed",
                "sponsor": "Johnson & Johnson"
            }
        ],
        "Patents": [
            {
                "patent_id": "US7085253B1",
                "title": "Pharmaceutical formulation for diabetes therapy",
                "assignee": "Novartis",
                "filing_date": "2018-08-29",
                "grant_date": "2020-03-15",
                "expiry_date": "2038-08-29",
                "ipc_codes": ["A61K31/00", "A61K31/125"]
            },
            {
                "patent_id": "US4593267A1",
                "title": "Method for treating diabetes using novel compounds",
                "assignee": "Merck & Co.",
                "filing_date": "2023-05-07",
                "grant_date": "2024-01-20",
                "expiry_date": "2043-05-07",
                "ipc_codes": ["A61K31/195", "A61K31/40"]
            }
        ],
        "Web Intel": [
            {
                "title": "Latest Advances in Diabetes Treatment",
                "link": "https://example.com/diabetes-advances",
                "snippet": "New breakthrough therapies for diabetes management show promising results in clinical trials.",
                "source": "Medical Journal"
            }
        ]
    }

def test_text_report():
    """Test text report generation"""
    print("Testing Text Report Generation...")
    try:
        sample_data = create_sample_data()
        summary = report_generator.generate_text_summary("Diabetes Treatment Research", sample_data)
        
        print("✓ Text report generated successfully")
        print(f"Summary length: {len(summary)} characters")
        print(f"Preview: {summary[:200]}...")
        print()
        return True
    except Exception as e:
        print(f"✗ Text report generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False

def test_pdf_report():
    """Test PDF report generation"""
    print("Testing PDF Report Generation...")
    try:
        sample_data = create_sample_data()
        pdf_path = report_generator.generate_pdf_report("Diabetes Treatment Research", sample_data, "test_report.pdf")
        
        print("✓ PDF report generated successfully")
        print(f"PDF saved to: {pdf_path}")
        
        # Check if file exists and has content
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"PDF file size: {file_size} bytes")
            if file_size > 0:
                print("✓ PDF file has content")
                return True
            else:
                print("✗ PDF file is empty")
                return False
        else:
            print("✗ PDF file was not created")
            return False
    except Exception as e:
        print(f"✗ PDF report generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False

def test_excel_report():
    """Test Excel report generation"""
    print("Testing Excel Report Generation...")
    try:
        sample_data = create_sample_data()
        excel_path = report_generator.generate_excel_report("Diabetes Treatment Research", sample_data, "test_report.xlsx")
        
        print("✓ Excel report generated successfully")
        print(f"Excel saved to: {excel_path}")
        
        # Check if file exists and has content
        if os.path.exists(excel_path):
            file_size = os.path.getsize(excel_path)
            print(f"Excel file size: {file_size} bytes")
            if file_size > 0:
                print("✓ Excel file has content")
                return True
            else:
                print("✗ Excel file is empty")
                return False
        else:
            print("✗ Excel file was not created")
            return False
    except Exception as e:
        print(f"✗ Excel report generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print()
        return False

def main():
    """Main test function"""
    print("Testing full report generation pipeline...\n")
    
    results = []
    results.append(test_text_report())
    results.append(test_pdf_report())
    results.append(test_excel_report())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"Report Generation Test Results: {passed}/{total} formats working correctly")
    
    if passed == total:
        print("🎉 All report formats are working properly!")
        print("✅ Text reports: Working")
        print("✅ PDF reports: Working")
        print("✅ Excel reports: Working")
        return True
    else:
        print("⚠️  Some report formats need attention")
        return False

if __name__ == "__main__":
    main()