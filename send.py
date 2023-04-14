import requests

def send_to_telegram(apiToken, chatID, message):

    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'HTML'})
        print(response.text)
    except Exception as e:
        print(e)