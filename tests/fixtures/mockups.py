import pytest

@pytest.fixture
def fp_variables():
    """
    Input for function compute_fp
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
    """Input for function compute_pfv
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
    Input for function compute_pex_value_handler
    """
    return {
        "eps": 1.5,
        "growth_value": 0.20,
        "return_value": 0.15,
        "future_pe": 9,
        "years": 6,
        "pfv": 17.427,
    }

@pytest.fixture
def pex_variables():
    """
    Input for function compute_pex_value
    """
    return {
        "deco": {"eps": -1.5},
        "growth_value": 0.20,
        "return_value": 0.15,
        "future_pe": 9,
        "years": 6,
        "pfv": -17.427,
    }

@pytest.fixture
def tangible_bv_variables():
    """
    Input for function compute_tangible_book_value
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "tangible_bv": 3432000,
    }

@pytest.fixture
def compute_tangible_bvps():
    """
    Input for function compute_tangible_book_value_ps
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "weightedAverageShsOutDil": 3150000,
        "tangible_bv": 3432000,
        "tangible_bvps": 1.089,
    }

@pytest.fixture
def dct_tangible_bv_variables():
    """
    Input for function compute_discounted_tangible_book_value
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "netReceivables": 400000,
        "inventory": 200000,
        "propertyPlantEquipmentNet": 300000,
        "dct_tangible_bv": 3173000,
    }
        

@pytest.fixture
def compute_dct_tangible_bvps():
    """
    Input for function compute_discounted_tangible_book_value_ps
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "netReceivables": 400000,
        "inventory": 200000,
        "propertyPlantEquipmentNet": 300000,
        "weightedAverageShsOutDil": 3150000,
        "dct_tangible_bv": -1,
        "dct_tangible_bvps": 1.007,
    }

@pytest.fixture
def pe_ratio_variables():
    return {
        "reporting_date_price": 6.28,
        "eps": 1.77,
        "pe_ratio": 3.548,
    }
