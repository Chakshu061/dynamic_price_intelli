import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from analytics import PriceAnalytics
from mock_scraper import MockPriceScraper

# Page config
st.set_page_config(
    page_title="Price Intelligence Dashboard",
    page_icon="💰",
    layout="wide"
)

# Initialize
@st.cache_data
def load_analytics():
    return PriceAnalytics()

def main():
    st.title("💰 Dynamic Pricing Intelligence Platform")
    st.markdown("*Real-time price monitoring and competitive analysis*")
    
    analytics = load_analytics()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Price Analysis", "Trends", "Alerts", "Data Collection"])
    
    if page == "Dashboard":
        show_dashboard(analytics)
    elif page == "Price Analysis":
        show_price_analysis(analytics)
    elif page == "Trends":
        show_trends(analytics)
    elif page == "Alerts":
        show_alerts(analytics)
    elif page == "Data Collection":
        show_data_collection()

def show_dashboard(analytics):
    """Main dashboard view"""
    st.header("📊 Dashboard Overview")
    
    # Get summary stats
    stats = analytics.get_summary_stats()
    
    if not stats:
        st.warning("No data available. Please run data collection first.")
        if st.button("🚀 Generate Sample Data", type="primary"):
            with st.spinner("Generating sample data..."):
                scraper = MockPriceScraper()
                scraper.run_full_scrape()
            st.success("✅ Sample data generated!")
            st.rerun()
        return
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", stats['total_products'])
    
    with col2:
        st.metric("Price Points", stats['total_price_points'])
    
    with col3:
        st.metric("Categories", stats['categories_tracked'])
    
    with col4:
        st.metric("Average Price", f"₹{stats['avg_price']}")
    
    # Additional metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Price Range", stats['price_range'])
    
    with col2:
        st.metric("Cheapest Category", stats['cheapest_category'].title())
    
    with col3:
        st.metric("Most Expensive", stats['most_expensive_category'].title())
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Category Price Analysis")
        category_data = analytics.get_category_analysis()
        
        if not category_data.empty:
            fig = px.bar(
                category_data, 
                x='category', 
                y='Avg_Price',
                title="Average Price by Category",
                color='Avg_Price',
                color_continuous_scale='viridis'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    with col2:
        st.subheader("🏪 Site Comparison")
        price_df = analytics.get_price_history_df()
        
        if not price_df.empty:
            # Get latest prices only
            latest_prices = price_df.loc[price_df.groupby(['product_name', 'site'])['scraped_at'].idxmax()]
            site_avg = latest_prices.groupby('site')['price'].mean().reset_index()
            
            fig = px.pie(
                site_avg, 
                values='price', 
                names='site',
                title="Average Price Distribution by Site"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No site data available")
    
    # Site comparison chart
    st.subheader("💰 Price Comparison Across Sites")
    site_comparison = analytics.get_site_comparison()
    
    if not site_comparison.empty:
        fig = px.bar(
            site_comparison.reset_index(), 
            x='category', 
            y=['Amazon', 'Flipkart'],
            title="Average Prices: Amazon vs Flipkart",
            barmode='group'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent data table
    st.subheader("📋 Recent Products")
    products_df = analytics.get_products_df()
    
    if not products_df.empty:
        # Show top products from each category
        display_df = products_df.groupby('category').head(2)
        display_df = display_df[['name', 'site', 'price', 'category', 'rating']].round(2)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No product data available")

def show_price_analysis(analytics):
    """Price analysis view"""
    st.header("📊 Detailed Price Analysis")
    
    price_df = analytics.get_price_history_df()
    
    if price_df.empty:
        st.warning("No price data available")
        return
    
    # Category selection
    categories = price_df['category'].unique()
    selected_category = st.selectbox("Select Category for Analysis", categories)
    
    # Filter data - get latest prices only
    latest_prices = price_df.loc[price_df.groupby(['product_name', 'site'])['scraped_at'].idxmax()]
    filtered_data = latest_prices[latest_prices['category'] == selected_category]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📈 {selected_category.title()} Price Distribution")
        
        fig = px.box(
            filtered_data, 
            x='site', 
            y='price',
            title=f"{selected_category.title()} Prices by Site",
            color='site'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"📊 {selected_category.title()} Statistics")
        
        stats = filtered_data['price'].describe()
        st.write("**Price Statistics:**")
        st.write(f"- Count: {stats['count']:.0f}")
        st.write(f"- Mean: ₹{stats['mean']:.2f}")
        st.write(f"- Min: ₹{stats['min']:.2f}")
        st.write(f"- Max: ₹{stats['max']:.2f}")
        st.write(f"- Std Dev: ₹{stats['std']:.2f}")
        
        # Site comparison for this category
        amazon_avg = filtered_data[filtered_data['site'] == 'Amazon']['price'].mean()
        flipkart_avg = filtered_data[filtered_data['site'] == 'Flipkart']['price'].mean()
        
        st.write("**Site Comparison:**")
        st.write(f"- Amazon Avg: ₹{amazon_avg:.2f}")
        st.write(f"- Flipkart Avg: ₹{flipkart_avg:.2f}")
        
        if amazon_avg > flipkart_avg:
            savings = amazon_avg - flipkart_avg
            st.write(f"- 💰 Save ₹{savings:.2f} on Flipkart")
        else:
            savings = flipkart_avg - amazon_avg
            st.write(f"- 💰 Save ₹{savings:.2f} on Amazon")
    
    # Detailed table
    st.subheader(f"📋 {selected_category.title()} Products")
    display_cols = ['name', 'site', 'price', 'rating', 'reviews_count']
    if all(col in filtered_data.columns for col in display_cols):
        st.dataframe(filtered_data[display_cols].round(2), use_container_width=True)
    else:
        st.dataframe(filtered_data, use_container_width=True)

def show_trends(analytics):
    """Price trends view"""
    st.header("📈 Price Trends Analysis")
    
    price_df = analytics.get_price_history_df()
    
    if price_df.empty:
        st.warning("No price data available")
        return
    
    # Category selection for trends
    categories = price_df['category'].unique()
    selected_category = st.selectbox("Select Category for Trend Analysis", categories)
    
    # Get trend data
    trends = analytics.get_price_trends(selected_category)
    
    if not trends.empty:
        st.subheader(f"📊 {selected_category.title()} Price Trends Over Time")
        
        fig = px.line(
            trends, 
            x='date', 
            y='price', 
            color='site',
            title=f"{selected_category.title()} Price Trends",
            markers=True
        )
        fig.update_layout(xaxis_title="Date", yaxis_title="Price (₹)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Trend Insights")
            
            amazon_trend = trends[trends['site'] == 'Amazon']['price']
            flipkart_trend = trends[trends['site'] == 'Flipkart']['price']
            
            if len(amazon_trend) > 1:
                amazon_change = ((amazon_trend.iloc[-1] - amazon_trend.iloc[0]) / amazon_trend.iloc[0]) * 100
                st.write(f"**Amazon:** {amazon_change:.1f}% change")
            
            if len(flipkart_trend) > 1:
                flipkart_change = ((flipkart_trend.iloc[-1] - flipkart_trend.iloc[0]) / flipkart_trend.iloc[0]) * 100
                st.write(f"**Flipkart:** {flipkart_change:.1f}% change")
        
        with col2:
            st.subheader("💡 Recommendations")
            
            current_amazon = amazon_trend.iloc[-1] if len(amazon_trend) > 0 else 0
            current_flipkart = flipkart_trend.iloc[-1] if len(flipkart_trend) > 0 else 0
            
            if current_amazon < current_flipkart:
                st.write("🛒 **Buy from Amazon** - Currently cheaper")
                st.write(f"💰 Save ₹{current_flipkart - current_amazon:.2f}")
            else:
                st.write("🛒 **Buy from Flipkart** - Currently cheaper")
                st.write(f"💰 Save ₹{current_amazon - current_flipkart:.2f}")
    else:
        st.info("No trend data available for this category")

def show_alerts(analytics):
    """Price alerts view"""
    st.header("🚨 Smart Price Alerts")
    
    threshold = st.slider("Price Difference Threshold (%)", 5, 30, 15)
    alerts = analytics.get_price_alerts(threshold)
    
    if not alerts:
        st.info(f"No significant price differences found above {threshold}% threshold.")
        return
    
    st.subheader(f"⚠️ Categories with >{threshold}% Price Difference")
    
    for i, alert in enumerate(alerts):
        with st.expander(f"💡 {alert['category'].title()} - {alert['difference_percent']}% difference", expanded=(i<3)):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Cheaper Site", alert['cheaper_site'])
            
            with col2:
                st.metric("Lower Price", f"₹{alert['min_price']:.2f}")
            
            with col3:
                st.metric("Higher Price", f"₹{alert['max_price']:.2f}")
            
            with col4:
                st.metric("Potential Savings", f"₹{alert['potential_savings']:.2f}")
            
            # Action buttons
            st.write("**💡 Recommendation:** Shop for " + alert['category'] + " on " + alert['cheaper_site'] + " to save money!")

def show_data_collection():
    """Data collection interface"""
    st.header("🔄 Data Management")
    
    st.write("Generate fresh sample data for the price intelligence system:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Generate New Data", type="primary"):
            with st.spinner("Generating comprehensive sample data... This may take a moment."):
                scraper = MockPriceScraper()
                products_count = scraper.run_full_scrape()
            
            st.success(f"✅ Successfully generated {products_count} products with historical data!")
            st.balloons()
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.checkbox("I understand this will delete all data"):
                import os
                if os.path.exists('price_data.json'):
                    os.remove('price_data.json')
                st.success("✅ All data cleared!")
                st.rerun()
    
    # Show current data status
    analytics = PriceAnalytics()
    stats = analytics.get_summary_stats()
    
    if stats:
        st.subheader("📈 Current Data Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Total Products:** {stats['total_products']}")
            st.write(f"**Categories:** {stats['categories_tracked']}")
        
        with col2:
            st.write(f"**Price Points:** {stats['total_price_points']}")
            st.write(f"**Sites:** {stats['sites_tracked']}")
        
        with col3:
            st.write(f"**Average Price:** ₹{stats['avg_price']}")
            st.write(f"**Last Updated:** {stats['last_updated']}")
    else:
        st.info("No data available. Click 'Generate New Data' to create sample data.")

if __name__ == "__main__":
    main()