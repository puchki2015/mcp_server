import asyncio
from pathlib import Path
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

load_dotenv()

os.environ["OPENAI_API_KEY"] = "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"

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# For Google Gemini, use:
# from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

ROOT_FOLDER = Path(__file__).parent.parent.absolute()
MCP_PATH = str(ROOT_FOLDER / "binance_mcp_ref" / "binace_file.py")
print(f"MCP Path: {MCP_PATH}")

mcp_config = {
    "binance": {
        "command": "python",
        "args": [MCP_PATH],
        "transport": "stdio",
    }
    # # npx NCP exmaple
    # ,"shopify": {
    #     "command": "npx",
    #     "args": ["-y", "@shopify/dev-mcp@latest"],
    #     "transport": "stdio",
    # },
}


async def get_crypto_prices():
    client = MultiServerMCPClient(mcp_config)
    async with client.session("binance") as session:
        tools = await client.get_tools()
        print(f"Available tools: {tools}")

        agent = create_react_agent(model, tools)

        query = "What are the current prices of Bitcoin and Ethereum?"
        message = HumanMessage(content=query)

        response = await agent.ainvoke({"messages": [message]})

        answer = response["messages"][-1].content

        return answer


if __name__ == "__main__":
    # Run the main async function
    response = asyncio.run(get_crypto_prices())
    print(response)