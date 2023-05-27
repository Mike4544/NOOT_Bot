import io

from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By

from pycoingecko import CoinGeckoAPI

from time import sleep
from discord import File


class CoinData:
    def __init__(self, data):
        # Get the data
        self.price = data["market_data"]["current_price"]["usd"]
        self.ath = data["market_data"]["ath"]["usd"]
        self.atl = data["market_data"]["atl"]["usd"]
        self.supply = data["market_data"]["total_supply"]

        # Calculate the market cap
        self.market_cap = self.price * self.supply

        # Get the 24h changes
        self.change_24h = data["market_data"]["price_change_percentage_24h"]

    def __str__(self):
        return f"Price: ${self.price}\nATH: ${self.ath}\nATL: ${self.atl}\nMarket Cap: ${self.market_cap}\n24h Change: {self.change_24h}%"


def get_coin_stats():
    cg = CoinGeckoAPI()

    data = cg.get_coin_by_id(
        id="noot",
        localization="false",
        tickers="false",
        market_data="true",
        community_data="true",
        developer_data="true",
        sparkline="false"
    )

    return CoinData(data)


def get_coin_ohlc(days: int = 1):
    cg = CoinGeckoAPI()

    data = cg.get_coin_ohlc_by_id(
        id="noot",
        vs_currency="usd",
        days=str(days)
    )

    return data

def geckoterminal_stats(timeframe):

    '''
    Get the latest stats from Gecko Terminal
    '''

    # Browser
    browser = webdriver.ChromiumEdge()

    # Open the site
    url = "https://www.geckoterminal.com/bsc/pools/0x67c51db055ab177cdd1035857784481a9b4b90cb"
    browser.get(url)

    # Find the desired timeframe button
    try:
        timeframe_button = browser.find_element(By.XPATH, f"//nav[@aria-label='Tabs']/a/span[text()='{timeframe}']")
        timeframe_button.click()

    except Exception as e:
        browser.quit()
        raise Exception(e)



    # Capture a screenshot
    screenshot = browser.get_screenshot_as_png()
    browser.quit()

    im = Image.open(io.BytesIO(screenshot))

    # Dimensions of the image
    left = 66
    top = 135
    bottom = 615
    right = 400

    cropped = im.crop((left, top, right, bottom))

    img_buffer = io.BytesIO()
    cropped.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    discord_file = File(img_buffer, filename="stats.png")
    return discord_file
