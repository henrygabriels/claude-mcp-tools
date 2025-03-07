# News Search MCP Server

This MCP server enables Claude to search for and retrieve recent news articles using the [News API](https://newsapi.org/).

## Features

The server provides two main tools:

1. **search_news**: Search for news articles based on keywords, date range, and other filters
2. **get_top_headlines**: Retrieve top headlines by country, category, and/or keywords

## Setup

### Prerequisites

- Python 3.10 or higher
- News API key (get one for free at [newsapi.org](https://newsapi.org/register))

### Installation

1. Replace the placeholder API key in `server.py`:
```python
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"  # Replace with your actual News API key
```

2. Install the required dependencies:
```bash
pip install -r ../requirements.txt
```

3. Add the server to your Claude Desktop configuration file:
```json
{
  "mcpServers": {
    "news-search": {
      "command": "python /absolute/path/to/claude-mcp-tools/news-search-server/server.py"
    }
  }
}
```

4. Restart Claude Desktop

## Usage Examples

Once configured, you can use the server through Claude Desktop by asking questions like:

- "What are the latest news about artificial intelligence?"
- "Search for news articles about climate change from the last week"
- "Get the top headlines in technology"
- "What are the top business news headlines in the UK?"

## Available Parameters

### search_news

- `query`: Keywords or phrases to search for
- `from_date`: Start date in YYYY-MM-DD format (defaults to 7 days ago)
- `to_date`: End date in YYYY-MM-DD format (defaults to today)
- `sort_by`: How to sort articles - 'relevancy', 'popularity', or 'publishedAt' (default)
- `language`: Two-letter language code (default: 'en' for English)

### get_top_headlines

- `country`: Two-letter country code (default: 'us' for United States)
- `category`: News category - 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology' (optional)
- `query`: Keywords to filter headlines by (optional)

## Limitations

- The free tier of News API has a limit of 100 requests per day
- Only news from the last month is available on the free plan
- Some functionality may be restricted based on your News API plan

## License

This project is licensed under the MIT License.
