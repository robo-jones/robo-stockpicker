##
## Re-builds the training data set by scraping data from Yahoo! finance for each symbol in training_symbols.txt
## Data is saved to training_data.csv
## You should only have to run this if you decided to add/remove symbols from training_symbols.txt
##

import os
import sys
import time
import requests
from datetime import date as Date, datetime, timedelta
from data_collection import get_training_data
from bs4 import BeautifulSoup
import pandas as pd


print('Re-scraping the training data set...')

# create timestamps for Now and 5 years ago, for use in retrieving historical price data
today = datetime.fromtimestamp(time.time())
minus_5_years = today + timedelta(days=-(5 * 365))

# retrieve historical S&P500 data
sp500_url = 'https://finance.yahoo.com/quote/^GSPC/history?period1={}&period2={}&interval=1mo&filter=history&frequency=1mo'.format(int(minus_5_years.timestamp()), int(today.timestamp()))
sp500_prices = BeautifulSoup(requests.get(sp500_url).content, 'html.parser')
sp500_price_table = sp500_prices.find(id='Col1-3-HistoricalDataTable-Proxy').tbody

# read the stock symbols for the training set from training_symbols.txt
symbols_file = os.path.join(sys.path[0], "training_symbols.txt")
training_symbols = []
with open(symbols_file, 'r') as file:
    for line in file:
        if line[0].isalpha():
            training_symbols.append(line.strip())

training_data = pd.DataFrame(columns=['Performance',
                                      'Return on Equity',
                                      'Return on Equity Change',
                                      'Working Capital Ratio',
                                      'Working Capital Change',
                                      'Debt to Equity',
                                      'Debt to Equity Change',
                                      'Comprehensive Free Cash Flow',
                                      'Free Cash Flow Change',
                                      'Earnings Growth'])

for symbol in training_symbols:
    try:
        print('Gathering data for: {}'.format(symbol))
        symbol_data = get_training_data(symbol=symbol,
                                        sp500_price_table=sp500_price_table,
                                        today=today,
                                        minus_5_years=minus_5_years)

        training_data = training_data.append(symbol_data, ignore_index=True)
    except:
        print('Error retrieving data for: {}, skipping'.format(symbol))

#save the training data to .csv
data_path = os.path.join(sys.path[0], "training_data.csv")
training_data.to_csv(data_path, index=False)
print('Success! Saved data to training_data.csv')