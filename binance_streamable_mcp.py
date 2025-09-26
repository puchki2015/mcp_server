from mcp.server.fastmcp import FastMCP
import requests
from typing import Any


print("Starting Binance MCP server...")

my_mcp = FastMCP("BINANCE_MCP",port=8897)

def get_symbol_from_name(name: str) -> str:
    if name.lower() in ["bitcoin", "btc"]:
        return "BTCUSDT"
    elif name.lower() in ["ethereum", "eth"]:
        return "ETHUSDT"
    else:
        return name.upper()

@my_mcp.tool()    
def get_price(symbol: str) -> Any:
    """Fetches the current price of a cryptocurrency from Binance.
    Args:
        symbol (str): The symbol of the cryptocurrency (e.g., 'BTCUSDT').
    Returns:
        Any: The current price data from Binance API.
        """
    symbol = get_symbol_from_name(symbol)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
            

if __name__ == "__main__":
    # Access the MCP server on stdio protocol
    print("Running Binance MCP server...")
    #my_mcp.run(transport="stdio")

    # Access the MCP server on SSE protocol through <<server_url>>/sse
    my_mcp.run(transport="sse")

    # Access the MCP server via streming protocol through <<server_url>>/streamable-http
    #my_mcp.run(transport="streamable-http")

    #### You can run by using the command below uv run binance_streamable.py

    ### in a different terminal run "npx @modelcontextprotocol/inspector"

    ### when the mcp inspector is accessible, select transport as "streamable-http" and enter the url
    #  as "http://localhost:8897/mcp"

    #Now for production deployement in the cloud, change it to transport="sse"


    ### use render.com for production deployment


    #########################IMPORTANT###############################

    ###render.com takes the code from github and deploy it,,,,so need to create a github repo 
    #"https://github.com/puchki2015/mcp_server"

    #Deploy webservice