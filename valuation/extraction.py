import os
from valuation.constants import API_BASE_PATH
from typing import List, Dict, Any, Tuple
import json
import requests
import pandas as pd

KEY = os.environ.get("VALUATION_KEY")

def get_income_stmt_info(ticker: str, period: str, limit: int = 10) -> List[Dict[str, Any]]:
    if not isinstance(ticker, str):
        raise AttributeError("`ticker` attribute must be a string")
    if not isinstance(limit, int):
        raise AttributeError("`limit` attribute must be an integer")

    url_income_stmt = f"{API_BASE_PATH}/income-statement/{ticker}"

    params = {
        "limit": limit,
        "apikey": KEY,
        "period": period,
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

def get_balance_sheet_info(ticker: str, period: str, limit: int = 10) -> List[Dict[str, Any]]:
    if not isinstance(ticker, str):
        raise TypeError("`ticker` attribute must be a string")
    if not isinstance(limit, int):
        raise TypeError("`nb_years` attribute must be an integer")
        
    url_balance_sheet = f"{API_BASE_PATH}/balance-sheet-statement/{ticker}"

    params ={
        "limit": limit,
        "apikey": KEY,
        "period": period,
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

def get_prices_in_range(ticker: str, window_start: str, window_end: str) -> Dict[str, Any]:
    if not all([isinstance(var, str) for var in (ticker, window_start, window_end)]):
        raise AttributeError("all input attributes must be of type string")

    for element in (window_start, window_end):
        try:
            year, month, day = element.split("-")
        except:
            raise TypeError("the format of attributes `window_start` and `window_end` must be YYYY-MM-DD")

        if not (len(year) == 4 and len(month) == 2 and len(day) == 2):
            raise TypeError(
                "the format of attributes `window_start` and `window_end` must be YYYY-MM-DD"
            )
        elif int(month) > 12 or int(day) > 31:
            raise TypeError(
                "the format of attributes `window_start` and `window_end` must be YYYY-MM-DD"
            )
        elif pd.to_datetime(window_start) > pd.to_datetime(window_end):
            raise TypeError("`window_start` must be earlier in time than `window_end`")


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
    
    return {}  # Return an empty list if hitting an exception

def get_current_price(ticker: str) -> float:
    if not isinstance(ticker, str):
        raise TypeError("`ticker` attribute must be a string")
    url_price = f"{API_BASE_PATH}/quote/{ticker}"
    
    params = {
        "limit": 1,
        "apikey": KEY,
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
