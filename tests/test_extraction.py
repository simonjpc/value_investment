import pytest
import requests_mock
import requests
from valuation.extraction import get_income_stmt_info, get_balance_sheet_info, get_prices_in_range, get_current_price
from valuation.constants import API_BASE_PATH


class MockResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP error: {self.status_code}")

@pytest.mark.parametrize(
    "ticker, nb_years, api_response",
    [
        (None, None, "`ticker` attribute must be a string"),
        ("", None, "`nb_years` attribute must be an integer"),
    ]
)
def test_get_income_stmt_info_crash(ticker, nb_years, api_response, monkeypatch):
    with pytest.raises(AttributeError) as e:
        _ = get_income_stmt_info(ticker, nb_years)
    assert str(e.value) == api_response

    def mock_request_exception(*args, **kwargs):
        raise requests.exceptions.RequestException("Request error")
    monkeypatch.setattr(requests, "get", mock_request_exception)
    result = get_income_stmt_info("GM", 5)
    assert result == []

    def mock_json_decode_error(*args, **kwargs):
        return MockResponse(200, "invalid JSON")
    monkeypatch.setattr(requests, "get", mock_json_decode_error)
    result = get_income_stmt_info("GM", 5)
    assert result == "invalid JSON"

@pytest.mark.usefixtures("income_stmt_response_mock")
def test_get_income_stmt_info(income_stmt_response_mock):

    with requests_mock.Mocker() as mocker:
        ticker, years = "SSY", 3
        mocked_url = f"{API_BASE_PATH}/income-statement/{ticker}"
        mocker.get(mocked_url, json=income_stmt_response_mock, status_code=200)
        result = get_income_stmt_info(ticker=ticker, nb_years=years)
        assert result[:years] == income_stmt_response_mock[:years]
        assert len(result) <= years

        ticker = "FAKETICKR"
        mocked_url = f"{API_BASE_PATH}/income-statement/{ticker}"
        mocker.get(mocked_url, json=[], status_code=200)
        result = get_income_stmt_info(ticker=ticker, nb_years=years)
        assert result == []


@pytest.mark.parametrize(
    "ticker, nb_years, api_response",
    [
        (None, None, "`ticker` attribute must be a string"),
        ("", None, "`nb_years` attribute must be an integer"),
    ]
)
def test_get_balance_sheet_info_crash(ticker, nb_years, api_response, monkeypatch):
    with pytest.raises(TypeError) as e:
        _ = get_balance_sheet_info(ticker, nb_years)
    assert str(e.value) == api_response

    def mock_request_exception(*args, **kwargs):
        raise requests.exceptions.RequestException("Request error")
    monkeypatch.setattr(requests, "get", mock_request_exception)
    result = get_balance_sheet_info("GM", 5)
    assert result == []

    def mock_json_decode_error(*args, **kwargs):
        return MockResponse(200, "invalid JSON")
    monkeypatch.setattr(requests, "get", mock_json_decode_error)
    result = get_balance_sheet_info("GM", 5)
    assert result == "invalid JSON"

@pytest.mark.usefixtures("balance_sheet_response_mock")
def test_get_balance_sheet_info(balance_sheet_response_mock):

    with requests_mock.Mocker() as mocker:
        ticker, years = "SSY", 3
        mocked_url = f"{API_BASE_PATH}/balance-sheet-statement/{ticker}"
        mocker.get(mocked_url, json=balance_sheet_response_mock, status_code=200)
        result = get_balance_sheet_info(ticker=ticker, nb_years=years)
        assert result[:years] == balance_sheet_response_mock[:years]
        assert len(result) <= len(balance_sheet_response_mock)

        ticker = "FAKETICKR"
        mocked_url = f"{API_BASE_PATH}/balance-sheet-statement/{ticker}"
        mocker.get(mocked_url, json=[], status_code=200)
        result = get_balance_sheet_info(ticker=ticker, nb_years=years)
        assert result == []


@pytest.mark.parametrize(
    "ticker, window_start, window_end, prices",
    [
        (None, None, None, "all input attributes must be of type string"),
        ("", "", [], "all input attributes must be of type string"),
        ("SSY", "2020-02-01", "06-02-2020", "the format of attributes `window_start` and `window_end` must be YYYY-MM-DD"),
        ("SSY", "2020-02-06", "2020-02-01", "`window_start` must be earlier in time than `window_end`"),
    ]
)
def test_get_prices_in_range_crash(ticker, window_start, window_end, prices):
    with pytest.raises((AttributeError, TypeError)) as e:
        _ = get_prices_in_range(ticker=ticker, window_start=window_start, window_end=window_end)
    assert str(e.value) == prices

@pytest.mark.usefixtures("prices_in_range_mock")
def test_get_prices_in_range(prices_in_range_mock):

    with requests_mock.Mocker() as mocker:
        ticker, start, end = "SSY", "2020-02-01", "2020-02-06"
        mocked_url = f"{API_BASE_PATH}/historical-price-full/{ticker}"
        mocker.get(mocked_url, json=prices_in_range_mock, status_code=200)
        result = get_prices_in_range(ticker=ticker, window_start=start, window_end=end)
        assert result == prices_in_range_mock

        ticker = "FAKETICKR"
        mocked_url = f"{API_BASE_PATH}/historical-price-full/{ticker}"
        mocker.get(mocked_url, json={}, status_code=200)
        result = get_prices_in_range(ticker=ticker, window_start=start, window_end=end)
        assert result == {}

"""def get_current_price(ticker: str) -> float:
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
    
    return None"""

@pytest.mark.parametrize(
    "ticker, current_price",
    [
        (None, "`ticker` attribute must be a string"),
        ([], "`ticker` attribute must be a string"),
    ]
)
def test_get_current_price_crash(ticker, current_price):
    with pytest.raises(TypeError) as e:
        _ = get_current_price(ticker)
    assert str(e.value) == current_price

@pytest.mark.usefixtures("get_current_price_mock")
def test_get_current_price(get_current_price_mock):

    with requests_mock.Mocker() as mocker:
        ticker = "SSY"
        mocked_url = f"{API_BASE_PATH}/quote/{ticker}"
        mocker.get(mocked_url, json=get_current_price_mock, status_code=200)
        result = get_current_price(ticker)
        assert result == get_current_price_mock[0].get("price")

        ticker = "FAKETICKR"
        mocked_url = f"{API_BASE_PATH}/quote/{ticker}"
        mocker.get(mocked_url, json=[], status_code=200)
        result = get_current_price(ticker)
        assert result == None
