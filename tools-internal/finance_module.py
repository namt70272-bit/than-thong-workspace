#!/usr/bin/env python
"""
Finance Module — Market data + analysis
Reference: finance/ (qlib_service, skfolio, bt_provider, fincept patterns)
"""
import os, sys, json, httpx, time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal")
REF = BASE / "reference-library" / "finance"

class MarketData:
    """Fetch market data from free APIs (no API key needed)"""
    
    @staticmethod
    def get_stock_quote(symbol):
        """Get stock quote from Yahoo Finance (no API key)"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            data = r.json()
            result = data.get("chart", {}).get("result", [{}])[0]
            meta = result.get("meta", {})
            return {
                "symbol": symbol,
                "price": meta.get("regularMarketPrice"),
                "previous_close": meta.get("previousClose"),
                "change": meta.get("regularMarketPrice", 0) - meta.get("previousClose", 0) if meta.get("regularMarketPrice") else None,
                "currency": meta.get("currency"),
                "exchange": meta.get("exchangeName"),
            }
        except Exception as e:
            return {"error": str(e)[:80]}
    
    @staticmethod
    def get_crypto_price(symbol="bitcoin"):
        """Get crypto price from CoinGecko (free)"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
            r = httpx.get(url, timeout=10)
            data = r.json()
            price = data.get(symbol, {}).get("usd")
            return {"symbol": symbol, "price_usd": price}
        except Exception as e:
            return {"error": str(e)[:80]}
    
    @staticmethod
    def get_economic_indicator(indicator="GDP"):
        """Get economic data from World Bank API (free)"""
        endpoints = {
            "GDP": "NY.GDP.MKTP.CD",
            "GDP_PER_CAPITA": "NY.GDP.PCAP.CD",
            "INFLATION": "FP.CPI.TOTL.ZG",
            "UNEMPLOYMENT": "SL.UEM.TOTL.ZS",
            "POPULATION": "SP.POP.TOTL",
        }
        code = endpoints.get(indicator, "NY.GDP.MKTP.CD")
        try:
            url = f"https://api.worldbank.org/v2/country/US/indicator/{code}?format=json"
            r = httpx.get(url, timeout=10)
            data = r.json()
            if len(data) > 1:
                values = [(item["date"], item["value"]) for item in data[1][:5] if item.get("value")]
                return {"indicator": indicator, "data": values}
            return {"error": "No data"}
        except Exception as e:
            return {"error": str(e)[:80]}

class PortfolioAnalyzer:
    """Simple portfolio analysis (from skfolio/core patterns)"""
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free=0.02):
        if not returns:
            return 0
        avg_return = sum(returns) / len(returns)
        std = (sum((r - avg_return)**2 for r in returns) / len(returns))**0.5
        if std == 0:
            return 0
        return (avg_return - risk_free/252) / std * (252**0.5)
    
    @staticmethod
    def portfolio_value(initial, annual_return, years):
        return initial * (1 + annual_return) ** years

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "test"
    
    if action == "stock":
        s = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
        print(json.dumps(MarketData.get_stock_quote(s), indent=2))
    elif action == "crypto":
        s = sys.argv[2] if len(sys.argv) > 2 else "bitcoin"
        print(json.dumps(MarketData.get_crypto_price(s), indent=2))
    elif action == "econ":
        ind = sys.argv[2] if len(sys.argv) > 2 else "GDP"
        print(json.dumps(MarketData.get_economic_indicator(ind), indent=2))
    else:
        print("Finance Module")
        print("  stock  <symbol>  - Stock quote (AAPL, MSFT)")
        print("  crypto <name>    - Crypto price (bitcoin, ethereum)")
        print("  econ   <ind>     - Economic indicator (GDP, INFLATION)")
