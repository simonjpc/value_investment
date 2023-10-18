import pandas as pd
from typing import List

class DataLoader():

    def __init__(self):
        pass
    
    @staticmethod
    def load_tickers_from_txt(path: str, mode: str = "r") -> List[str]:
        if path[-3:] != "txt":
            raise ValueError("`path` attribute must be a .txt file")
        with open(path, mode) as f:
            tickers = f.read()
        tickers = tickers.split("\n")
        return tickers
