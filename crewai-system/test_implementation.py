"""
Test script to verify the Pharma Mind Nexus implementation
"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, '.')

def test_agents():
    """Test all agents"""
    print("Testing Pharma Mind Nexus Implementation")
    print("=" * 50)
    
    # Test EXIM agent
    print("1. Testing EXIM Agent...")
    try:
        from agents.exim_agent import get_trade_by_hs
        result = get_trade_by_hs('3004')
        print(f"   ✓ EXIM agent working, returned {len(result)} items")
    except Exception as e:
        print(f"   ✗ EXIM agent error: {e}")
    
    # Test Trials agent
    print("2. Testing Trials Agent...")
    try:
        from agents.trials_agent import search_trials
        result = search_trials('diabetes')
        print(f"   ✓ Trials agent working, returned {len(result)} items")
    except Exception as e:
        print(f"   ✗ Trials agent error: {e}")
    
    # Test IQVIA agent
    print("3. Testing IQVIA Agent...")
    try:
        from agents.iqvia_agent import get_market_stats
        result = get_market_stats('Oncology')
        print(f"   ✓ IQVIA agent working, returned market stats for {result['therapy_area']}")
    except Exception as e:
        print(f"   ✗ IQVIA agent error: {e}")
    
    # Test Patent agent
    print("4. Testing Patent Agent...")
    try:
        from agents.patent_agent import get_mock_patent_data
        result = get_mock_patent_data('cancer')
        print(f"   ✓ Patent agent working, returned {len(result)} mock patents")
    except Exception as e:
        print(f"   ✗ Patent agent error: {e}")
    
    # Test Web Intel agent
    print("5. Testing Web Intelligence Agent...")
    try:
        from agents.webintel_agent import get_mock_web_results
        result = get_mock_web_results('immunotherapy')
        print(f"   ✓ Web Intel agent working, returned {len(result)} mock results")
    except Exception as e:
        print(f"   ✗ Web Intel agent error: {e}")
    
    # Test Internal Docs agent
    print("6. Testing Internal Documents Agent...")
    try:
        from agents.internal_agent import get_mock_internal_documents
        result = get_mock_internal_documents('clinical trial')
        print(f"   ✓ Internal Docs agent working, returned {len(result)} mock documents")
    except Exception as e:
        print(f"   ✗ Internal Docs agent error: {e}")
    
    # Test Report Generator
    print("7. Testing Report Generator...")
    try:
        from reports.report_generator import generate_text_summary
        mock_data = {"market_insights": {"size": "$50B", "growth": "5%"}}
        result = generate_text_summary("Test Query", mock_data)
        print("   ✓ Report Generator working")
    except Exception as e:
        print(f"   ✗ Report Generator error: {e}")
    
    print("\n" + "=" * 50)
    print("Implementation test completed!")

if __name__ == "__main__":
    test_agents()