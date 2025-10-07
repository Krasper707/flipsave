
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="FlipSave Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    """Loads the processed data from the CSV file."""
    try:
        df = pd.read_csv('data/processed_offers_from_api.csv')
        # Basic data cleaning
        df['vendor'] = df['vendor'].str.strip().str.title()
        return df
    except FileNotFoundError:
        return None

df = load_data()

st.title("FlipSave: AI Data Pipeline Analysis")
st.markdown("This dashboard provides an interactive analysis of the offer data extracted and processed by the FlipSave AI pipeline.")

st.sidebar.header("Filters & Info")
st.sidebar.markdown("Use the filters below to explore the dataset.")

if df is None:
    st.error("Data not found. Please run the main pipeline first by executing `python run_pipeline.py`.")
else:
    # --- Sidebar Filters ---
    all_vendors = sorted(df['vendor'].dropna().unique())
    selected_vendors = st.sidebar.multiselect(
        "Select Vendors",
        options=all_vendors,
        default=all_vendors[:5] # Default to the first 5 vendors
    )

    all_categories = sorted(df['category'].dropna().unique())
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=all_categories,
        default=all_categories
    )

    filtered_df = df[
        df['vendor'].isin(selected_vendors) &
        df['category'].isin(selected_categories)
    ]

    st.markdown("---")

    total_offers = len(filtered_df)
    unique_vendors_selected = filtered_df['vendor'].nunique()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Offers Displayed", value=total_offers)
    with col2:
        st.metric(label="Unique Vendors in Selection", value=unique_vendors_selected)

    st.markdown("---")

    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Vendors by Offer Count")
        if not filtered_df.empty:
            vendor_counts = filtered_df['vendor'].value_counts().nlargest(10)
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.barplot(x=vendor_counts.values, y=vendor_counts.index, ax=ax1, palette="viridis", hue=vendor_counts.index, legend=False)
            ax1.set_title("Top 10 Vendors in Selection")
            ax1.set_xlabel("Number of Offers")
            ax1.set_ylabel("Vendor")
            st.pyplot(fig1)
        else:
            st.warning("No data available for the selected filters.")

    with col2:
        st.subheader("Offer Distribution by Category")
        if not filtered_df.empty:
            category_counts = filtered_df['category'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
            ax2.set_title("Distribution of Offer Categories")
            ax2.axis('equal')
            st.pyplot(fig2)
        else:
            st.warning("No data available for the selected filters.")
    
    st.markdown("---")

    st.subheader("Filtered Offer Data")
    st.dataframe(filtered_df)

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**About FlipSave:**\n"
        "This project demonstrates an end-to-end ETL pipeline using an LLM to process real-world data."
    )