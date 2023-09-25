import pytest
from valuation.utils import get_key_from_iterator
"""
def get_key_from_iterator(
    iterator: List[Dict[str, Any]], key: str,
) -> List[float]:
    return [element[key] for element in iterator]
"""

@pytest.mark.parametrize(
    "iterator, key, element",
    [
        (None, None, "`iterator` attribute must be a list of dictionaries"),
        ([], None, "`key` attribute must be a string"),
    ]
)
def test_get_key_from_iterator_crash(iterator, key, element):
    with pytest.raises(TypeError) as e:
        _ = get_key_from_iterator(iterator, key)
    assert str(e.value) == element

@pytest.mark.usefixtures("balance_sheet_data")
def test_get_key_from_iterator(balance_sheet_data):
    expected_output = [19120000, 20810000, 13743000]
    computed_output = get_key_from_iterator(balance_sheet_data, "totalStockholdersEquity")
    assert expected_output == computed_output

    expected_output = [None, None, None]
    computed_output = get_key_from_iterator(balance_sheet_data, "fake_key")
    assert expected_output == computed_output
