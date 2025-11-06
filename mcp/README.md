## LangChain and Model Context Protocol (MCP) Examples

This project demonstrates how to create LangChain agents that utilize tools exposed via the Model Context Protocol (MCP). It includes two examples:

1. **Adzuna Job Search Agent** (`run_adzuna_agent.py`) - Connects to the Adzuna MCP server to search for jobs and company information
2. **String Tools Agent** (`run_agent.py`) - Uses a local MCP server for string manipulation tools

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.12

- Conda (Miniconda or Anaconda)

- A Google API Key for the Gemini model. This key must be set as an environment variable named `GOOGLE_API_KEY`.

### Setup

- Create and Activate the Conda Environment:

  The `environment.yml` file specifies all the necessary dependencies.

  Navigate to the project directory and run the following command to create the environment:

  ```
  conda env create -f environment.yml
  ```

- Activate the Environment:
  After the environment is created, activate it with this command:
  ```
  conda activate mcp-env
  ```
- Set Your Google API Key:

  Make sure your GOOGLE_API_KEY is set in your environment.

  On Linux/macOS:

  ```
  export GOOGLE_API_KEY="your-api-key"
  ```

  On Windows (Command Prompt):

  ```
  set GOOGLE_API_KEY="your-api-key"
  ```

### Running the Examples

#### Example 1: Adzuna Job Search Agent

This agent connects to the Adzuna MCP server to search for jobs and get company information:

```bash
python run_adzuna_agent.py
```

**Expected Output:**

```
Connecting to Adzuna MCP server at https://adzuna-mcp-server-236255620233.us-central1.run.app/mcp...
✓ Connected!
✓ Found 9 tools

Available tools:
  - search_jobs
  - get_categories
  - get_top_companies
  ...

Agent ready!

=== Example 1: Searching for data science jobs ===
Response: I found 1746 data scientist jobs in Singapore. Here are the top 3:

1.  **Data Scientist** at Changi Airport Group
2.  **Data Scientist** at TEKsystems
3.  **Data Scientist** at HYUNDAI MOTOR GROUP INNOVATION CENTER IN SINGAPORE PTE. LTD.

============================================================

=== Example 2: Top companies hiring ===
Response: The top companies hiring in Singapore are Nanyang Technological University, Marina Bay Sands, Micron Semiconductor Asia, OCBC, and PricewaterhouseCoopers.
```

#### Example 2: String Tools Agent

This agent uses a local MCP server for string manipulation:

```bash
python run_agent.py
```

**Expected Output:**

```
Reverse response: The reversed string is 'dlrow olleh'.
Word-count response: There are 5 words.
```

### Code Explanation

#### Adzuna Job Search Agent (`run_adzuna_agent.py`)

This script demonstrates connecting to a remote MCP server using FastMCP Client:

- **`json_schema_to_pydantic()`**: Converts JSON schema from MCP tools to Pydantic models for proper type validation
- **`create_tool_from_mcp()`**: Wraps MCP tools as LangChain StructuredTools with proper async support
- **`Client(server_url)`**: FastMCP client that connects to the remote Adzuna MCP server via HTTPS
- **`client.list_tools()`**: Retrieves available tools from the MCP server
- **`create_react_agent(model, langchain_tools)`**: Creates a ReAct-style agent that can reason and use tools

The agent can:

- Search for jobs by keywords and location
- Get top hiring companies
- Retrieve job categories, salary data, and more

#### String Tools Server and Agent

**`string_tools_server.py`**: A local MCP server that exposes string manipulation tools

- `FastMCP("StringTools")`: Initializes a new MCP server
- `@mcp.tool()`: Decorator that registers Python functions as callable tools
- `mcp.run(transport="stdio")`: Starts the server using standard I/O transport

**`run_agent.py`**: Agent that connects to the local string tools server

- `MultiServerMCPClient`: Connects to the MCP tool server using stdio transport
- `tools = await client.get_tools()`: Retrieves available tools from the server
- `create_react_agent(model, tools)`: Creates a ReAct-style agent that can use the tools
- `agent.ainvoke(...)`: Sends prompts and receives responses, using tools as needed
