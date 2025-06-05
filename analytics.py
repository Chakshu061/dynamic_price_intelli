import pandas as pd
import json
from datetime import datetime, timedelta
import statistics

class PriceAnalytics:
    def __init__(self, data_file='price_data.json'):
        self.data_file = data_file
        self.load_data()
    
    def load_data(self):
        """Load data from JSON"""
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except:
            self.data = {'products': [], 'price_history': []}
    
    def get_products_df(self):
        """Get products as DataFrame"""
        return pd.DataFrame(self.data['products'])
    
    def get_price_history_df(self):
        """Get price history as DataFrame"""
        df = pd.DataFrame(self.data['price_history'])
        if not df.empty:
            df['scraped_at'] = pd.to_datetime(df['scraped_at'])
        return df
    
    def get_category_analysis(self):
        """Analyze prices by category"""
        df = self.get_price_history_df()
        if df.empty:
            return pd.DataFrame()
        
        # Get latest prices only
        latest_prices = df.loc[df.groupby(['product_name', 'site'])['scraped_at'].idxmax()]
        
        analysis = latest_prices.groupby('category').agg({
            'price': ['count', 'mean', 'min', 'max', 'std']
        }).round(2)
        
        analysis.columns = ['Count', 'Avg_Price', 'Min_Price', 'Max_Price', 'Price_StdDev']
        return analysis.reset_index()
    
    def get_site_comparison(self):
        """Compare prices across sites"""
        df = self.get_price_history_df()
        if df.empty:
            return pd.DataFrame()
        
        # Get latest prices only
        latest_prices = df.loc[df.groupby(['product_name', 'site'])['scraped_at'].idxmax()]
        
        comparison = latest_prices.groupby(['category', 'site'])['price'].mean().unstack(fill_value=0).round(2)
        return comparison
    
    def get_price_trends(self, category=None):
        """Get price trends over time"""
        df = self.get_price_history_df()
        if df.empty:
            return pd.DataFrame()
        
        if category:
            df = df[df['category'] == category]
        
        # Group by date and calculate average prices
        df['date'] = df['scraped_at'].dt.date
        trends = df.groupby(['date', 'site'])['price'].mean().reset_index()
        
        return trends
    
    def get_price_alerts(self, threshold_percent=15):
        """Find products with significant price differences between sites"""
        df = self.get_price_history_df()
        if df.empty:
            return []
        
        # Get latest prices
        latest_prices = df.loc[df.groupby(['product_name', 'site'])['scraped_at'].idxmax()]
        
        alerts = []
        
        # Group by category and find price differences
        for category in latest_prices['category'].unique():
            cat_data = latest_prices[latest_prices['category'] == category]
            
            # Compare prices between sites for similar products
            amazon_avg = cat_data[cat_data['site'] == 'Amazon']['price'].mean()
            flipkart_avg = cat_data[cat_data['site'] == 'Flipkart']['price'].mean()
            
            if amazon_avg > 0 and flipkart_avg > 0:
                if amazon_avg > flipkart_avg:
                    price_diff_percent = ((amazon_avg - flipkart_avg) / flipkart_avg) * 100
                    cheaper_site = 'Flipkart'
                    min_price = flipkart_avg
                    max_price = amazon_avg
                else:
                    price_diff_percent = ((flipkart_avg - amazon_avg) / amazon_avg) * 100
                    cheaper_site = 'Amazon'
                    min_price = amazon_avg
                    max_price = flipkart_avg
                
                if price_diff_percent > threshold_percent:
                    alerts.append({
                        'category': category,
                        'cheaper_site': cheaper_site,
                        'min_price': round(min_price, 2),
                        'max_price': round(max_price, 2),
                        'difference_percent': round(price_diff_percent, 1),
                        'potential_savings': round(max_price - min_price, 2)
                    })
        
        return sorted(alerts, key=lambda x: x['difference_percent'], reverse=True)
    
    def get_summary_stats(self):
        """Get overall summary statistics"""
        products_df = self.get_products_df()
        price_df = self.get_price_history_df()
        
        if products_df.empty or price_df.empty:
            return {}
        
        # Get latest prices only for current statistics
        latest_prices = price_df.loc[price_df.groupby(['product_name', 'site'])['scraped_at'].idxmax()]
        
        return {
            'total_products': len(products_df),
            'total_price_points': len(price_df),
            'categories_tracked': len(price_df['category'].unique()),
            'sites_tracked': len(price_df['site'].unique()),
            'avg_price': round(latest_prices['price'].mean(), 2),
            'price_range': f"₹{latest_prices['price'].min():.0f} - ₹{latest_prices['price'].max():.0f}",
            'cheapest_category': latest_prices.groupby('category')['price'].mean().idxmin(),
            'most_expensive_category': latest_prices.groupby('category')['price'].mean().idxmax(),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }