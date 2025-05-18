import pandas as pd
import matplotlib.pyplot as plt
from core.data_loader import load_tickers, download_data
from core.calc_spread import calculate_spread_and_thresholds
from core.pair_selector import select_pairs

def plot_trades(price_a: pd.Series, price_b: pd.Series, entry_z: float = 2.0, exit_z: float = 0.0):
    result = calculate_spread_and_thresholds(price_a, price_b)
    zscore = result["zscore"]

    position = 0
    entry_dates = []
    exit_dates = []
    trade_log = []

    for date in zscore.index:
        z = zscore.loc[date]
        pa = price_a.loc[date]
        pb = price_b.loc[date]
        if position == 0:
            if z > entry_z or z < -entry_z:
                position = 1 if z < -entry_z else -1
                entry_type = "Long A, Short B" if position == 1 else "Short A, Long B"
                entry_dates.append(date)
                trade_log.append({
                    "Date": date,
                    "Type": "Entry",
                    "Z-Score": round(z, 2),
                    "Price A": round(pa, 2),
                    "Price B": round(pb, 2),
                    "Position": entry_type
                })
        elif (position == -1 and z < exit_z) or (position == 1 and z > exit_z):
            exit_dates.append(date)
            exit_type = "Exit Short" if position == -1 else "Exit Long"
            trade_log.append({
                "Date": date,
                "Type": "Exit",
                "Z-Score": round(z, 2),
                "Price A": round(pa, 2),
                "Price B": round(pb, 2),
                "Position": exit_type
            })
            position = 0

    # --- Show Trade Log ---
    trade_df = pd.DataFrame(trade_log)
    print("\nTrade Log:")
    print(trade_df.to_string(index=False))

    # --- Plot 1: Z-Score with Trade Markers ---
    plt.figure(figsize=(14, 6))
    plt.plot(zscore, label="Z-Score", color="black")
    plt.axhline(entry_z, color="red", linestyle="--", label="+ Entry Threshold")
    plt.axhline(-entry_z, color="green", linestyle="--", label="- Entry Threshold")
    plt.axhline(exit_z, color="gray", linestyle="--", label="Exit Threshold")

    for i, date in enumerate(entry_dates):
        plt.axvline(date, color="blue", linestyle=":", alpha=0.6, label="Entry" if i == 0 else "")
    for i, date in enumerate(exit_dates):
        plt.axvline(date, color="orange", linestyle=":", alpha=0.6, label="Exit" if i == 0 else "")

    plt.title("Z-Score of Spread: Trade Entry/Exit Visualization")
    plt.xlabel("Date")
    plt.ylabel("Z-Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Plot 2: Price Series with Trade Markers ---
    plt.figure(figsize=(14, 6))
    plt.plot(price_a, label=price_a.name or "Asset A", color="purple")
    plt.plot(price_b, label=price_b.name or "Asset B", color="teal")

    for i, date in enumerate(entry_dates):
        plt.axvline(date, color="blue", linestyle="--", alpha=0.5, label="Entry" if i == 0 else "")
    for i, date in enumerate(exit_dates):
        plt.axvline(date, color="orange", linestyle="--", alpha=0.5, label="Exit" if i == 0 else "")

    plt.title("Price Series with Trade Points")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    tickers = load_tickers()
    df = download_data(tickers, "2022-01-01", "2024-01-01")
    price_a = df["Adj Close"]["MA"]
    price_b = df["Adj Close"]["V"]
    
    plot_trades(price_a, price_b, entry_z=2.0, exit_z=0.0)

