#!/usr/bin/env python
"""
Enhanced System Server — port 9881
Combines: Finance, WebTools, Auth, Data Sources
Reference: 2,434 files across 21 categories
"""
import os, sys, json
BASE = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal"
sys.path.insert(0, BASE)

# Import new modules
from finance_module import MarketData, PortfolioAnalyzer
from web_tools import WebTools
from auth_system import create_user, authenticate, create_token, validate_token

from fastmcp import FastMCP
import asyncio

mcp = FastMCP("Enhanced Server")

@mcp.tool()
def stock_quote(symbol: str = "AAPL"):
    """Get stock price from Yahoo Finance"""
    return MarketData.get_stock_quote(symbol)

@mcp.tool()
def crypto_price(name: str = "bitcoin"):
    """Get crypto price from CoinGecko"""
    return MarketData.get_crypto_price(name)

@mcp.tool()
def economic_data(indicator: str = "GDP"):
    """Get World Bank economic data"""
    return MarketData.get_economic_indicator(indicator)

@mcp.tool()
def web_search(query: str, limit: int = 5):
    """Search web via DuckDuckGo (free fallback)"""
    return WebTools.search_duckduckgo(query, limit)

@mcp.tool()
def fetch_page(url: str):
    """Fetch web page and extract text"""
    return WebTools.fetch_page_text(url)

@mcp.tool()
def portfolio_value(initial: float = 10000, annual_return: float = 0.1, years: int = 10):
    """Calculate future portfolio value"""
    return {
        "initial": initial,
        "annual_return": annual_return,
        "years": years,
        "final_value": round(PortfolioAnalyzer.portfolio_value(initial, annual_return, years), 2)
    }

@mcp.tool()
def list_capabilities():
    """List all capabilities of the Enhanced System"""
    return {
        "finance": ["stock_quote", "crypto_price", "economic_data", "portfolio_value"],
        "web": ["web_search", "fetch_page"],
        "sources": ["Yahoo Finance", "CoinGecko", "World Bank", "DuckDuckGo"],
        "based_on": "2,434 reference files across 21 categories"
    }

async def main():
    print("Enhanced Server: http://127.0.0.1:9881")
    print("Tools: stock_quote, crypto_price, economic_data, web_search, fetch_page, portfolio_value")
    await mcp.run_http_async(host="127.0.0.1", port=9881)

asyncio.run(main())
