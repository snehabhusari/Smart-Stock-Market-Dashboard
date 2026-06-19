from helper_funcs import calculate_rsi, calculate_moving_average
from datetime import datetime
from data_preprocess import fetch_data, clean_data
import viz

def run_analysis(company_name, date_mode, months=None, start_date=None, end_date=None, plot_type=None):
    """
    Complete data pipeline that:
    - Fetches stock data via yfinance
    - Computes indicators (MA, RSI)
    - Chooses plot type
    - Returns plot + summary table
    """
    if date_mode == "Relative Period":
        df = fetch_data(company_name, period_months=int(months))
    else:
        df = fetch_data(company_name, start_date=start_date, end_date=end_date)
    # Remove cols
    df = clean_data(df)

    # Compute indicators
    df = calculate_rsi(df)
    df = calculate_moving_average(df)

    # Plot based on selection
    if plot_type == "Price Only":
        fig = viz.plot_price(df)
    elif plot_type == "Price + MA":
        fig = viz.plot_price_ma(df)
    elif plot_type == "RSI Only":
        fig = viz.plot_rsi(df)
    else:
        fig = viz.plot_combined(df)

    # Return chart and summary
    summary = df[["Close", "RSI_10", "MA_10"]].tail(5)
    return fig, summary