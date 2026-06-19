from ticker import fetch_ticker
import pandas as pd
from typing import Optional

def fetch_symbol(company_name: str) -> str:
    """
    Returns the ticker symbol for a given company name.
    If the company_name already looks like a ticker, it's returned as-is.
    """
    if '.' in company_name:
        return company_name

    ticker = fetch_ticker(company_name)

    if not ticker or not isinstance(ticker, str):
        raise ValueError(f"Unable to resolve ticker for company: {company_name}")

    return ticker

def calculate_rsi(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Adds an RSI_10 column to the filtered DataFrame using EMA smoothing.
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")
    if 'Close' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'Close' column.")

    df = df.copy()
    period = 10

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index)

    if start_date:
        df = df[df.index >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df.index <= pd.to_datetime(end_date)]

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    df['RSI_10'] = 100 - (100 / (1 + rs))

    return df


def calculate_moving_average(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Adds a MA_10 column to the filtered DataFrame using a 10-day rolling window.
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty or None.")
    if 'Close' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'Close' column.")

    df = df.copy()
    window = 10

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index)

    if start_date:
        df = df[df.index >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df.index <= pd.to_datetime(end_date)]

    df["MA_10"] = df['Close'].rolling(window=window).mean()

    return df
