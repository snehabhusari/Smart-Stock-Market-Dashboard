from helper_funcs import calculate_rsi, calculate_moving_average
from datetime import datetime 
from data_preprocess import fetch_data, clean_data
import viz
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

def run_analysis(company_name, date_mode, months=None, start_date=None, end_date=None, plot_type=None):
    # --- single company pipeline ---
    if date_mode == "Relative Period":
        df = fetch_data(company_name, period_months=int(months))
    else:
        df = fetch_data(company_name, start_date=start_date, end_date=end_date)
    df = clean_data(df)
    df = calculate_rsi(df)
    df = calculate_moving_average(df)

    if plot_type == "Price Only":
        fig = viz.plot_price(df)
    elif plot_type == "Price + MA":
        fig = viz.plot_price_ma(df)
    elif plot_type == "RSI Only":
        fig = viz.plot_rsi(df)
    else:
        fig = viz.plot_combined(df)

    summary = df[["Close", "RSI_10", "MA_10"]].tail(5)
    return fig, summary

def run_analysis_simple(df, analysis_type="RSI Only"):
    # --- simple plotting helper ---
    fig, ax = plt.subplots()
    ax.plot(df['Close'], label="Close Price")
    ax.plot(df['RSI_10'], label="RSI")
    ax.plot(df['MA_10'], label="MA")
    ax.legend()
    return fig, df

def run_analysis_multi(companies, date_mode, months=None, start_date=None, end_date=None, plot_type=None):
    # --- multi-company portfolio analysis ---
    all_data = []
    fig, ax = plt.subplots(figsize=(10,6))

    for ticker in companies:
        if date_mode == "Relative Period":
            df = fetch_data(ticker, period_months=int(months))
        else:
            df = fetch_data(ticker, start_date=start_date, end_date=end_date)

        df = clean_data(df)
        df = calculate_rsi(df)
        df = calculate_moving_average(df)
        df["Company"] = ticker

        all_data.append(df)

        ax.plot(df.index, df["Close"], label=f"{ticker} Close")
        if "MA" in plot_type:
            ax.plot(df.index, df["MA_10"], linestyle="--", label=f"{ticker} MA_10")

    ax.set_title("Portfolio Price Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()

    combined_df = pd.concat(all_data)
    summary = combined_df[["Company","Close","RSI_10","MA_10"]].tail(10)

    return fig, summary

# --- unified wrapper for Gradio ---
def run_analysis_wrapper(company_name, date_mode, months=None, start_date=None, end_date=None, plot_type=None):
    """
    Wrapper function that decides whether to call single-company or multi-company analysis.
    Gradio Dropdown with multiselect=True will pass a list when multiple tickers are chosen.
    """
    if isinstance(company_name, list):  # multiple tickers selected
        return run_analysis_multi(company_name, date_mode, months, start_date, end_date, plot_type)
    else:  # single ticker
        return run_analysis(company_name, date_mode, months, start_date, end_date, plot_type)
