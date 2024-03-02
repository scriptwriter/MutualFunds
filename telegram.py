import requests

def send_telegram_message(msg, parse_mode=None):
    # Your bot's token
    bot_token = "6412072616:AAEzcimx6m85mSDiazMhV_oy1-45FtBQeXw"

    # The chat ID of the channel (replace with your channel's chat ID)
    channel_id = "@amitscreenerbot"

    # Send the message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": msg,
        "parse_mode": parse_mode  # This can be "Markdown", "MarkdownV2", "HTML", or None
    }
    # Remove parse_mode from the data if it's not specified to avoid sending it as None
    if parse_mode is None:
        data.pop("parse_mode")

    response = requests.post(url, json=data)  # Use json instead of data for correct headers
    print(response.json())
