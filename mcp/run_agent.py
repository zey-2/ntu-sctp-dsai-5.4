import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")


async def main():
    client = MultiServerMCPClient({
        "string_tools": {
            "transport": "stdio",
            "command": "python",
            "args": ["string_tools_server.py"],
        }
    })

    tools = await client.get_tools()

    if not tools:
        raise RuntimeError("Failed to connect to MCP server")

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    agent = create_react_agent(model, tools)

    resp1 = await agent.ainvoke({"messages": "Reverse the string 'hello world'"})
    print("Reverse response:", resp1["messages"][-1].content)

    resp2 = await agent.ainvoke({"messages": "How many words in 'Model Context Protocol is powerful'?"})
    print("Word-count response:", resp2["messages"][-1].content)

# Run the async function
asyncio.run(main())
