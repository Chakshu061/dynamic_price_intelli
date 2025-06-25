# 🛍️ Dynamic Price Intelligence Platform

A data engineering project that scrapes historical product prices from Common Crawl and visualizes price inflation over time.

---

### 🔍 Objective

Use petabytes of archived web data (Common Crawl) to:

- Extract product prices from e-commerce sites like Amazon
- Clean, transform, and store structured data
- Build a dashboard to analyze pricing trends and detect inflation

---

### ⚙️ Pipeline Overview

1. **Data Extraction**
   - Domain: `amazon.com`
   - Index: `Common Crawl`
   - Technology: WARC, CDX, `requests`, `gzip`

2. **Parsing & Cleaning**
   - Extracts: Title, ASIN, Price, Rating, URL
   - Price cleaning: Removes `$`, `,`; ensures float conversion

3. **Storage**
   - Format: JSON (`data/products.json`)
   - Cleaned schema: `title`, `price`, `rating`, `url`, `sid`, `uid`

4. **Dashboard**
   - Built with **Streamlit**
   - Shows price distribution, ratings, ASIN-based filtering

---

### 📊 Dashboard Preview

![Dashboard](screenshots/dashboard_preview.png)

---

### 💡 Tools Used

| Component        | Tool/Library            |
|------------------|-------------------------|
| Data Source      | Common Crawl (WARC/CDX) |
| Parsing          | BeautifulSoup           |
| Extraction       | Requests + Range Header |
| Processing       | Python, Regex, JSON     |
| Dashboard        | Streamlit               |
| Deployment       | Local (can be Dockerized) |

---

### 🚀 Run It Yourself

```bash
# Install requirements
pip install -r requirements.txt

# Scrape product prices (Amazon)
python main.py --domain amazon.com

# Run dashboard
cd dash
streamlit run streamlit_dash.py
