import pytest
import requests_mock
import requests
from valuation.extraction import get_income_stmt_info
from valuation.constants import API_BASE_PATH

# Mock the requests library to simulate API responses
class MockResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP error: {self.status_code}")

@pytest.fixture
def mock_requests_get(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(200, {"key": "value"})

    monkeypatch.setattr(requests, "get", mock_get)
    
@pytest.mark.parametrize(
    "ticker, nb_years, api_response",
    [
        (None, None, "`ticker` attribute must be a string"),
        ("", None, "`nb_years` attribute must be an integer"),
    ]
)
def test_get_income_stmt_info_crash(ticker, nb_years, api_response):
    try:
        _ = get_income_stmt_info(ticker, nb_years)
    except (AttributeError) as err:
        assert api_response == str(err)

def test_request_exception(monkeypatch):

    def mock_request_exception(*args, **kwargs):
        raise requests.exceptions.RequestException("Request error")

    monkeypatch.setattr(requests, "get", mock_request_exception)

    result = get_income_stmt_info("AAPL", 5)
    assert result == []

def test_json_decode_error(monkeypatch):
    # Test when a JSON decoding error occurs
    def mock_json_decode_error(*args, **kwargs):
        return MockResponse(200, "invalid JSON")

    monkeypatch.setattr(requests, "get", mock_json_decode_error)

    #with pytest.raises(json.JSONDecodeError):
    result = get_income_stmt_info("AAPL", 5)
    assert result == "invalid JSON"

@pytest.mark.usefixtures("income_stmt_response_mock")
def test_get_income_stmt_info(income_stmt_response_mock):

    with requests_mock.Mocker() as mocker:
        ticker, years = "SSY", 3
        mocked_url = f"{API_BASE_PATH}/income-statement/{ticker}"
        mocker.get(mocked_url, json=income_stmt_response_mock, status_code=200)
        output = get_income_stmt_info(ticker=ticker, nb_years=years)
        assert output[:years] == income_stmt_response_mock[:years]
        assert len(output) <= years

        ticker = "FAKETICKR"
        mocked_url = f"{API_BASE_PATH}/income-statement/{ticker}"
        mocker.get(mocked_url, json=[], status_code=200)
        output = get_income_stmt_info(ticker=ticker, nb_years=years)
        assert output == []
