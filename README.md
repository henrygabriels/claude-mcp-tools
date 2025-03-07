# Claude MCP Tools

A collection of [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers for extending Claude's capabilities.

## What is MCP?

The Model Context Protocol (MCP) is an open standard developed by Anthropic that enables secure, two-way connections between AI models like Claude and external data sources, APIs, or tools. 

MCP provides three main capabilities:
- **Tools**: Functions that can be called by Claude (with user approval)
- **Resources**: File-like data that can be read by clients 
- **Prompts**: Pre-written templates that help users accomplish specific tasks

## Servers in this Repository

This repository contains the following MCP servers:

1. **news-search-server**: A server that enables Claude to search for and retrieve recent news articles
2. **wikipedia-server**: Allows Claude to search and retrieve content from Wikipedia
3. **analytics-server**: A server for performing data analysis on CSV files

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Claude Desktop App installed (v1.2.0+)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/henrygabriels/claude-mcp-tools.git
cd claude-mcp-tools
```

2. Set up a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure Claude Desktop to use these servers by editing your configuration file:
```
# On macOS
~/Library/Application Support/Claude/claude_desktop_config.json
# On Windows
%APPDATA%\Claude\claude_desktop_config.json
```

Add the following to your configuration:
```json
{
  "mcpServers": {
    "news-search": {
      "command": "python /absolute/path/to/claude-mcp-tools/news-search-server/server.py"
    },
    "wikipedia": {
      "command": "python /absolute/path/to/claude-mcp-tools/wikipedia-server/server.py"
    },
    "analytics": {
      "command": "python /absolute/path/to/claude-mcp-tools/analytics-server/server.py"
    }
  }
}
```

4. Restart Claude Desktop

## Building Your Own MCP Server

To create your own MCP server, follow these steps:

1. Create a new directory for your server
2. Create a Python file with your server logic using the MCP SDK
3. Define the tools you want to expose
4. Add your server to the Claude Desktop configuration

See the [official MCP quickstart guide](https://modelcontextprotocol.io/quickstart) for more details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/docs)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP GitHub Repositories](https://github.com/modelcontextprotocol)
