from mock_scraper import MockPriceScraper
from analytics import PriceAnalytics

def run_demo():
    """Run a comprehensive demo with mock data"""
    print("🚀 Price Intelligence Platform Demo")
    print("=" * 50)
    
    # Generate mock data
    print("1. Generating realistic sample data...")
    scraper = MockPriceScraper()
    products_count = scraper.run_full_scrape()
    
    # Analyze data
    print("\n2. Analyzing generated data...")
    analytics = PriceAnalytics()
    
    # Display results
    print(f"\n📊 Analysis Results:")
    print("=" * 30)
    
    stats = analytics.get_summary_stats()
    if stats:
        print(f"✅ Total Products: {stats['total_products']}")
        print(f"📈 Price Points: {stats['total_price_points']}")
        print(f"🏷️  Categories: {stats['categories_tracked']}")
        print(f"🏪 Sites: {stats['sites_tracked']}")
        print(f"💰 Average Price: ₹{stats['avg_price']}")
        print(f"📊 Price Range: {stats['price_range']}")
        print(f"💸 Cheapest Category: {stats['cheapest_category']}")
        print(f"💎 Most Expensive: {stats['most_expensive_category']}")
    
    # Show price alerts
    print(f"\n🚨 Price Alerts:")
    print("=" * 20)
    
    alerts = analytics.get_price_alerts(threshold_percent=10)
    if alerts:
        for alert in alerts[:3]:  # Show top 3 alerts
            print(f"⚠️  {alert['category'].title()}: {alert['difference_percent']}% cheaper on {alert['cheaper_site']}")
            print(f"   💰 Save ₹{alert['potential_savings']} (₹{alert['max_price']} → ₹{alert['min_price']})")
    else:
        print("No significant price differences found.")
    
    print(f"\n✅ Demo complete! Run 'streamlit run dashboard.py' to see the interactive dashboard")
    print("🌐 Dashboard features:")
    print("   • Real-time price comparison")
    print("   • Interactive charts and graphs") 
    print("   • Price trend analysis")
    print("   • Smart price alerts")
    print("   • Category-wise insights")

if __name__ == "__main__":
    run_demo()