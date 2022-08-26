import requests
import datetime as dt
from datetime import timedelta, datetime
import pandas as pd
import os

#---Secret Stuff---#
# Go to Polygon.io to set up API key #
key = os.getenv('STOCK_API_KEY')
API_KEY= key

#---Parameters---#
parameters = {
    'apiKey':API_KEY,
}

class Stocks:

    def __init__ (self, ticker, days):
        self.ticker = ticker
        self.days=days

    def current (self):
        self.raw_today = dt.datetime.now()
        self.today = self.raw_today.strftime('%Y-%m-%d')
        return self.today

    def start (self):
        self.raw_today = dt.datetime.now()
        self.start_date = (self.raw_today - timedelta(days=self.days)).strftime('%Y-%m-%d')
        return self.start_date

    def stocks(self):
        self.response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/1/day/{self.start()}/{self.current()}", params = parameters)
        self.response.raise_for_status()
        self.data = self.response.json()
        self.closing_prices = []
        self.dates = []
        for close in self.data['results']:
            self.closing_prices.append(close['c'])
        for day in self.data['results']:
            self.dates.append(dt.datetime.fromtimestamp(day['t']/1000).strftime("%Y-%m-%d"))
        self.df = pd.DataFrame(list(zip(self.dates,self.closing_prices)), columns = ['Dates', 'Closing Price'])
        return self.df

    # def crypto(self):
    #     self.response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{crypto_ticker}/range/1/day/{start_date}/{today}", params = parameters)
    #     self.response.raise_for_status()
    #     dself.ata = self.response.json()
    #     self.closing_prices = []
    #     for close in self.data['results']:
    #         self.closing_prices.append(close['c'])
    #     return self.closing_prices


#----TEST CODE----#
# ticker = 'TSLA'
# days = 10
# stock = Stocks(ticker, days)
# print (stock.stocks())




