"""
IQVIA Agent (using mock data since real IQVIA API is not publicly available)
"""
import random
from datetime import datetime

def get_market_stats(therapy_area=None, years=5):
    """
    Get market size and CAGR for a therapy area
    
    Args:
        therapy_area (str): Therapy area to get stats for
        years (int): Number of years for projection
    
    Returns:
        dict: Market statistics
    """
    # Mock therapy areas
    therapy_areas = [
        "Oncology", "Immunology", "Neurology", "Cardiology", 
        "Endocrinology", "Respiratory", "Gastroenterology"
    ]
    
    if not therapy_area:
        therapy_area = random.choice(therapy_areas)
    
    # Generate mock data
    current_value = random.randint(10, 100)  # Billions USD
    growth_rate = round(random.uniform(2.0, 15.0), 1)  # Percentage
    
    # Calculate projected value
    projected_value = current_value * ((1 + growth_rate/100) ** years)
    
    stats = {
        "therapy_area": therapy_area,
        "current_value": f"${current_value} Billion",
        "projected_value": f"${round(projected_value, 1)} Billion",
        "cagr": f"{growth_rate}%",
        "years_projection": years,
        "last_updated": datetime.utcnow().isoformat()
    }
    
    return stats

def get_competitor_analysis(therapy_area=None):
    """
    Get competitor analysis for a therapy area
    
    Args:
        therapy_area (str): Therapy area to analyze
    
    Returns:
        list: List of competitors with market shares
    """
    # Mock competitors
    competitors = [
        {"name": "Pfizer Inc.", "market_share": "18%", "revenue": "$81.3B"},
        {"name": "Johnson & Johnson", "market_share": "15%", "revenue": "$94.9B"},
        {"name": "Roche Holding", "market_share": "12%", "revenue": "$75.1B"},
        {"name": "Novartis AG", "market_share": "10%", "revenue": "$55.9B"},
        {"name": "Merck & Co.", "market_share": "8%", "revenue": "$59.7B"}
    ]
    
    # Add some randomness
    for competitor in competitors:
        market_share_val = float(competitor["market_share"].rstrip('%'))
        revenue_val = float(competitor["revenue"].lstrip('$').rstrip('B'))
        
        # Add some variation
        market_share_val += random.uniform(-2, 2)
        revenue_val += random.uniform(-5, 5)
        
        competitor["market_share"] = f"{max(1, round(market_share_val, 1))}%"
        competitor["revenue"] = f"${max(10, round(revenue_val, 1))}B"
    
    return competitors

def get_therapy_trends(therapy_area=None):
    """
    Get therapy area trends
    
    Args:
        therapy_area (str): Therapy area to analyze
    
    Returns:
        list: List of trends
    """
    # Mock trends
    trend_descriptions = [
        "Increasing prevalence of chronic diseases",
        "Advancements in personalized medicine",
        "Growing geriatric population",
        "Rising healthcare expenditure",
        "Technological innovations in drug delivery",
        "Expansion in emerging markets",
        "Focus on orphan drugs",
        "Increased investment in R&D"
    ]
    
    # Select random trends
    selected_trends = random.sample(trend_descriptions, k=min(5, len(trend_descriptions)))
    
    trends = []
    for i, trend in enumerate(selected_trends):
        trends.append({
            "rank": i + 1,
            "trend": trend,
            "impact_score": random.randint(70, 100)
        })
    
    return trends

# Example usage:
# stats = get_market_stats("Oncology")
# competitors = get_competitor_analysis("Immunology")
# trends = get_therapy_trends("Neurology")