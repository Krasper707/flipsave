# FlipSave - AI Financial Text Processor

An intelligent API to extract and categorize information from unstructured financial text messages using Google Gemini.

## 🚀 Overview

FlipSave is an intelligent API designed to automate the extraction and categorization of financial information from unstructured text messages, such as bank alerts and promotional offers. This project leverages the power of **Google's Gemini Pro** model via **Langchain** to transform messy text data into clean, structured JSON, making it ready for downstream financial applications.

This project was built as a portfolio piece to demonstrate skills required for the **AI Intern role at Paybyflip**, focusing on LLMs, Data Processing, and API development.

## ✨ Key Features

- **Intelligent Entity Extraction:** Parses text to identify key entities like vendor, amount, offer details, and coupon codes.
- **Automated Categorization:** Assigns a relevant category (e.g., "Food & Dining", "Shopping") to each transaction or offer.
- **Robust API:** A production-ready REST API built with **FastAPI**, complete with automatic data validation and interactive documentation.
- **Resilient Logic:** The core extraction chain includes an automatic retry mechanism to handle transient API failures.
- **Bulk Testing:** Includes a test script to validate API performance against a sample CSV dataset.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **AI/ML:**
  - **LLM:** Google Gemini 1.5 Pro
  - **Framework:** Langchain (`langchain`, `langchain-google-genai`)
- **API:** FastAPI, Uvicorn
- **Data Handling:** Pydantic, Pandas
- **Testing:** Requests

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Krasper707/flipsave.git
cd flipsave
```

### 2. Set Up a Virtual Environment

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project of the form

```bash
GOOGLE_API_KEY="your-google-api-key-goes-here"
```

### 5. Run the API Server

```bash
uvicorn src.main:app --reload
```

The server will be running at `http://127.0.0.1:8000`.

## 📚 API Usage

### Interactive Documentation

Once the server is running, access the interactive Swagger UI documentation at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** to test the endpoint live.

### Testing with the CSV file

To run the bulk test script against the `sample_data.csv`:

1. Keep the API server running in one terminal.
2. In a second terminal (with the venv activated), run:

```bash
python test_api.py
```

### Example `curl` Request

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/process-text/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Get 50% off on your Myntra order of Rs. 1500. Use code SAVEBIG. Valid till 31st Dec."
}'
```

---
