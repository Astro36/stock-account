import re
from datetime import date, timedelta
from typing import Iterable

import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def convert_to_yfinance_symbol(symbol: str) -> str:
    """Convert a stock symbol to a symbol used by Yahoo Finance.

    Args:
        symbol (str): The stock symbol.

    Returns:
        str: The corresponding Yahoo Finance symbol.
    """
    if re.match(r"^A\d{6}$", symbol):
        symbol = symbol[1:]
    r = requests.get(
        f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        },
    )
    yfinance_symbol: str = sorted(
        filter(lambda x: x["symbol"].startswith(symbol), r.json()["quotes"]),
        key=lambda x: len(x["symbol"]),
    )[0]["symbol"]
    return yfinance_symbol


def create_headless_edge_webdriver() -> webdriver.Remote:
    """Create a headless Edge webdriver instance.

    Returns:
        webdriver.Remote: A headless Edge webdriver instance.
    """
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Edge(options=options, service=Service(EdgeChromiumDriverManager().install()))
    return driver


def daterange(start_date: date, end_date: date) -> Iterable[date]:
    """Generate all dates between start_date and end_date (inclusive).

    Args:
        start_date (date): The starting date.
        end_date (date): The ending date.

    Yields:
        date: Each date in the range.
    """
    while start_date < end_date:
        yield start_date
        start_date += timedelta(days=1)
    yield end_date


def weekrange(start_date: date, end_date: date) -> Iterable[tuple[date, date]]:
    """Generate all week ranges between start_date and end_date (inclusive).

    Args:
        start_date (date): The starting date.
        end_date (date): The ending date.

    Yields:
        tuple[date, date]: Each week range in the range.
    """
    s = start_date
    e = start_date + timedelta(days=6 - start_date.weekday())
    while e <= end_date:
        yield (s, e)
        s = e + timedelta(days=1)
        e = s + timedelta(days=6)
    yield (s, end_date)
