import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from typing import Union
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def read_stocks_from_csv(filename: str) -> pd.DataFrame:
    try:
        stocks_df = pd.read_csv(filename)
        logging.info(f"Successfully read data from {filename}")
        return stocks_df
    except Exception as e:
        logging.error(f"Error reading CSV file {filename}: {str(e)}")
        return pd.DataFrame()


def convert_value(value):
    """Convert string values to float, handling commas and suffixes (K, M, B)"""
    if pd.isna(value):  # Add check for NaN values
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
    
    # Remove any % signs
    value = str(value).replace('%', '')
    
    # Handle numbers with commas
    value = value.replace(',', '')
    
    # Handle K/M/B suffixes
    if value.endswith('K'):
        return float(value[:-1]) * 1_000
    elif value.endswith('M'):
        return float(value[:-1]) * 1_000_000
    elif value.endswith('B'):
        return float(value[:-1]) * 1_000_000_000
    
    try:
        return float(value)
    except ValueError:  # Add error handling for invalid conversions
        return 0.0


def get_background_image(ticker: str) -> Union[Image.Image, None]:
    """Try to load the background original image for a ticker"""
    image_path = f"assets/images/{ticker}_original_img.png"
    try:
        if os.path.exists(image_path):
            return Image.open(image_path)
        return None
    except Exception as e:
        logging.error(f"Error loading background image for {ticker}: {str(e)}")
        return None


def create_graph_from_single_ticker(row):
    # Get background image if available
    background = get_background_image(row['Ticker'])
    
    # Create figure with or without background
    fig = plt.figure(figsize=(16, 8))
    
    if background:
        # Add background as the first axes covering the entire figure
        background_ax = plt.axes([0, 0, 1, 1])
        background_ax.imshow(np.array(background), aspect='auto', alpha=0.3)
        background_ax.axis('off')  # Hide the axes
    
    # Continue with existing gridspec and plotting
    gs = fig.add_gridspec(1, 5, left=0.1, right=0.9, top=0.8, bottom=0.2, wspace=0.9)
    
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    ax4 = fig.add_subplot(gs[3])
    ax5 = fig.add_subplot(gs[4])
    
    bar_width = 0.3
    
    # 1. Price Bar
    price = convert_value(row['Price'])
    channel_range = convert_value(row['channel_range'])
    support = convert_value(row['support'])
    resistance = convert_value(row['resistance'])
    
    # Calculate drawdown price
    max_drawdown_pct = convert_value(row['max_drawdown_%'])
    drawdown_price = price * (1 + max_drawdown_pct / 100)
    
    # Calculate percentages
    channel_ratio = convert_value(row['current_price_ratio_channel']) * 100
    support_ratio = convert_value(row['current_price_ratio_support']) * 100
    potential_profit = convert_value(row["potential_profit_%"]) * 100
    
    # Determine the bottom of the bar as the minimum of support and price
    bottom_price_bar = min(drawdown_price, support)
    top_price_bar = max(drawdown_price, support)

    ax1.bar(0, price - support, bottom=support, width=bar_width, color='blue')
    ax1.bar(0, resistance - price, bottom=price, width=bar_width, color='lightgray', alpha=0.3)
    ax1.bar(0, top_price_bar - bottom_price_bar, bottom=bottom_price_bar, width=bar_width, color='lightgray', alpha=0.3)
    
    # Add cut lines and labels for price values
    values_labels = [
        (price, f'Price: {price:.2f}'),
        (support, f'Support: {support:.2f}'),
        (resistance, f'Resistance: {resistance:.2f}'),
        (drawdown_price, f'Drawdown Price \n(365d): {drawdown_price:.2f}')
    ]
    
    for value, label in values_labels:
        ax1.hlines(y=value, xmin=-0.25, xmax=0.25, color='gray', linestyles='--', linewidth=1)
        ax1.text(-0.25, value, label, ha='right', va='center')
    
    # Add price tooltip with percentages
    ax1.annotate(f'Price: {price:.2f}\n'
                 f'Range: {channel_range:.2f}\n'
                 f'% Potential: {potential_profit:.1f}%\n'
                 f'% Channel: {channel_ratio:.1f}%\n'
                 f'% Support: {support_ratio:.1f}%',
                 xy=(0, price), xytext=(10, 0),
                 textcoords='offset points',
                 ha='left', va='center',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
    
    ax1.set_title('Price')

    # 2. Volume Bar
    volume = convert_value(row['Volume'])
    avg_volume = convert_value(row['Avg Volume'])
    rel_volume = convert_value(row['Rel Volume'])
    avg_time_based = volume / rel_volume  # Calculate time-based average
    
    ax2.bar(0, volume, width=bar_width, color='green')
    ax2.bar(0, max(0, avg_time_based - volume), bottom=volume, width=bar_width, color='lightgray', alpha=0.3)
    
    # Add cut lines and labels for volume values
    for value, label in [(volume, 'Vol:'), (avg_time_based, 'Avg (Time based):\n')]:
        ax2.hlines(y=value, xmin=-0.25, xmax=0.25, color='gray', linestyles='--', linewidth=1)
        ax2.text(-0.25, value, f'{label} {value:,.0f}', ha='right', va='center')
    
    # Move tooltip to avg_time_based instead of volume
    ax2.annotate(f'Avg Volume: {avg_volume:,.0f}\n'
                 f'Rel Volume: {rel_volume:,.2f}',
                 xy=(0, avg_time_based), xytext=(10, 0),
                 textcoords='offset points',
                 ha='left', va='center',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
    
    ax2.set_title('Volume')

    # 3. RSI Bar
    rsi = convert_value(row['rsi_14'])
    ax3.bar(0, rsi, width=bar_width, color='orange')
    ax3.bar(0, 100 - rsi, bottom=rsi, width=bar_width, color='lightgray', alpha=0.3)
    
    # Add cut lines and labels for RSI values
    for value, label, color in [(rsi, 'RSI', 'gray'), (30, '30', 'green'), (70, '70', 'red')]:
        ax3.hlines(y=value, xmin=-0.25, xmax=0.25, color=color, linestyles='--', linewidth=1)
        if value == rsi:
            ax3.text(-0.25, value, f'{label}: {value:.1f}', ha='right', va='center')
        else:
            ax3.text(-0.25, value, str(value), ha='right', va='center')
    
    ax3.set_ylim(0, 100)
    ax3.set_title('RSI')

    # 4. SMA Bar
    sma20 = convert_value(row['sma_short_20'])
    sma50 = convert_value(row['sma_long_50'])
    price = convert_value(row['Price'])
    
    # Add safety checks for SMA values
    if all(v > 0 for v in [sma20, sma50, price]):  # Only draw if all values are valid
        max_sma = max(sma20, sma50, price)
        min_sma = min(sma20, sma50, price)
        
        # Calculate the difference between SMAs
        sma_diff = abs(sma20 - sma50)
        sma_avg = (sma20 + sma50) / 2
        
        # Adjust padding based on the difference between values
        if sma_diff / sma_avg < 0.01:  # If difference is less than 1%
            padding = sma_diff * 2
        else:
            padding = sma_diff * 0.5
        
        # Draw the main bar up to SMA20 (solid purple)
        ax4.bar(0, sma20 - (min_sma - padding), bottom=(min_sma - padding), width=bar_width, color='purple')
        
        # Draw the remaining part (transparent)
        ax4.bar(0, (max_sma + padding) - sma20, bottom=sma20, width=bar_width, color='lightgray', alpha=0.3)
        
        # Add cut lines and labels for SMA values
        for value, label in [(sma20, f'SMA20: {sma20:.2f}'), (sma50, f'SMA50: {sma50:.2f}'), (price, f'Price: {price:.2f}')]:
            ax4.hlines(y=value, xmin=-0.25, xmax=0.25, color='gray', linestyles='--', linewidth=1)
            ax4.text(-0.25, value, label, ha='right', va='center')
        
        ax4.set_ylim(min_sma - padding, max_sma + padding)
    else:
        # If values are invalid, draw an empty bar
        ax4.bar(0, 100, width=bar_width, color='lightgray', alpha=0.3)
        ax4.text(0, 50, 'No SMA Data', ha='center', va='center')
        ax4.set_ylim(0, 100)

    ax4.set_title('SMA')

    # 5. Past Trend Bar
    last_resistance = convert_value(row['last_up_trade_resistence_price'])
    last_support = convert_value(row['last_up_trade_support_price'])
    current_price = convert_value(row['Price'])
    range_value = convert_value(row['last_up_trade_range'])
    days = convert_value(row['last_up_trade_days'])
    avg_days = convert_value(row['last_up_trade_avg_days'])

    # Find min and max for y-axis limits
    min_value = min(last_support, current_price)
    max_value = max(last_resistance, current_price)
    padding = (max_value - min_value) * 0.07

    # Draw the main bar up to current price
    ax5.bar(0, current_price - last_support, bottom=last_support, width=bar_width, color='yellow')
    ax5.bar(0, last_resistance - current_price, bottom=current_price, width=bar_width, color='lightgray', alpha=0.3)
    
    # Add cut lines and labels
    values_labels = [
        (last_resistance, f"Last Resistance:\n{row['last_up_trade_resistence_date']} - {last_resistance:.2f}"),
        (last_support, f"Last Support:\n{row['last_up_trade_support_date']} - {last_support:.2f}"),
    ]

    # Add labels on the left side
    for value, label in values_labels:
        ax5.hlines(y=value, xmin=-0.25, xmax=0.25, color='gray', linestyles='--', linewidth=1)
        ax5.text(-0.25, value, label, ha='right', va='center')

    # Add current price label on the right side
    ax5.text(0.25, current_price, f"Price: {current_price:.2f}", ha='left', va='center')
    ax5.hlines(y=current_price, xmin=-0.25, xmax=0.25, color='gray', linestyles='--', linewidth=1)

    # Add tooltip
    ax5.annotate(f'Range: {range_value:.2f}\n'
                 f'Days: {days:.0f}\n'
                 f'Avg Days (all rising): {avg_days:.1f}',
                 xy=(0, last_resistance), xytext=(10, 0),
                 textcoords='offset points',
                 ha='left', va='center',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

    ax5.set_ylim(min_value, max_value + padding)
    ax5.set_title('Past Trend')

    # Remove all axis numbers and ticks
    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    # Add ticker name at top left
    current_datetime = datetime.now().strftime('%Y-%m-%d')
    plt.figtext(0.02, 0.97, f"{row['Ticker']} - {current_datetime}", fontsize=20, weight='bold')
    
    # Calculate investment metrics
    price = convert_value(row['Price'])
    shares = int(1000/price)  # rounddown by using int()
    total_investment = price * shares
    potential_profit_pct = convert_value(row['potential_profit_%'])
    future_portfolio = total_investment * (1 + potential_profit_pct)
    profit = future_portfolio - total_investment
    days_to_hold = int(convert_value(row['last_up_trade_days']))
    target_date = (datetime.now() + pd.Timedelta(days=days_to_hold)).strftime('%Y-%m-%d')

    # Add investment projection text
    investment_projection = (
        f"Entry now with 1000$, buy {shares} shares "
        f"(Total: ${total_investment:.2f}), based on past trend, "
        f"you will hold portfolio of ${future_portfolio:.2f} "
        f"(Earning: ${profit:.2f}) until {target_date} "
        f"({days_to_hold} trading days from today)"
    )

    plt.figtext(0.02, 0.96, investment_projection, 
                ha='left', va='top', fontsize=10)

    # Calculate backtest metrics and add them below
    historical_metrics = (
        f"Backtest (365d), " +
        f"Entry: $1000 | " +
        f"Strategy: SMA20 > SMA50 & RSI < 70 | " +
        f"Return %: {convert_value(row['return_%']):.1f}% | " +
        f"Max Drawdown %: {convert_value(row['max_drawdown_%']):.1f}% | " +
        f"Sharpe Ratio: {convert_value(row['sharpe_ratio']):.2f}"
    )
    
    # Add metrics text at left side, below ticker
    plt.figtext(0.02, 0.935, historical_metrics, 
                ha='left', va='top', fontsize=10)
    
    # Add Earnings value on next line
    earnings_value = row['Earnings']
    plt.figtext(0.02, 0.91, f"Quarterly report: {earnings_value}",
                ha='left', va='top', fontsize=10)

    plt.savefig(f"assets/output/{row['Ticker']}_chart.png", bbox_inches='tight', dpi=300)
    plt.close()


def main(filename: str, image_folder: str):
    try:

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        stocks_df = read_stocks_from_csv(filename)

        # Process each row
        for index, row in stocks_df.iterrows():
            try:
                create_graph_from_single_ticker(row)
                logging.info(f"Created graph for {row['Ticker']}")
            except Exception as e:
                logging.error(f"Error creating graph for {row['Ticker']}: {str(e)}")

    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")

# if __name__ == "__main__":
#     main(filename='../assets/stocks_list_filter.csv', image_folder='../assets/output')
