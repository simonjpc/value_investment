import pytest

@pytest.fixture
def fp_variables():
    """
    Input structure for filters
    """
    return {
        "eps": 1.5,
        "growth_value": 0.20,
        "years": 7,
        "future_pe": 9,
        "fp": 48.373,
    }
