import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="📈 Inflation Intelligence Explorer", layout="wide")

st.title("📦 Inflation Intelligence Explorer")
st.markdown("""
A data engineering project that analyzes online product prices extracted from Common Crawl.
Easily track pricing trends, inflation signals, and product segments over time.
""")

# === Load & Clean Data ===
@st.cache_data
def load_data():
    try:
        with open('../data/products.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        # Clean and parse fields
        df['price'] = pd.to_numeric(df['price'].replace('[\$,]', '', regex=True), errors='coerce')
        df['rating'] = pd.to_numeric(df['rating'].replace(',', '', regex=True), errors='coerce')
        df.dropna(subset=['price', 'rating'], inplace=True)

        # Categorize prices
        def categorize_price(p):
            if p < 50:
                return "💲 Budget (<$50)"
            elif p < 150:
                return "💵 Mid-Range ($50–$150)"
            else:
                return "💸 Premium ($150+)"
        df['price_category'] = df['price'].apply(categorize_price)

        # Parse crawl date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.dropna(subset=['date'], inplace=True)

        return df

    except Exception as e:
        st.error(f"❌ Failed to load or clean data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# === Sidebar Filters ===
with st.sidebar:
    st.header("🔍 Filter Products")
    price_range = st.slider("Price range ($)", 0, int(df['price'].max()) + 1, (0, 300))
    rating_min = st.slider("Minimum rating", 0, int(df['rating'].max()), 0)

# Apply filters
filtered_df = df[
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1]) &
    (df['rating'] >= rating_min)
]

# === Tabbed Layout ===
tab1, tab2, tab3 = st.tabs(["📦 Products", "📈 Trends", "📊 Insights"])

# === Tab 1: Product Table ===
with tab1:
    st.subheader("🔍 Filtered Product Listings")
    st.dataframe(filtered_df[['title', 'price', 'rating', 'price_category', 'url']], use_container_width=True)
    st.download_button("📥 Download Filtered Data", filtered_df.to_csv(index=False), "filtered_products.csv", "text/csv")

# === Tab 2: Price Trends ===
with tab2:
    st.subheader("📆 Average Price Trend by Product Tier")

    if 'date' in filtered_df.columns:
        trend_df = filtered_df.copy()
        trend_df['month'] = trend_df['date'].dt.to_period('M').astype(str)

        monthly_avg = (
            trend_df.groupby(['month', 'price_category'])['price']
            .mean()
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=monthly_avg, x='month', y='price', hue='price_category', marker="o")
        ax.set_title("Inflation Trend by Price Category")
        ax.set_ylabel("Avg Price ($)")
        ax.set_xlabel("Month")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    else:
        st.info("ℹ️ No crawl date provided — trend analysis unavailable.")

# === Tab 3: Summary Insights ===
with tab3:
    st.subheader("💡 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Price", f"${filtered_df['price'].mean():.2f}")
    col2.metric("Median Rating", f"{filtered_df['rating'].median():.0f}")
    col3.metric("Unique Products", filtered_df['title'].nunique())

    st.subheader("📉 Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df['price'], bins=30, kde=True, ax=ax)
    ax.set_xlabel("Price ($)")
    ax.set_title("Distribution of Product Prices")
    st.pyplot(fig)

st.caption("✅ Built using Common Crawl + Streamlit • A Data Engineering Showcase by Chakshu Shaktawat")
