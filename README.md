# Robo-Stockpicker
A simple program that utilizes machine learning to attempt to rate stocks based on their financials

***Disclaimer:** This program was created for educational/entertainment purposes. It should not be construed as providing any actual financial advice!*

Created for my final project in [CS50x](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) 2017.
### Installation:
* Ensure you are running Python >=3.6
* From a terminal window in the program's directory, run `pip install -r requirements.txt`

### Running the program:
* First, ensure you have an active internet connection (the program grabs stock data from Yahoo! Finance)
* From the program's directory, simply run `python3 stockpicker.py` and follow the directions
* *Note: this program relies on being able to determine various parameters from a company's financial reports, as posted on Yahoo! Finance.
Since this data is not always available for every company, you may encounter errors even when passing a valid ticker symbol to the program.*

#### A note on training data:
This repository already conatins a set of training data for the algorithm (`training_data.csv`).
However, if for some reason, you want to re-generate the data, the program used to create the training set can be executed by running `python3 rebuild_training_set.pv`.
This script will scrape (potentially) large amounts of data from Yahoo! Finance for all of the stock ticker symbols found in `training_symbols.txt`,
so be sure to check their [robots.txt](https://finance.yahoo.com/robots.txt) to ensure that they still permit that sort of thing!