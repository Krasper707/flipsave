import pandas as pd

def load_financial_texts(filepath: str):
    """Loads and cleans the financial text data."""
    df = pd.read_csv(filepath)
    df.dropna(subset=['text_input'], inplace=True)
    return df['text_input'].tolist()