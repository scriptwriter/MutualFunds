import yaml
import pandas as pd

from telegram import send_telegram_message
from yahooquery import Ticker

# Load ticker symbols from the YAML file
with open('mf_tickers.yaml', 'r') as file:
    tickers_data = yaml.safe_load(file)

all_holdings = {}

# Iterate over each ticker and fetch its fund_top_holdings
for key, mf_ticker in tickers_data.items():
    ticker = Ticker(mf_ticker)
    holdings = ticker.fund_top_holdings

    # Check if the holdings is a DataFrame and not empty
    if isinstance(holdings, pd.DataFrame) and not holdings.empty:
        # Iterate through each row in the DataFrame
        for index, row in holdings.iterrows():
            symbol = row['symbol']
            holdingPercent = row['holdingPercent']
            
            # If the symbol is not already in all_holdings, add it
            if symbol not in all_holdings:
                all_holdings[symbol] = { 'mf_count' : 1, 'mf_names': [key],  'total_holding_perc': float(row['holdingPercent']) }
            else:
                all_holdings[symbol]['mf_count'] += 1
                all_holdings[symbol]['mf_names'].append(key)
                all_holdings[symbol]['total_holding_perc'] += float(row['holdingPercent'])

holdings_list = list(all_holdings.items())
sorted_holdings_list = sorted(holdings_list, key=lambda x: x[1]['mf_count'], reverse=True)

# Iterate through the sorted list and print symbols with mf_count > 1
telegram_msg = ""
for symbol, details in sorted_holdings_list:
    if details['mf_count'] > 2:
        # Check if the symbol ends with .BO or .NS and strip it
        if symbol.endswith('.BO') or symbol.endswith('.NS'):
            symbol = symbol[:-3]  # This removes the last 3 characters from the symbol
        
        mf_count = details['mf_count']
        mf_names = details['mf_names']
        mf_total = details['total_holding_perc'] * 100
        # Concatenate the new line to the info_string
        telegram_msg += f"{symbol} is held by {mf_count} funds - {', '.join(mf_names)} - total:{round(mf_total,1)}%\n"

send_telegram_message(telegram_msg)