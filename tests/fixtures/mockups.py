import pytest

@pytest.fixture
def fp_variables():
    """
    Input structure function compute_fp
    """
    return {
        "eps": 1.5,
        "growth_value": 0.20,
        "years": 7,
        "future_pe": 9,
        "fp": 48.373,
    }

@pytest.fixture
def pfv_variables():
    """Input structure function compute_pfv
    """
    return {
        "fp": 3.21, 
        "return_value": 0.15,
        "pfv": 1.387,
        "years": 6,
    }

@pytest.fixture
def pex_handler_variables():
    """
    Input structure function compute_fp
    """
    return {
        "eps": 1.5,
        "growth_value": 0.20,
        "return_value": 0.15,
        "future_pe": 9,
        "years": 6,
        "pfv": 17.427,
    }
