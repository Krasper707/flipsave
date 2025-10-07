# src/process_api_data.py

import json
import pandas as pd
import time
from .llm_extractor import create_extraction_chain

# --- Configuration ---
INPUT_FILE = 'data/raw_api_data.json'
OUTPUT_FILE = 'data/processed_offers_from_api.csv'
# --- NEW: Add a variable to control how many items to process ---
# Set to None to process all items, or a number to process just the top N.
NUM_ITEMS_TO_PROCESS = 10

def transform_raw_data():
    """
    Reads raw data fetched from the API, processes it through the LLM extractor,
    and saves the structured data to a final CSV file.
    """
    print("--- Starting Data Transformation Step ---")

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print(f"Successfully loaded {len(raw_data)} raw articles from {INPUT_FILE}")
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Please run the api_client.py script first.")
        return

    # --- NEW: Slice the data before processing ---
    if NUM_ITEMS_TO_PROCESS is not None:
        data_to_process = raw_data[:NUM_ITEMS_TO_PROCESS]
        print(f"Processing the top {NUM_ITEMS_TO_PROCESS} items as configured.")
    else:
        data_to_process = raw_data
        print("Processing all items in the file.")
    # ---------------------------------------------

    try:
        extraction_chain = create_extraction_chain()
        print("Successfully initialized the Gemini extraction chain.")
    except Exception as e:
        print(f"Error initializing the extraction chain: {e}")
        return

    structured_results = []
    total_items = len(data_to_process)
    
    print(f"Processing {total_items} articles...")

    # --- UPDATED: Loop over the sliced data ---
    for i, item in enumerate(data_to_process):
        raw_text = item.get("raw_text")
        if not raw_text:
            continue
        
        print(f"  Processing item {i+1}/{total_items}: {raw_text[:70]}...")

        try:
            result = extraction_chain.invoke({"text_input": raw_text})
            # Use the corrected .model_dump() method
            structured_results.append(result.model_dump())
        except Exception as e:
            print(f"    -> Could not process item {i+1}. Error: {e}")
        
        time.sleep(1)

    if not structured_results:
        print("No data was successfully processed. Halting.")
        return
        
    df = pd.DataFrame(structured_results)
    
    # --- UPDATED: Make sure to align the original_text column correctly ---
    df['original_text'] = [item.get("raw_text") for item in data_to_process[:len(structured_results)]]
    
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    
    print("\n--- Transformation complete! ---")
    print(f"Successfully processed and saved {len(structured_results)} items.")
    print(f"Clean, structured data has been saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    transform_raw_data()