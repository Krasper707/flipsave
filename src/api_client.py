# src/api_client.py

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

SEARCH_KEYWORDS = "amazon discount OR flipkart offer OR myntra sale"

def fetch_news_data():
    """
    Fetches news articles from NewsAPI based on search keywords.
    
    Returns:
        A list of dictionaries, where each dictionary contains the raw text 
        of an article's title and description.
    """
    if not API_KEY:
        print("Error: NEWS_API_KEY not found in .env file.")
        print("Please get a key from newsapi.org and add it to your .env file.")
        return []

    print(f"Fetching news articles with keywords: '{SEARCH_KEYWORDS}'...")

    params = {
        'q': SEARCH_KEYWORDS,
        'language': 'en',
        'sortBy': 'publishedAt', 
        'pageSize': 50,
        'apiKey': API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NewsAPI: {e}")
        return []

    data = response.json()

    if data.get("status") != "ok":
        print(f"NewsAPI returned an error: {data.get('message')}")
        return []

    articles = data.get("articles", [])
    print(f"Successfully fetched {len(articles)} articles.")

    extracted_data = []
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')

        if title and description:
            raw_text = f"{title}. {description}"
            extracted_data.append({"raw_text": raw_text})
            
    return extracted_data


if __name__ == "__main__":
    raw_articles = fetch_news_data()
    if raw_articles:
        output_path = 'data/raw_api_data.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(raw_articles, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {len(raw_articles)} articles to {output_path}")
