import yaml
import pandas as pd

from yahooquery import Ticker
from telegram import send_telegram_message


def lambda_handler(event, context):
    # Assuming 'mf_tickers.yaml' is included in the deployment package
    with open('mf_tickers.yaml', 'r') as file:
        tickers_data = yaml.safe_load(file)

    all_holdings = {}

    for key, mf_ticker in tickers_data.items():
        ticker = Ticker(mf_ticker)
        holdings = ticker.fund_top_holdings

        if isinstance(holdings, pd.DataFrame) and not holdings.empty:
            for index, row in holdings.iterrows():
                symbol = row['symbol']
                holdingPercent = row['holdingPercent']
                
                if symbol not in all_holdings:
                    all_holdings[symbol] = {'mf_count': 1, 'mf_names': [key], 'total_holding_perc': float(row['holdingPercent'])}
                else:
                    all_holdings[symbol]['mf_count'] += 1
                    all_holdings[symbol]['mf_names'].append(key)
                    all_holdings[symbol]['total_holding_perc'] += float(row['holdingPercent'])

    holdings_list = list(all_holdings.items())
    sorted_holdings_list = sorted(holdings_list, key=lambda x: x[1]['mf_count'], reverse=True)

    telegram_msg = ""
    for symbol, details in sorted_holdings_list:
        if details['mf_count'] > 2:
            if symbol.endswith('.BO') or symbol.endswith('.NS'):
                symbol = symbol[:-3]

            mf_count = details['mf_count']
            mf_names = details['mf_names']
            mf_total = details['total_holding_perc'] * 100
            telegram_msg += f"{symbol} is held by {mf_count} funds - {', '.join(mf_names)} - total:{round(mf_total,1)}%\n"

    send_telegram_message(telegram_msg)
    return {'statusCode': 200, 'body': 'Message sent successfully'}
