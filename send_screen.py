import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import subprocess
import os
from dotenv import load_dotenv
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()

endpoints = [
    {
        "name": "Mensa",
        "url": "https://www.mensen.at/",
        "selectors": [".menu-left > div:nth-child(1) > div:nth-child(1)", "div.menu-right:nth-child(1) > div:nth-child(1) > div:nth-child(1)"]
    },
    {
        "name": "Bits and Bytes",
        "url": "https://www.lakeside-scitec.com/services/gastronomie/bits-bytes",
        "selectors": ["table.contenttable:nth-child(7)"],
    },
    {
        "name": "Hotspot",
        "url": "https://www.lakeside-scitec.com/services/gastronomie/hotspot",
        "selectors": ["table.contenttable:nth-child(7)"]
    },
    {
        "name": "Uniwirt",
        "url": "https://www.uniwirt.at/wp/home/mittagsmenues/",
        "selectors": ["div.vc_row:nth-child(2)", "div.vc_row:nth-child(3)"],
        "click_button": "#BorlabsCookieBox > div > div > div > div.cookie-box > div > div > div > p:nth-child(4) > a"
    },
]

options = Options()
prefs = {
  "translate_whitelists": {"de":"en"},
  "translate":{"enabled":"true"}
}
options.add_argument("--lang=en")
# options.add_argument("--headless")
options.add_argument("--window-size=1920,3000")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("prefs", prefs)
# options.binary_location = "/usr/bin/google-chrome-stable"
driver = webdriver.Chrome(options=options)

time.sleep(15)

def send_image(botToken, imageFile, chat_id, caption):
    command = 'curl -s -X POST https://api.telegram.org/bot' + botToken + '/sendPhoto?chat_id=' + chat_id + " -F photo=@" + imageFile + " -F caption=\"" + caption + "\""
    os.system(command)
    return

for endpoint in endpoints:
    driver.get(endpoint["url"])
    time.sleep(5)
    if endpoint["name"] == "Mensa":
        driver.add_cookie({
            "name": "mensenExtLocation",
            "value": "45",
            # "domain": 'mensen.at',
            # "path": '/',
            # "secure": False
        })
        driver.get(endpoint["url"])
    elif endpoint["name"] == "Uniwirt":
        element = driver.find_element(By.CSS_SELECTOR, endpoint["click_button"])
        element.click()

    imgs = []

    for selector in endpoint["selectors"]:
        element = driver.find_element(By.CSS_SELECTOR, selector)

        location = element.location
        size = element.size

        driver.save_screenshot("shot.png")

        x = location['x']
        y = location['y']
        w = size['width']
        h = size['height']
        width = x + w
        height = y + h

        im = Image.open('shot.png')
        im = im.crop((int(x), int(y), int(width), int(height)))
        
        imgs.append(im)
    
    widths, heights = zip(*(i.size for i in imgs))

    total_width = max(widths)
    max_height = sum(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for img in imgs:
        new_im.paste(img, (0,y_offset))
        y_offset += img.size[1]
    new_im.save('to_send.png')
    
    send_image(os.getenv("TELEGRAM_API_KEY"), "to_send.png", os.getenv("BROADCAST_CHAT_ID"), endpoint["name"])
    # send_image(os.getenv("TELEGRAM_API_KEY"), "to_send.png", os.getenv("DEBUG_CHAT_ID"), endpoint["name"])