import matplotlib.pyplot as plt
import pandas as pd

def plot_price(df:pd.DataFrame):
    
    df = df.reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Date"], df["Close"], label="Close", color="blue")
    ax.set_title("Stock Price")
    ax.grid(True)
    ax.legend()
    return fig

def plot_price_ma(df: pd.DataFrame):
    
    df = df.reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Date"], df["Close"], label="Close", color="blue")
    ax.plot(df["Date"], df["MA_10"], label="MA 10", color="orange")
    ax.set_title("Stock Price with Moving Average")
    ax.grid(True)
    ax.legend()
    return fig

def plot_rsi(df: pd.DataFrame, rsi_column="RSI_10"):
    
    df = df.reset_index()

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df["Date"], df[rsi_column], label=rsi_column, color="purple")
    ax.axhline(70, color="red", linestyle="--", lw=1)
    ax.axhline(30, color="green", linestyle="--", lw=1)
    ax.set_title("RSI Indicator")
    ax.grid(True)
    ax.legend()
    return fig

def plot_combined(df: pd.DataFrame, rsi_column="RSI_10"):
    
    df = df.reset_index()

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axs[0].plot(df["Date"], df["Close"], label="Close", color="blue")
    axs[0].plot(df["Date"], df["MA_10"], label="MA 10", color="orange")
    axs[0].set_title("Stock Price with MA")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(df["Date"], df[rsi_column], label=rsi_column, color="purple")
    axs[1].axhline(70, color="red", linestyle="--", lw=1)
    axs[1].axhline(30, color="green", linestyle="--", lw=1)
    axs[1].set_title("RSI Indicator")
    axs[1].grid(True)
    axs[1].legend()

    fig.tight_layout()
    return fig
