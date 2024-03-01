import requests

def send_telegram_message(msg):

    # Your bot's token
    #bot_token = "6558272038:AAGOXAneBcu0dQ8OE18O_401opjjrYLVuB0"
    bot_token = "6412072616:AAEzcimx6m85mSDiazMhV_oy1-45FtBQeXw"

    # The chat ID of the channel (replace with your channel's chat ID)
    bot_id = "@Amits_screener_bot"
    channel_id = "@amitscreenerbot"

    # Send the message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": msg
    }
    response = requests.post(url, data=data)
    print(response.json())