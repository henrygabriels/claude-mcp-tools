from typing import Any, List, Optional, Dict
import httpx
import json
import re
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("wikipedia")

# Constants
WIKIPEDIA_API_BASE = "https://en.wikipedia.org/w/api.php"

async def make_wikipedia_request(params: Dict[str, Any]) -> dict[str, Any] | None:
    """Make a request to the Wikipedia API with proper error handling."""
    # Add common parameters
    params.update({
        "format": "json",
        "action": "query",
        "formatversion": "2"
    })
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(WIKIPEDIA_API_BASE, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making Wikipedia request: {e}")
            return None

def clean_html(html_text: str) -> str:
    """Remove HTML tags from text."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_text)

@mcp.tool()
async def search_wikipedia(query: str, limit: int = 5, language: str = "en") -> str:
    """Search Wikipedia for articles matching the query.
    
    Args:
        query: Search terms
        limit: Maximum number of results to return (default: 5)
        language: Wikipedia language code (default: 'en' for English)
    """
    try:
        # Update API base URL for language
        global WIKIPEDIA_API_BASE
        WIKIPEDIA_API_BASE = f"https://{language}.wikipedia.org/w/api.php"
        
        # Build parameters for search
        params = {
            "list": "search",
            "srsearch": query,
            "srlimit": limit
        }
        
        # Make the request
        data = await make_wikipedia_request(params)
        
        if not data or "query" not in data or "search" not in data["query"]:
            return f"No Wikipedia articles found for query: {query}"
        
        results = data["query"]["search"]
        
        if not results:
            return f"No Wikipedia articles found for query: {query}"
        
        # Format the results
        formatted_results = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "Unknown title")
            snippet = clean_html(result.get("snippet", "No snippet available"))
            page_id = result.get("pageid", "Unknown ID")
            
            formatted_result = f"{i}. {title}\n"
            formatted_result += f"   Page ID: {page_id}\n"
            formatted_result += f"   Snippet: {snippet}...\n"
            
            formatted_results.append(formatted_result)
        
        return f"Wikipedia search results for '{query}':\n\n" + "\n".join(formatted_results)
    
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

@mcp.tool()
async def get_wikipedia_article(title: str, extract_size: str = "full", language: str = "en") -> str:
    """Get a Wikipedia article by title.
    
    Args:
        title: Title of the Wikipedia article
        extract_size: Amount of content to retrieve ('intro', 'short', 'full')
        language: Wikipedia language code (default: 'en' for English)
    """
    try:
        # Update API base URL for language
        global WIKIPEDIA_API_BASE
        WIKIPEDIA_API_BASE = f"https://{language}.wikipedia.org/w/api.php"
        
        # Map extract_size to exintro and explaintext
        exintro = True if extract_size in ["intro", "short"] else False
        prop = "extracts"
        
        # Build parameters for content retrieval
        params = {
            "titles": title,
            "prop": prop,
            "explaintext": True,  # Plain text instead of HTML
            "exintro": exintro,
            "redirects": True  # Follow redirects
        }
        
        # Add character limit for short extracts
        if extract_size == "short":
            params["exchars"] = 1000
        
        # Make the request
        data = await make_wikipedia_request(params)
        
        if not data or "query" not in data or "pages" not in data["query"]:
            return f"No Wikipedia article found for title: {title}"
        
        pages = data["query"]["pages"]
        
        if not pages:
            return f"No Wikipedia article found for title: {title}"
        
        # Get the first page (should be the only one)
        page = pages[0]
        
        if "missing" in page:
            return f"Wikipedia article '{title}' not found."
        
        page_title = page.get("title", "Unknown title")
        extract = page.get("extract", "No content available")
        
        # Add a Wikipedia URL
        url = f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        
        result = f"# {page_title}\n\n"
        result += extract
        result += f"\n\nSource: {url}"
        
        return result
    
    except Exception as e:
        return f"Error retrieving Wikipedia article: {str(e)}"

@mcp.tool()
async def get_wikipedia_summary(title: str, sentences: int = 3, language: str = "en") -> str:
    """Get a summary of a Wikipedia article.
    
    Args:
        title: Title of the Wikipedia article
        sentences: Number of sentences to include in the summary (default: 3)
        language: Wikipedia language code (default: 'en' for English)
    """
    try:
        # Update API base URL for language
        global WIKIPEDIA_API_BASE
        WIKIPEDIA_API_BASE = f"https://{language}.wikipedia.org/w/api.php"
        
        # Build parameters for summary retrieval
        params = {
            "titles": title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "exsentences": sentences,
            "redirects": True
        }
        
        # Make the request
        data = await make_wikipedia_request(params)
        
        if not data or "query" not in data or "pages" not in data["query"]:
            return f"No Wikipedia article found for title: {title}"
        
        pages = data["query"]["pages"]
        
        if not pages:
            return f"No Wikipedia article found for title: {title}"
        
        # Get the first page (should be the only one)
        page = pages[0]
        
        if "missing" in page:
            return f"Wikipedia article '{title}' not found."
        
        page_title = page.get("title", "Unknown title")
        extract = page.get("extract", "No summary available")
        
        # Add a Wikipedia URL
        url = f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        
        result = f"# Summary: {page_title}\n\n"
        result += extract
        result += f"\n\nSource: {url}"
        
        return result
    
    except Exception as e:
        return f"Error retrieving Wikipedia summary: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
