from data_processing import build_training_set
from StockAnalyzer import StockAnalyzer

def main():
    print('\nWelcome! This program will attempt to use Machine Learning(tm) to rate a stock.\nStocks are rated by their financials, and Buy/Sell/Hold recommendations are based on predicted performance versus the S&P 500.\nThis program is intended for educational/entertainment purposes only; it is not to be construed as giving actual financial advice.\nType "quit" to quit.\n')
    X, y = build_training_set()
    analyzer = StockAnalyzer(X, y)

    while(True):
        symbol = input('Please enter a stock ticker symbol: ')
        if symbol.lower() == 'quit':
            break
        try:
            result = analyzer.analyze(symbol.upper())
            if result == 1:
                print('Buy')
            elif result == 0:
                print('Hold')
            else:
                print('Sell')
        except:
            print('\nCannot retrieve data for symbol: {}. \nThe symbol may be invalid, or there may be an issue with retrieving the data.\nPlease try again.\n'.format(symbol))

if __name__ == "__main__":
    main()