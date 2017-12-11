##
## Creates a StockAnalyzer object that will use a set of training data (supplied at construction) and a Support Vector Machine
## to classify a stock as either Buy, Hold, or Sell. Stock data is obtained by scraping Yahoo! finance.
##

from sklearn import svm
from data_collection import get_financials
import numpy as np

class StockAnalyzer():

    def __init__(self, X, y):
        self.classifier = svm.SVC(kernel='poly')
        self.classifier.fit(X, y)

    # retrieves financial data for a given symbol and uses it to classify the stock's predicted performance vs. the S&P 500
    # returns a 1 for "Buy", 0 for "Hold", and -1 for "Sell"
    def analyze(self, symbol):
        results = get_financials(symbol)

        # Format the data for out SVM by converting the dictionary to a numPy array, then converting that array to a 2D array
        data = np.array(list(results.values())).reshape(1, -1)
        return self.classifier.predict(data)[0]