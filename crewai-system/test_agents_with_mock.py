"""
Test script to verify that all agents work properly with mock data
"""
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import exim_agent, trials_agent, patent_agent

def test_exim_agent():
    """Test EXIM agent with mock data"""
    print("Testing EXIM Agent...")
    try:
        # Test trade partners data
        trade_data = exim_agent.get_mock_trade_data("3004", 5)
        print(f"EXIM Trade Data: {len(trade_data)} entries")
        for entry in trade_data[:2]:  # Show first 2 entries
            print(f"  - {entry['partner']}: ${entry['value']:,.2f}")
        
        # Test trade trends data
        trends_data = exim_agent.get_mock_trade_trends("3004")
        print(f"EXIM Trends Data: {len(trends_data)} years")
        for entry in trends_data:
            print(f"  - {entry['year']}: ${entry['value']:,.2f}")
        
        print("✓ EXIM Agent working correctly\n")
        return True
    except Exception as e:
        print(f"✗ EXIM Agent error: {str(e)}\n")
        return False

def test_trials_agent():
    """Test Clinical Trials agent with mock data"""
    print("Testing Clinical Trials Agent...")
    try:
        # Test trials search
        trials_data = trials_agent.get_mock_trials("diabetes", top_n=5)
        print(f"Clinical Trials Data: {len(trials_data)} trials")
        for trial in trials_data[:2]:  # Show first 2 trials
            print(f"  - {trial['nct_id']}: {trial['title'][:50]}...")
            print(f"    Phase: {trial['phase']}, Status: {trial['status']}")
        
        # Test statistics
        stats_data = trials_agent.get_mock_trial_statistics()
        print(f"Trial Statistics: {stats_data['total_trials']} total trials")
        print(f"  Phases: {[p['phase'] for p in stats_data['phase_distribution'][:3]]}")
        
        print("✓ Clinical Trials Agent working correctly\n")
        return True
    except Exception as e:
        print(f"✗ Clinical Trials Agent error: {str(e)}\n")
        return False

def test_patent_agent():
    """Test Patent agent with mock data"""
    print("Testing Patent Agent...")
    try:
        # Test patent search
        patent_data = patent_agent.get_mock_patent_data("cancer", 5)
        print(f"Patent Data: {len(patent_data)} patents")
        for patent in patent_data[:2]:  # Show first 2 patents
            print(f"  - {patent['patent_id']}: {patent['title'][:50]}...")
            print(f"    Assignee: {patent['assignee']}, Filed: {patent['filing_date']}")
        
        # Test statistics
        stats_data = patent_agent.get_mock_patent_statistics()
        print(f"Patent Statistics: {stats_data['total_patents']} total patents")
        print(f"  Top Assignees: {[a['assignee'] for a in stats_data['top_assignees'][:3]]}")
        
        print("✓ Patent Agent working correctly\n")
        return True
    except Exception as e:
        print(f"✗ Patent Agent error: {str(e)}\n")
        return False

def main():
    """Main test function"""
    print("Testing all agents with mock data...\n")
    
    results = []
    results.append(test_exim_agent())
    results.append(test_trials_agent())
    results.append(test_patent_agent())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} agents working correctly")
    
    if passed == total:
        print("🎉 All agents are working properly with mock data!")
        return True
    else:
        print("⚠️  Some agents need attention")
        return False

if __name__ == "__main__":
    main()