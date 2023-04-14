import requests
import deepl
import time
from send import send_to_telegram
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TELEGRAM_API_KEY")
deepl_api = os.getenv("DEEPL_API_KEY")

if os.getenv("DEBUG") == 1:
    chat_id = os.getenv("DEBUG_CHAT_ID")
else:
    chat_id = os.getenv("BROADCAST_CHAT_ID")

endpoints = [
    {
        "name": "Mensa",
        "url": "https://food.felf.io/food/mensa"
    },
    {
        "name": "Uniwirt",
        "url": "https://food.felf.io/food/uniwirt"
    },
    {
        "name": "Bits and Bytes",
        "url": "https://food.felf.io/food/bitsandbytes"
    },
    {
        "name": "Hotspot",
        "url": "https://food.felf.io/food/hotspot"
    }
]

translator = deepl.Translator(deepl_api)

output = ""

def translate(string):
    translated = translator.translate_text(string, target_lang="EN-GB")
    return translated.text

def get_string_for_entry(entry, bold=False, is_list=False):
    output = ""

    if is_list:
        output += "  - "
    if bold:
        output += "<b>"

    output += f"""{entry["name"]}"""

    if bold:
        output += "</b>"

    output += f""" ({translate(entry["name"])})"""

    if entry["price"] is not None:
        output += f""" [€ {entry["price"]}]"""

    output += "\n"
    return output

for i, endpoint in enumerate(endpoints):
    loop = True
    while loop:
        try:
            r = requests.get(endpoint["url"])
            data = r.json()
            loop = False
        except Exception as e:
            print(e)
            time.sleep(10)

    output += f"""--- <b>{endpoint["name"]}</b> ---\n\n"""

    for starter in data["starters"]:
        pass # TODO

    for main in data["mains"]:
        if main["name"] == "":
            continue

        output += get_string_for_entry(main, bold=True)

        if "entries" not in main:
            continue

        for entry in main["entries"]:
            output += get_string_for_entry(entry, is_list=True)
        
        output += "\n"

    output += "\n"
    
send_to_telegram(token, chat_id, output)        