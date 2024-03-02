import yaml
import pandas as pd

from datetime import datetime
from yahooquery import Ticker
from telegram import send_telegram_message


def convert_str_to_percent(str):
    return round(float(str) * 100, 1)


def scan_equity_mutual_funds():
    with open("mf_tickers.yaml", "r") as file:
        tickers_data = yaml.safe_load(file)

    all_holdings = {}

    for key, mf_ticker in tickers_data.items():
        ticker = Ticker(mf_ticker)
        holdings = ticker.fund_top_holdings

        if isinstance(holdings, pd.DataFrame) and not holdings.empty:
            for index, row in holdings.iterrows():
                symbol = row["symbol"]
                holdingPercent = row["holdingPercent"]

                if symbol not in all_holdings:
                    all_holdings[symbol] = {
                        "mf_count": 1,
                        "mf_names": [key],
                        "total_holding_perc": float(holdingPercent),
                    }
                else:
                    all_holdings[symbol]["mf_count"] += 1
                    all_holdings[symbol]["mf_names"].append(key)
                    all_holdings[symbol]["total_holding_perc"] += float(holdingPercent)

    holdings_list = list(all_holdings.items())
    sorted_holdings_list = sorted(
        holdings_list, key=lambda x: x[1]["mf_count"], reverse=True
    )

    # Start preformatted block for HTML message
    telegram_msg = "<pre>\n"
    header = "Stock      | Tot% | Cn | Holding Funds\n"
    telegram_msg += header
    telegram_msg += (
        "-" * (max(len(header), 70)) + "\n"
    )  # Adjust the underline to match header length or a fixed width

    for symbol, details in sorted_holdings_list:
        if details["mf_count"] > 2:
            symbol_display = (
                symbol[:-3]
                if symbol.endswith(".BO") or symbol.endswith(".NS")
                else symbol
            )
            mf_total = details["total_holding_perc"] * 100
            # Adjust the formatting here to align with the new headers
            telegram_msg += "{:<10} | {:<4} | {:<2} | {}\n".format(
                symbol_display,
                round(mf_total, 1),
                details["mf_count"],
                ", ".join(details["mf_names"]),
            )

    telegram_msg += "</pre>"

    print(telegram_msg)  # For debugging
    send_telegram_message(telegram_msg, parse_mode='HTML')


def scan_balanced_advantage_funds():
    with open("bal_adv_tickers.yaml", "r") as file:
        tickers_data = yaml.safe_load(file)

    funds = {}

    for key, mf_ticker in tickers_data.items():
        ticker = Ticker(mf_ticker)
        holdings = ticker.fund_holding_info

        if isinstance(holdings, dict):
            funds[key] = {
                "equity": convert_str_to_percent(holdings[mf_ticker]["stockPosition"]),
                "bonds": convert_str_to_percent(holdings[mf_ticker]["bondPosition"]),
                "cash": convert_str_to_percent(holdings[mf_ticker]["cashPosition"]),
            }

    # Start preformatted block for HTML message
    table_str = "<pre>\n"
    table_str += "Funds  | Equity | Bonds  | Cash\n"
    table_str += "-" * 33 + "\n"

    # Fill in the rows
    for fund, allocations in funds.items():
        table_str += "{:<6} | {:>5.1f}% | {:>5.1f}% | {:>3.1f}%\n".format(
            fund, allocations["equity"], allocations["bonds"], allocations["cash"]
        )

    # Close the preformatted block
    table_str += "</pre>"

    send_telegram_message(table_str, parse_mode="HTML")


def lambda_handler(event, context):
    today_date = datetime.now().strftime("%-d-%b-%Y")
    send_telegram_message(f'<b>{today_date}</b>', parse_mode='HTML')
    scan_equity_mutual_funds()
    scan_balanced_advantage_funds()
    return {"statusCode": 200, "body": "Message sent successfully"}
