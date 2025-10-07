
import os
import json

from api_client import fetch_news_data
from process_api_data import transform_raw_data

RAW_DATA_PATH = 'data/raw_api_data.json'

def main_pipeline():
    """
    Runs the full ETL (Extract, Transform, Load) data pipeline.
    
    1. Extract: Fetches raw data from the NewsAPI.
    2. Transform & Load: Processes the raw data using the Gemini LLM 
       and loads the structured result into a CSV file.
    """
    print("--- [START] Kicking off the FlipSave Data Pipeline ---")

    # --- Step 1: EXTRACT ---
    print("\n[Step 1/2] Running EXTRACTION from NewsAPI...")
    raw_articles = fetch_news_data()
    
    if not raw_articles:
        print("\nExtraction failed or returned no data. Halting pipeline.")
        return

    # Save the intermediate raw data so we can inspect it if needed
    with open(RAW_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(raw_articles, f, indent=2, ensure_ascii=False)
    print(f"Extraction successful. Saved {len(raw_articles)} raw articles to {RAW_DATA_PATH}")

    # --- Step 2: TRANSFORM & LOAD ---
    print("\n[Step 2/2] Running TRANSFORMATION using Gemini and saving to CSV...")
    transform_raw_data()

    print("\n--- [SUCCESS] FlipSave Data Pipeline finished successfully! ---")
    print("Check 'data/processed_offers_from_api.csv' for the final, structured output.")


if __name__ == "__main__":
    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    main_pipeline()