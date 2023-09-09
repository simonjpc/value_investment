import os
from valuation.constants import API_BASE_PATH
from typing import List, Dict, Any, Tuple
import json
import requests
import pandas as pd

KEY = os.getenv("VALUATION_KEY")

def get_income_stmt_info(ticker: str, nb_years: int = 10) -> List[Dict[str, Any]]:
    url_income_stmt = f"{API_BASE_PATH}/income-statement/{ticker}"

    params = {
        "limit": nb_years,
        "apikey": KEY,
    }

    try:
        response = requests.get(url_income_stmt, params=params)
        response.raise_for_status()
        data_income_stmt = response.json()
        return data_income_stmt
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")

    return [] # Return an empty list if we fall in an exception

def get_balance_sheet_info(ticker: str, nb_years: int = 10) -> List[Dict[str, Any]]:
    url_balance_sheet = f"{API_BASE_PATH}/balance-sheet-statement/{ticker}"

    params ={
        "limit": nb_years,
        "apikey": KEY,
    }

    try:
        response = requests.get(url_balance_sheet, params=params)
        response.raise_for_status()
        data_balance_sheet = response.json()
        return data_balance_sheet
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")

    return [] # Return an empty list if we fall in an exception

def get_prices_in_range(ticker: str, window_start: str, window_end: str) -> List[Dict[str, Any]]:
    url_prices = f"{API_BASE_PATH}/historical-price-full/{ticker}"
    
    params = {
        "from": window_start,
        "to": window_end,
        "apikey": KEY,
    }
    
    try:
        response = requests.get(url_prices, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data_prices = response.json()
        return data_prices
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"JSON decoding error: {e}")
    
    return []  # Return an empty list if hitting an exception

def get_current_price(ticker: str) -> float:
    url_price = f"{API_BASE_PATH}/quote/{ticker}"
    
    params = {
        "limit": 1,
        "apikey": KEY
    }
    
    try:
        response = requests.get(url_price, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data_price = response.json()
        
        if data_price:
            return data_price[0]["price"]
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"JSON decoding error: {e}")
    
    return None

