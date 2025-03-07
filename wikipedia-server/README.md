# Wikipedia MCP Server

This MCP server enables Claude to search for, retrieve, and summarize content from Wikipedia, providing access to a vast knowledge base directly within Claude.

## Features

The server provides three main tools:

1. **search_wikipedia**: Search Wikipedia for articles matching a query
2. **get_wikipedia_article**: Retrieve a complete Wikipedia article by title
3. **get_wikipedia_summary**: Get a concise summary of a Wikipedia article

## Setup

### Prerequisites

- Python 3.10 or higher
- httpx library

### Installation

1. Install the required dependencies:
```bash
pip install -r ../requirements.txt
```

2. Add the server to your Claude Desktop configuration file:
```json
{
  "mcpServers": {
    "wikipedia": {
      "command": "python /absolute/path/to/claude-mcp-tools/wikipedia-server/server.py"
    }
  }
}
```

3. Restart Claude Desktop

## Usage Examples

Once configured, you can use the server through Claude Desktop by asking questions like:

- "Search Wikipedia for information about quantum computing"
- "Get me the Wikipedia article on climate change"
- "Give me a brief summary of black holes from Wikipedia"

## Available Tools and Parameters

### search_wikipedia

Search Wikipedia for articles matching the query.

Parameters:
- `query`: Search terms
- `limit`: Maximum number of results to return (default: 5)
- `language`: Wikipedia language code (default: 'en' for English)

### get_wikipedia_article

Get a Wikipedia article by title.

Parameters:
- `title`: Title of the Wikipedia article
- `extract_size`: Amount of content to retrieve ('intro', 'short', 'full')
- `language`: Wikipedia language code (default: 'en' for English)

### get_wikipedia_summary

Get a summary of a Wikipedia article.

Parameters:
- `title`: Title of the Wikipedia article
- `sentences`: Number of sentences to include in the summary (default: 3)
- `language`: Wikipedia language code (default: 'en' for English)

## Example Workflows

### Research on a Topic

1. "Search Wikipedia for information about artificial intelligence"
2. "Get me a summary of the article on neural networks"
3. "Now retrieve the full Wikipedia article on machine learning"

### Learning About Different Languages

1. "Search Wikipedia for articles about ancient languages"
2. "Get me a summary of Latin from Wikipedia"
3. "Retrieve the Wikipedia article on Sanskrit with language set to 'fr' for French"

## Multilingual Support

The server supports accessing Wikipedia content in different languages by changing the `language` parameter. For example:

- 'en' - English (default)
- 'es' - Spanish
- 'fr' - French
- 'de' - German
- 'zh' - Chinese
- 'ja' - Japanese

And many more. Simply specify the appropriate language code when using the tools.

## Limitations

- The Wikipedia API may have rate limits that could temporarily restrict access
- Very long articles might be truncated due to API limitations
- Some content with complex formatting or elements like tables may not be perfectly represented in text form
- The server does not provide access to edit Wikipedia content (read-only)

## License

This project is licensed under the MIT License.