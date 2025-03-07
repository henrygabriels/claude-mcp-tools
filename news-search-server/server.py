from typing import Any, List, Optional
import httpx
import json
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta

# Initialize FastMCP server
mcp = FastMCP("news-search")

# Constants
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"  # Replace with your News API key
NEWS_API_BASE = "https://newsapi.org/v2"

async def make_news_request(endpoint: str, params: dict) -> dict[str, Any] | None:
    """Make a request to the News API with proper error handling."""
    # Add API key to params
    params["apiKey"] = NEWS_API_KEY
    
    url = f"{NEWS_API_BASE}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making news request: {e}")
            return None

def format_article(article: dict) -> str:
    """Format a news article into a readable string."""
    title = article.get("title", "No title")
    source = article.get("source", {}).get("name", "Unknown source")
    author = article.get("author", "Unknown author")
    published = article.get("publishedAt", "Unknown publication date")
    description = article.get("description", "No description available")
    url = article.get("url", "#")
    
    # Format the date if available
    try:
        published_date = datetime.fromisoformat(published.replace("Z", "+00:00"))
        published = published_date.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass
    
    return f"""
Title: {title}
Source: {source}
Author: {author}
Published: {published}
Description: {description}
URL: {url}
"""

@mcp.tool()
async def search_news(query: str, from_date: Optional[str] = None, to_date: Optional[str] = None, sort_by: str = "publishedAt", language: str = "en") -> str:
    """Search for news articles based on keywords and filters.
    
    Args:
        query: Keywords or phrases to search for
        from_date: Start date in YYYY-MM-DD format (defaults to 7 days ago)
        to_date: End date in YYYY-MM-DD format (defaults to today)
        sort_by: How to sort articles - 'relevancy', 'popularity', or 'publishedAt' (default)
        language: Two-letter language code (default: 'en' for English)
    """
    # Set default dates if not provided
    if not from_date:
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")
    
    # Validate sort_by parameter
    valid_sort_options = ["relevancy", "popularity", "publishedAt"]
    if sort_by not in valid_sort_options:
        sort_by = "publishedAt"
    
    # Build parameters
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "sortBy": sort_by,
        "language": language,
        "pageSize": 10  # Limit results to 10 articles
    }
    
    # Make the request
    data = await make_news_request("everything", params)
    
    if not data or "articles" not in data:
        return "Unable to fetch news articles."
    
    if not data["articles"]:
        return f"No articles found for query: {query}"
    
    articles = [format_article(article) for article in data["articles"]]
    
    result = f"Found {len(articles)} news articles for '{query}':\n\n"
    result += "\n---\n".join(articles)
    
    return result

@mcp.tool()
async def get_top_headlines(country: str = "us", category: Optional[str] = None, query: Optional[str] = None) -> str:
    """Get top headlines by country, category, and/or keywords.
    
    Args:
        country: Two-letter country code (default: 'us' for United States)
        category: News category - 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology' (optional)
        query: Keywords to filter headlines by (optional)
    """
    # Build parameters
    params = {"country": country}
    
    # Add optional parameters if provided
    if category:
        valid_categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
        if category in valid_categories:
            params["category"] = category
    
    if query:
        params["q"] = query
    
    # Make the request
    data = await make_news_request("top-headlines", params)
    
    if not data or "articles" not in data:
        return "Unable to fetch top headlines."
    
    if not data["articles"]:
        return f"No top headlines found for the specified filters."
    
    articles = [format_article(article) for article in data["articles"]]
    
    result = f"Top headlines"
    if category:
        result += f" in {category}"
    if country:
        result += f" from {country.upper()}"
    if query:
        result += f" matching '{query}'"
    result += ":\n\n"
    
    result += "\n---\n".join(articles)
    
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
