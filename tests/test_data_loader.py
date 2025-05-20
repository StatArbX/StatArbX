import pandas as pd
from core.data_loader import DataLoader


def test_load_tickers(tmp_path):
    # Create a temporary tickers.txt file
    test_file = tmp_path / "tickers.txt"
    test_file.write_text("AAPL\nMSFT\nGOOGL")

    # Initialize DataLoader with the temporary file
    loader = DataLoader(tickers_path=str(test_file))
    tickers = loader.load_tickers()

    assert isinstance(tickers, list)
    assert tickers == ["AAPL", "MSFT", "GOOGL"]


def test_download_data():
    tickers = ["AAPL", "MSFT"]
    loader = DataLoader()
    df = loader.download_data(tickers, start_date="2023-01-01", end_date="2023-01-15")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # Check for expected structure when multiple tickers
    assert isinstance(df.columns, pd.MultiIndex)
    assert "AAPL" in df.columns.levels[1]
    assert "Close" in df.columns.levels[0]
