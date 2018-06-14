
import requests as r
from pprint import pprint
from discord_hooks import Webhook
from BeautifulSoup import BeautifulSoup
#url = 'WEBHOOK_URL'
#msg = Webhook(url,msg="Hello there! I'm a webhook \U0001f62e")
#msg.post()


def fetch_wowtokenprice():
    """[summary]
    Fetches Prices from http://wowtokenprices.com
    Returns:
        [dictionary] -- [data]
    """

    wow_tokenpriceurl = 'http://wowtokenprices.com/current_prices.json'
    resp = r.get(wow_tokenpriceurl).json()
    # Empty dict
    priceData = {}
    priceData["price"] = resp['us']['current_price']
    priceData["lastupdate"] = resp['us']['time_of_last_change_utc_timezone']
    priceData["change"] = resp['us']['last_change']
    return priceData

def push_data_to_discord_webhook(data,webhookid,webhookkey):
    """[summary]
    Pushes data to discord web-hook
    Arguments:
        data {[dictionary]} -- [data]
        webhookid {[string]} -- [webhook id]
        webhookkey {[string]} -- [key]
    """

    if data != None:
        url = 'https://discordapp.com/api/webhooks/{}/{}'.format(webhookid,webhookkey)
        content = "Price {} \nLast Update {} \nChange {}".format(data['price'],data['lastupdate'],data['change'])
        msg = Webhook(url,msg=content)
        msg.add_field(name="Field", value='Test Text')
        msg.post()

def load_config():
    """[summary]
    Loads Keys from xml file
    Returns:
        [dictionary] -- [settings]
    """

    with open("config.xml") as f:
        content = f.read()

    y = BeautifulSoup(content)
    configKeys = {}
    configKeys["webhookid"] = y.discord.webhookid.contents[0]
    configKeys["webhooktoken"] = y.discord.webhooktoken.contents[0]
    return configKeys


def main():
    """[summary]
    Main Entry point of the module.
    """

    wow_us_tokenpricedata = fetch_wowtokenprice()
    config = load_config()
    push_data_to_discord_webhook(wow_us_tokenpricedata,config["webhookid"],config["webhooktoken"])

if __name__ == "__main__":
    main()