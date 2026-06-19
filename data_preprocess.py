from helper_funcs import fetch_symbol
import pandas as pd
import yfinance as yf

def fetch_data(company_name: str, period_months: int=None, start_date: str = None, end_date= None) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker and period in months.
    """
    try:
        start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
        end_date = pd.to_datetime(end_date, format="%Y-%m-%d")

        ticker = fetch_symbol(company_name)
        stock = yf.Ticker(ticker)

        if start_date and end_date:
            df = stock.history(start=start_date, end=end_date)
        elif period_months:
            df = stock.history(period=f"{period_months}mo")
        else:
            raise ValueError("You must provide either period_months or both start_date and end_date.")

        if df.empty:
            raise ValueError(f"No data returned for {ticker} with given parameters.")

        df.index = df.index.tz_localize(None)
        return df

    except Exception as e:
        raise RuntimeError(f"Failed to fetch data for {ticker}: {e}")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop unused columns and handle missing data (if any).
    """
    return df.drop(['Dividends', 'Stock Splits'], axis=1, errors='ignore')

def describe_data(df: pd.DataFrame) -> None:
    """
    Print basic statistics and missing value report for the DataFrame.
    """
    print("Column Data Types:\n", df.dtypes, "\n")
    print("Data Description:\n", df.describe(), "\n")
    print("Missing Values:\n", df.isna().sum(), "\n")
