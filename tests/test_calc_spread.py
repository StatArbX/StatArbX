import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pandas as pd
from core.data_loader import download_data
from core.calc_spread import calculate_spread_and_thresholds

def test_spread_calculation():
    tickers = ['AAPL', 'MSFT']
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    # Load price data
    df = download_data(tickers, start_date, end_date)
    price_a = df['Adj Close']['AAPL']
    price_b = df['Adj Close']['MSFT']

    # Run spread calculation
    result = calculate_spread_and_thresholds(price_a, price_b)

    # Print results for inspection
    print("Beta:", result['beta'])
    print("Spread Mean:", result['mean'])
    print("Spread Std:", result['std'])
    print("Latest Z-score:", result['zscore'].iloc[-1])