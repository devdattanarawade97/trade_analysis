import os
import requests
import json
import pandas as pd
from datetime import datetime

def get_bitcoin_news(api_key):
    """
    Fetch the latest Bitcoin news from Alpha Vantage API.
    
    Args:
        api_key (str): Your Alpha Vantage API key.
    
    Returns:
        list: A list of the latest Bitcoin news.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": "ETH",
        "apikey": api_key
    }
    
    response = requests.get(base_url, params=params)
    # log response 
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        if "feed" in data:
            return data["feed"]
        else:
            print("Error:", data.get("Note", "No news available."))
            return None
    else:
        print(f"HTTP Error {response.status_code}: {response.reason}")
        return None

def analyze_news(news_data):
    """
    Analyze the Bitcoin news data for sentiment and content.
    
    Args:
        news_data (list): A list of Bitcoin news articles.
    
    Returns:
        DataFrame: A pandas DataFrame with the news analysis results.
    """
    if not news_data:
        print("No news data to analyze.")
        return None
    
    # Prepare the news data
    news_list = []
    for article in news_data:
        title = article.get("title", "No title")
        url = article.get("url", "No URL")
        time_published = article.get("time_published", "No time")
        summary = article.get("summary", "No summary")
        sentiment_score = article.get("sentiment_score", "No sentiment score")
        
        news_list.append({
            "Title": title,
            "URL": url,
            "Time Published": time_published,
            "Summary": summary,
            "Sentiment Score": sentiment_score
        })
    
    # Create a pandas DataFrame for analysis
    df = pd.DataFrame(news_list)
    
    # Convert 'Time Published' to a datetime object
    df["Time Published"] = pd.to_datetime(df["Time Published"], errors="coerce")
    
    # Sort by time to show the latest news first
    df = df.sort_values("Time Published", ascending=False)
    
    return df

def save_to_csv(df, file_name):
    """
    Save the analyzed Bitcoin news data to a CSV file.
    
    Args:
        df (DataFrame): The pandas DataFrame containing news data.
        file_name (str): The name of the output CSV file.
    """
    if df is not None:
        df.to_csv(file_name, index=False)
        print(f"News data saved to {file_name}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    # Replace with your Alpha Vantage API key
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")  # or replace with your key directly
    # log api key 
    print(api_key)
    # Fetch the latest Bitcoin news
    news_data = get_bitcoin_news(api_key)
    
    if news_data:
        # Analyze the news data
        analyzed_df = analyze_news(news_data)
        
        # Save the analyzed data to a CSV file
        save_to_csv(analyzed_df, "bitcoin_latest_news.csv")
