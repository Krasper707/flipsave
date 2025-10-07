# test_api.py

import pandas as pd
import requests
import json
import time

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/process-text/"
DATA_FILE_PATH = "data/sample_data.csv"
# We can test a subset of the data to be quick, or all of it.
# Use None to test all rows, or a number like 5 to test the first 5.
NUM_ROWS_TO_TEST = 5 

def test_api_with_csv():
    """
    Reads financial texts from a CSV file and tests them against the running API.
    """
    print("--- Starting API Bulk Test ---")
    
    try:
        df = pd.read_csv(DATA_FILE_PATH)
        print(f"Successfully loaded {len(df)} rows from {DATA_FILE_PATH}")
    except FileNotFoundError:
        print(f"Error: The file {DATA_FILE_PATH} was not found.")
        print("Please ensure the CSV file exists and the path is correct.")
        return

    # Handle slicing the dataframe for testing
    if NUM_ROWS_TO_TEST is not None:
        df_to_test = df.head(NUM_ROWS_TO_TEST)
        print(f"Testing the first {NUM_ROWS_TO_TEST} rows...")
    else:
        df_to_test = df
        print("Testing all rows in the file...")

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    for index, row in df_to_test.iterrows():
        input_text = row['text_input']
        
        # Create the JSON payload for the POST request
        payload = {
            "text": input_text
        }
        
        print(f"\n--- [Test Case {index + 1}] ---")
        print(f"Input:  {input_text}")
        
        try:
            # Make the POST request to the API
            response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
            
            # Check if the request was successful
            if response.status_code == 200:
                print("Output:")
                # The response.json() method parses the JSON from the response
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Error: API returned status code {response.status_code}")
                print(f"Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print("\nFATAL ERROR: Could not connect to the API.")
            print(f"Please make sure the FastAPI server is running at {API_URL}")
            return # Exit the function if the server is not running
        
        # A small delay to avoid overwhelming the free-tier API limits
        time.sleep(1) 

if __name__ == "__main__":
    test_api_with_csv()