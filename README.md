# 💰 Dynamic Pricing Intelligence Platform

A lightweight price monitoring and competitive analysis platform built with Python, Streamlit, and web scraping.

## 🚀 Quick Start (5 minutes)

### 1. Setup
```bash
# Create project folder
mkdir pricing-intelligence
cd pricing-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas requests beautifulsoup4 plotly schedule fake-useragent

# Copy the code files (from the artifacts above)
# Create: scraper.py, analytics.py, dashboard.py, main.py
```

### 2. Run the Platform
```bash
# Option 1: Quick demo
python main.py

# Option 2: Direct dashboard
streamlit run dashboard.py
```

### 3. Access Dashboard
- Open browser to `http://localhost:8501`
- Navigate through: Dashboard → Data Collection → Start Data Collection
- Wait 2-3 minutes for scraping to complete
- Explore the analytics!

## 📊 Features

### ✅ **Data Collection**
- Scrapes Amazon & Flipkart for 10 product categories
- Extracts: Product name, price, URL, category, site
- Stores data in JSON (no database setup needed)
- Handles rate limiting and error recovery

### ✅ **Price Analytics**
- Category-wise price analysis
- Site comparison (Amazon vs Flipkart)
- Price difference alerts
- Statistical analysis (mean, min, max, std dev)

### ✅ **Interactive Dashboard**
- Real-time metrics display
- Interactive charts (bar, pie, box plots)
- Price alerts with customizable thresholds
- Data export capabilities

### ✅ **Automation Ready**
- Scheduled scraping capability
- Alert system for price changes
- Easy to extend with more sites/categories

## 🛠 Technical Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **Backend** | Python 3.9+ | Easy to learn, great for scraping |
| **Web Scraping** | BeautifulSoup + Requests | Reliable, free, no browser needed |
| **Data Storage** | JSON files | No database setup, portable |
| **Analytics** | Pandas + NumPy | Industry standard for data analysis |
| **Dashboard** | Streamlit | Creates web app with just Python |
| **Visualization** | Plotly | Interactive charts, professional look |
| **Deployment** | Streamlit Cloud (free) | No server costs |

## 📁 Project Structure

```
pricing-intelligence/
├── scraper.py          # Web scraping logic
├── analytics.py        # Price analysis functions
├── dashboard.py        # Streamlit web dashboard
├── main.py            # Demo runner
├── price_data.json    # Data storage (auto-generated)
└── requirements.txt   # Dependencies
```

## 🎯 Resume Impact

This project demonstrates:

### **Technical Skills**
- **Web Scraping**: Automated data collection from multiple sources
- **Data Analysis**: Statistical analysis and trend identification
- **API Integration**: RESTful data processing
- **Dashboard Development**: Interactive BI visualization
- **Error Handling**: Robust scraping with retry logic

### **Business Value**
- **Competitive Intelligence**: Real-time price monitoring
- **Decision Support**: Price difference alerts and recommendations
- **Automation**: Scheduled data collection and reporting
- **Scalability**: Easy to add new sites and categories

### **Problem-Solving Approach**
- **End-to-end Solution**: From data collection to insights
- **User-Friendly Interface**: Non-technical users can operate
- **Cost-Effective**: Built entirely with free tools
- **Maintainable**: Clean, modular code structure

## 🔧 Customization Options

### Add New Sites
```python
# In scraper.py, add new scraping function
def scrape_myntra_search(self, search_term, max_results=10):
    # Implementation here
    pass
```

### Add New Categories
```python
# In scraper.py, modify categories list
categories = [
    'laptop', 'smartphone', 'headphones', 'shoes', 'books',
    'watch', 'backpack', 'camera', 'tablet', 'speaker',
    'furniture', 'clothing', 'gaming'  # Add these
]
```

### Schedule Automatic Scraping
```python
import schedule
import time

def job():
    scraper = SimplePriceScraper()
    scraper.run_full_scrape()

schedule.every(6).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 🚀 Deployment (Free Options)

### 1. Streamlit Cloud (Recommended)
- Push code to GitHub
- Connect GitHub to Streamlit Cloud
- Auto-deploy on code changes
- **Cost: Free**

### 2. Heroku
- Add `Procfile`: `web: streamlit run dashboard.py`
- Deploy via Git
- **Cost: Free tier available**

### 3. Railway
- Connect GitHub repository
- Automatic deployments
- **Cost: Free tier available**

## 📈 Potential Enhancements

### Week 2+ (If you want to expand)
1. **Email Alerts**: Send notifications for price drops
2. **Price Prediction**: ML models for price forecasting
3. **User Accounts**: Save favorite products
4. **Mobile App**: React Native or Flutter frontend
5. **API Endpoints**: REST API for external integration

## 🎬 Demo Script

For interviews, you can demo:

1. **Problem Statement**: "Companies need to monitor competitor pricing"
2. **Solution**: "Built automated price intelligence platform"
3. **Data Collection**: Show scraping 100+ products in real-time
4. **Analytics**: Demonstrate price comparison and alerts
5. **Business Impact**: "Identifies 20%+ price differences for competitive advantage"

## 💡 Interview Talking Points

### **Architecture Decisions**
- "Used JSON storage for simplicity and portability"
- "Chose Streamlit for rapid prototyping and deployment"
- "Implemented rate limiting to respect website policies"

### **Challenges Solved**
- "Handled dynamic HTML structures across different sites"
- "Implemented error recovery for network failures"
- "Created user-friendly interface for non-technical users"

### **Scalability Considerations**
- "Modular design allows easy addition of new sites"
- "Configurable scraping parameters for different use cases"
- "Ready for database migration when scaling up"

## 🔍 What Recruiters Will Notice

1. **Full-Stack Thinking**: Data collection → Analysis → Visualization
2. **Business Acumen**: Understanding of competitive intelligence
3. **Technical Diversity**: Web scraping, data analysis, dashboard creation
4. **Problem-Solving**: Handling real-world challenges (rate limiting, error handling)
5. **User Experience**: Built interface that non-technical users can operate

---

**Time to Complete**: 1 week
**Skill Level**: Beginner to Intermediate
**Cost**: $0 (completely free)
**Impact**: High (shows full-stack capabilities)

This project perfectly balances technical complexity with practical business value, making it ideal for your resume and interviews! 🎯
