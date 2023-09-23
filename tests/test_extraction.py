import pytest
import requests_mock
import requests
from valuation.extraction import get_income_stmt_info, get_balance_sheet_info
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
    try:
        _ = get_income_stmt_info(ticker, nb_years)
    except (AttributeError) as err:
        assert api_response == str(err)

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


"""
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
"""

@pytest.mark.parametrize(
    "ticker, nb_years, api_response",
    [
        (None, None, "`ticker` attribute must be a string"),
        ("", None, "`nb_years` attribute must be an integer"),
    ]
)
def test_get_balance_sheet_info_crash(ticker, nb_years, api_response, monkeypatch):
    try:
        _ = get_balance_sheet_info(ticker, nb_years)
    except (TypeError) as err:
        assert api_response == str(err)

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
