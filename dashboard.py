
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.llm_extractor import get_llm 

from src.llm_extractor import create_extraction_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import json
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

@st.cache_data
def generate_ai_summary(_df):
    """
    Generates a natural language summary of the dataframe using the LLM from the existing extraction chain.
    
    Args:
        _df (pd.DataFrame): The dataframe to analyze.
        
    Returns:
        str: The AI-generated summary.
    """
    if _df.empty:
        return "No data available to generate a summary."

    # 1. Pre-process the data to get key statistics
    offer_df = _df[_df['transaction_type'] == 'Offer'].copy()
    if offer_df.empty:
        return "No 'Offer' type data found to generate a summary."

    total_offers = len(offer_df)
    unique_vendors = offer_df['vendor'].nunique()
    top_5_vendors = offer_df['vendor'].value_counts().nlargest(5).to_dict()
    top_3_categories = offer_df['category'].value_counts().nlargest(3).to_dict()

    stats_summary = f"""
    - Total Offers Analyzed: {total_offers}
    - Unique Vendors Found: {unique_vendors}
    - Top 5 Vendors by Offer Volume: {json.dumps(top_5_vendors)}
    - Top 3 Categories by Offer Volume: {json.dumps(top_3_categories)}
    """

    try:
        llm = get_llm()
    except Exception as e:
        return f"Failed to initialize the language model. Error: {e}"
    
    # 3. Create a specific LLM chain for reporting
    prompt_template = ChatPromptTemplate.from_template(
        """
        You are a sharp and concise financial data analyst. Your task is to write a brief executive summary based on the following statistics extracted from a dataset of recent financial offers.

        **Key Statistics:**
        {stats}

        **Your Report:**
        Based on the data, write a short, insightful summary (3-4 sentences).
        - Start with a clear opening statement about the dataset.
        - Highlight the most dominant vendor or trend.
        - Mention the most common categories.
        - Conclude with a brief closing thought.
        - Use a professional and analytical tone. Do not just list the stats; interpret them.
        """
    )
    
    reporting_chain = prompt_template | llm | StrOutputParser()

    # 4. Invoke the chain to get the report
    try:
        report = reporting_chain.invoke({"stats": stats_summary})
        return report
    except Exception as e:
        return f"An error occurred while generating the report: {e}"

df = load_data()

st.title("FlipSave: AI Data Pipeline Analysis")
st.markdown("This dashboard provides an interactive analysis of the offer data extracted and processed by the FlipSave AI pipeline.")

st.sidebar.header("Filters & Info")
st.sidebar.markdown("Use the filters below to explore the dataset.")

if df is None:
    st.error("Data not found. Please run the main pipeline first by executing `python run_pipeline.py`.")
else:
    st.subheader("🤖 AI-Generated Executive Summary")
    if st.button("Generate Report"):
        with st.spinner("AI Analyst at work... Analyzing trends..."):
            # We will generate a summary based on the full, unfiltered dataset
            summary_report = generate_ai_summary(df)
            st.success("Analysis Complete!")
            st.markdown(summary_report)
    
    st.markdown("---")

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