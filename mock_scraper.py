import json
import random
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()

class MockPriceScraper:
    def __init__(self):
        self.data_file = 'price_data.json'
        self.categories = {
            'laptop': {
                'brands': ['Dell', 'HP', 'Lenovo', 'ASUS', 'MacBook', 'Acer'],
                'models': ['Inspiron', 'Pavilion', 'ThinkPad', 'VivoBook', 'Air', 'Aspire'],
                'price_range': (25000, 150000)
            },
            'smartphone': {
                'brands': ['iPhone', 'Samsung Galaxy', 'OnePlus', 'Xiaomi', 'Realme', 'Oppo'],
                'models': ['14', 'S23', '11', 'Note 12', '10 Pro', 'Reno'],
                'price_range': (8000, 120000)
            },
            'headphones': {
                'brands': ['Sony', 'JBL', 'Bose', 'Audio-Technica', 'Sennheiser', 'Beats'],
                'models': ['WH-1000XM4', 'Tune 750', 'QuietComfort', 'ATH-M50x', 'HD 450BT', 'Studio3'],
                'price_range': (1500, 35000)
            },
            'shoes': {
                'brands': ['Nike', 'Adidas', 'Puma', 'Reebok', 'New Balance', 'Converse'],
                'models': ['Air Max', 'Ultraboost', 'Suede', 'Classic', '574', 'Chuck Taylor'],
                'price_range': (2000, 15000)
            },
            'books': {
                'brands': ['Penguin', 'HarperCollins', 'Random House', 'Scholastic', 'Oxford', 'Cambridge'],
                'models': ['Classics', 'Modern Fiction', 'Academic', 'Children', 'Reference', 'Textbook'],
                'price_range': (200, 3000)
            },
            'watch': {
                'brands': ['Casio', 'Titan', 'Fossil', 'Timex', 'Seiko', 'Citizen'],
                'models': ['Digital', 'Analog', 'Smart', 'Sports', 'Dress', 'Chronograph'],
                'price_range': (1000, 50000)
            },
            'backpack': {
                'brands': ['American Tourister', 'VIP', 'Wildcraft', 'Skybags', 'Tommy Hilfiger', 'Nike'],
                'models': ['Travel', 'School', 'Laptop', 'Hiking', 'Casual', 'Sport'],
                'price_range': (800, 8000)
            },
            'camera': {
                'brands': ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Panasonic', 'Olympus'],
                'models': ['DSLR', 'Mirrorless', 'Point & Shoot', 'Action', 'Instant', 'Professional'],
                'price_range': (15000, 200000)
            },
            'tablet': {
                'brands': ['iPad', 'Samsung Tab', 'Lenovo Tab', 'Amazon Fire', 'Huawei', 'Microsoft Surface'],
                'models': ['Air', 'S8', 'M10', 'HD 10', 'MatePad', 'Go'],
                'price_range': (8000, 80000)
            },
            'speaker': {
                'brands': ['JBL', 'Sony', 'Bose', 'Marshall', 'Ultimate Ears', 'Harman Kardon'],
                'models': ['Flip', 'SRS-XB', 'SoundLink', 'Acton', 'Boom', 'Onyx'],
                'price_range': (2000, 25000)
            }
        }
        
    def generate_product_name(self, category):
        """Generate realistic product name"""
        cat_data = self.categories[category]
        brand = random.choice(cat_data['brands'])
        model = random.choice(cat_data['models'])
        
        # Add some variation
        extras = ['Pro', 'Plus', 'Max', 'Ultra', 'SE', 'Lite', '']
        extra = random.choice(extras)
        
        if extra:
            return f"{brand} {model} {extra}"
        else:
            return f"{brand} {model}"
    
    def generate_price(self, category, site):
        """Generate realistic price with site-based variation"""
        base_min, base_max = self.categories[category]['price_range']
        
        # Add some randomness
        price = random.uniform(base_min, base_max)
        
        # Site-based price variation (Amazon typically 5-10% higher, Flipkart competitive)
        if site == 'Amazon':
            price *= random.uniform(1.0, 1.15)  # 0-15% higher
        else:  # Flipkart
            price *= random.uniform(0.9, 1.1)   # 10% lower to 10% higher
            
        return round(price, 2)
    
    def generate_mock_products(self, category, products_per_site=8):
        """Generate mock products for a category"""
        products = []
        sites = ['Amazon', 'Flipkart']
        
        for site in sites:
            for _ in range(products_per_site):
                product = {
                    'name': self.generate_product_name(category),
                    'price': self.generate_price(category, site),
                    'url': f"https://www.{site.lower()}.{'in' if site == 'Flipkart' else 'in'}/product/{fake.uuid4()}",
                    'image_url': f"https://via.placeholder.com/300x300?text={category.title()}",
                    'site': site,
                    'category': category,
                    'scraped_at': datetime.now().isoformat(),
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'reviews_count': random.randint(50, 5000)
                }
                products.append(product)
        
        return products
    
    def load_existing_data(self):
        """Load existing data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {'products': [], 'price_history': []}
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def scrape_category(self, category):
        """Generate mock data for a category"""
        print(f"Generating {category} data...")
        products = self.generate_mock_products(category)
        
        amazon_count = len([p for p in products if p['site'] == 'Amazon'])
        flipkart_count = len([p for p in products if p['site'] == 'Flipkart'])
        
        print(f"  Amazon: {amazon_count} products")
        print(f"  Flipkart: {flipkart_count} products")
        
        return products
    
    def run_full_scrape(self):
        """Generate comprehensive mock data"""
        self.load_existing_data()
        
        # Clear existing data for fresh demo
        self.data = {'products': [], 'price_history': []}
        
        all_products = []
        
        for category in self.categories.keys():
            products = self.scrape_category(category)
            all_products.extend(products)
        
        # Add to data structure
        self.data['products'] = all_products
        
        # Create price history (simulate multiple scraping sessions)
        for product in all_products:
            # Current price
            self.data['price_history'].append({
                'product_name': product['name'],
                'site': product['site'],
                'price': product['price'],
                'category': product['category'],
                'scraped_at': product['scraped_at']
            })
            
            # Add historical prices (simulate price changes over time)
            for days_ago in [7, 14, 30]:
                historical_price = product['price'] * random.uniform(0.9, 1.1)  # ±10% variation
                historical_date = (datetime.now() - timedelta(days=days_ago)).isoformat()
                
                self.data['price_history'].append({
                    'product_name': product['name'],
                    'site': product['site'],
                    'price': round(historical_price, 2),
                    'category': product['category'],
                    'scraped_at': historical_date
                })
        
        self.save_data()
        print(f"\n✅ Total products generated: {len(all_products)}")
        return len(all_products)