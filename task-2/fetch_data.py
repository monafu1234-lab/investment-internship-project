import pandas as pd
import yfinance as yf

start_date = "2016-11-01"
end_date = "2026-11-01"

for symbol in ["QQQ", "TQQQ"]:
    data = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        multi_level_index=False
    )

    if data.empty:
        raise ValueError("No data")

    print(data.head())

    data = data.reset_index()
    data = data.rename(columns={
        "Date": "date",
        "Open": "open",
        "Close": "close",
        "High": "high",
        "Low": "low",
        "Volume": "volume",
    })
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")
    data["date"] = data["date"].dt.strftime("%Y-%m-%d")
    data["symbol"] = symbol

    data = data[["symbol", "date", "open", "close", "high", "low", "volume"]]
    filename = f"{symbol.lower()}_prices.csv"
    data.to_csv(filename, index=False)

    saved_data = pd.read_csv(filename)

    if saved_data.empty:
        raise ValueError("Empty CSV")

    dates = pd.to_datetime(saved_data["date"])
    if not (
        (dates >= pd.Timestamp(start_date)) &
        (dates < pd.Timestamp(end_date))
    ).all():
        raise ValueError("Invalid dates")

    print(filename)
    print("Rows:", len(saved_data))
    print("First date:", saved_data["date"].min())
    print("Last date:", saved_data["date"].max())
    print("columns:", saved_data.columns.tolist())