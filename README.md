# FlipSave - AI Financial Data Pipeline

An end-to-end data pipeline that extracts real-world offer data from the internet, transforms it into structured information using Google Gemini, and makes it available for financial applications.

## 🚀 Overview

FlipSave has evolved from a simple API into a complete, automated ETL (Extract, Transform, Load) data pipeline. This project demonstrates a full-stack AI workflow, from proactive data gathering to intelligent processing and storage.

The pipeline uses the **NewsAPI** to extract real-time articles about discounts and sales. This unstructured text is then fed into a sophisticated model powered by **Google's Gemini Pro** and **Langchain**, which transforms it into clean, categorized, and structured JSON. The final, valuable data is saved to a CSV, ready for analysis or application use.

This project was built as a portfolio piece to demonstrate skills required for the **AI Intern role at Paybyflip**, showcasing expertise in **Data Pipelines, API Integration, LLMs, and Automation.**

## ✨ Key Features

- **Automated Data Pipeline:** A complete, runnable ETL workflow that gathers and processes data with a single command (`run_pipeline.py`).
- **API-Driven Data Extraction:** Robustly fetches real-world data from the NewsAPI, demonstrating professional third-party API integration.
- **Intelligent LLM Transformation:** Uses Gemini to perform complex entity extraction (vendor, amount, offers, codes) and classification (category).
- **Structured Data Output:** Produces a clean, analysis-ready CSV file with valuable, structured offer information.
- **Modular and Professional Code:** Well-structured Python code with clear separation of concerns (Extract, Transform, Orchestrate).
- **AI-Powered Reporting:** Features an "AI Analyst" that generates natural language summaries and insights from the processed data.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **AI/ML:**
  - **LLM:** Google Gemini 1.5 Pro
  - **Framework:** Langchain (`langchain`, `langchain-google-genai`)
- **Data Pipeline:**
  - **Extraction:** Requests, NewsAPI
  - **Transformation & Load:** Pandas, Pydantic
- **Original API Component:** FastAPI, Uvicorn

## ⚙️ How to Run the Data Pipeline

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

Create a `.env` file and add your unique API keys.

```env
GOOGLE_API_KEY="your-google-api-key"
NEWS_API_KEY="your-news-api-key"
```

### 5. Run the Entire Pipeline

Execute the master orchestrator script. This will run all steps: fetching from the API, processing with the LLM, and saving the final CSV.

```bash
python run_pipeline.py
```

Upon completion, you will find the final structured data in `data/processed_offers_from_api.csv`.

---

## 🔬 Original API Server (For Testing Core Logic)

This project also includes the original FastAPI server used for development and single-text testing.

**To Run the Server:**

```bash
uvicorn src.main:app --reload
```

You can then access the interactive documentation at `http://127.0.0.1:8000/docs` to test individual text strings.

## 📊 Interactive Analysis Dashboard

This project includes a live, interactive dashboard built with Streamlit to visualize and explore the processed data. The dashboard also includes an **AI Analyst** feature that generates a written summary of the key trends in the data with the click of a button.

### How to Run the Dashboard

1. Ensure you have run the data pipeline at least once to generate the `processed_offers_from_api.csv` file.
2. In your terminal, run the following command:

```bash
streamlit run dashboard.py
```
